"""Authentification JWT et hachage des mots de passe.

Ce module centralise la sécurité applicative :
- hachage des mots de passe avec bcrypt (jamais de mot de passe en clair) ;
- génération et vérification de jetons JWT signés (HS256) ;
- dépendances FastAPI pour protéger les routes et gérer les rôles.
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
import jwt
from fastapi import Depends, Header, HTTPException, status

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me-in-production")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "720"))  # 12h par défaut

ROLE_PLAYER = "player"
ROLE_ADMIN = "admin"


# ---------------------------------------------------------------------------
# Hachage de mot de passe (bcrypt)
# ---------------------------------------------------------------------------
def hash_password(password: str) -> str:
    """Retourne le hash bcrypt d'un mot de passe en clair."""
    if not password or len(password) < 4:
        raise HTTPException(status_code=400, detail="Mot de passe trop court (min. 4 caractères).")
    salt = bcrypt.gensalt()
    digest = bcrypt.hashpw(password.encode("utf-8"), salt)
    return digest.decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Vérifie un mot de passe contre son hash bcrypt."""
    if not password or not password_hash:
        return False
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except (ValueError, TypeError):
        return False


# ---------------------------------------------------------------------------
# Jetons JWT
# ---------------------------------------------------------------------------
def create_access_token(subject: str, role: str = ROLE_PLAYER) -> str:
    """Crée un jeton JWT signé pour un utilisateur donné."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Décode et vérifie un jeton JWT. Lève 401 si invalide ou expiré."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Jeton expiré.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Jeton invalide.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Jeton incomplet.")
    return payload


# ---------------------------------------------------------------------------
# Dépendances FastAPI
# ---------------------------------------------------------------------------
def _extract_bearer(authorization: Optional[str]) -> str:
    """Extrait le jeton d'un en-tête Authorization: Bearer <token>."""
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="En-tête Authorization manquant ou invalide.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return authorization.split(" ", 1)[1].strip()


class CurrentUser:
    """Utilisateur authentifié résolu depuis le jeton JWT."""

    def __init__(self, username: str, role: str) -> None:
        self.username = username
        self.role = role

    def is_admin(self) -> bool:
        return self.role == ROLE_ADMIN


def get_current_user(authorization: Optional[str] = Header(default=None)) -> CurrentUser:
    """Dépendance : exige un JWT valide et retourne l'utilisateur courant."""
    token = _extract_bearer(authorization)
    payload = decode_access_token(token)
    return CurrentUser(username=payload["sub"], role=payload.get("role", ROLE_PLAYER))


def require_admin(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    """Dépendance : exige le rôle administrateur."""
    if not user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux administrateurs.",
        )
    return user
