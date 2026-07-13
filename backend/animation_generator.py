"""
Generateur d'animations procedurales via LLM.
Cree dynamiquement des descripteurs d'animations JSON pour les skills.
"""
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
import openai


CACHE_FILE = Path(__file__).parent / "animations_cache.json"

# Instructions systeme pour la generation d'animations
ANIMATION_SYSTEM_PROMPT = """Tu es un expert en animation procedurale pour un jeu RPG Warhammer 40K en pixel art.
Tu generes des descripteurs d'animations JSON pour des competences de combat.

Format requis:
{
  "skill_id": "nom_du_skill",
  "name": "Nom lisible",
  "duration": 600,  // duree totale en ms
  "phases": [
    {
      "name": "phase_name",
      "start": 0.0,     // progression 0.0 a 1.0
      "end": 0.3,
      "easing": "easeOut",  // linear, easeIn, easeOut, easeInOut
      "transforms": {
        "translateX": [0, 50],   // deplacement horizontal (pixels)
        "translateY": [0, -20],  // deplacement vertical
        "rotation": [0, 0.2],    // rotation en radians
        "scale": [1.0, 1.1],     // echelle
        "opacity": [1.0, 0.8]    // transparence
      }
    }
  ],
  "particles": [
    {
      "type": "spark|blood|energy|muzzle_flash|explosion",
      "at": 0.3,           // moment d'emission (progression 0-1)
      "color": "#ff6633",
      "count": 5,
      "spread": 45,        // angle de dispersion en degres
      "speed": 100         // vitesse initiale
    }
  ],
  "cameraShake": {
    "at": 0.3,
    "intensity": 2.0
  },
  "flash": {             // flash de couleur sur le sprite
    "color": "#ffffff",
    "intensity": 0.5,
    "duration": 0.2      // durée relative (0-1)
  },
  "sound": "laser_shot|sword_slash|explosion|psyker_warp"  // optionnel
}

Principes d'animation:
- Attaques de melee: windup (recul) -> strike (avancee rapide) -> recovery
- Tirs: aim (leger zoom) -> fire (recul) + particules projectile -> recovery
- Pouvoirs psyker: charge (aura) + rotation -> release (impulsion) + particules energy
- Esquive/parade: deplacement lateral rapide
- Buffs/soins: pulsation (scale oscillant) + particules douces

Durees typiques:
- Attaques rapides: 400-600ms
- Attaques lourdes: 800-1200ms
- Sorts: 1000-1500ms
- Reactions (hurt/dodge): 300-500ms

Sois creatif mais coherent avec l'univers Warhammer 40K (brutal, gothic, technologique).
Retourne UNIQUEMENT le JSON valide, sans texte additionnel."""


def load_cache() -> Dict[str, Any]:
    """Charge le cache d'animations depuis le fichier JSON."""
    if not CACHE_FILE.exists():
        return {}
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Erreur lecture cache animations: {e}")
        return {}


def save_cache(cache: Dict[str, Any]) -> bool:
    """Sauvegarde le cache d'animations dans le fichier JSON."""
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Erreur ecriture cache animations: {e}")
        return False


def get_cached_animation(skill_id: str) -> Optional[Dict[str, Any]]:
    """Recupere une animation depuis le cache."""
    cache = load_cache()
    return cache.get(skill_id)


def generate_animation_with_llm(
    skill_id: str,
    skill_name: str,
    skill_description: str,
    skill_category: str = "combat"
) -> Optional[Dict[str, Any]]:
    """
    Genere un descripteur d'animation via OpenAI API.
    
    Args:
        skill_id: Identifiant unique du skill
        skill_name: Nom lisible du skill
        skill_description: Description des effets du skill
        skill_category: Categorie (combat, psyker, support, etc.)
    
    Returns:
        Descripteur JSON d'animation ou None si echec
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY non configuree, animation par defaut utilisee")
        return None
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        user_prompt = f"""Genere une animation pour cette competence Warhammer 40K:

ID: {skill_id}
Nom: {skill_name}
Description: {skill_description}
Categorie: {skill_category}

L'animation doit etre visuelle, impactante et coherente avec la description."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": ANIMATION_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=1000
        )
        
        content = response.choices[0].message.content.strip()
        
        # Parse le JSON (parfois le LLM ajoute des backticks markdown)
        if content.startswith('```'):
            # Extrait le contenu entre ```json et ```
            lines = content.split('\n')
            json_lines = []
            in_json = False
            for line in lines:
                if line.strip().startswith('```'):
                    if in_json:
                        break
                    in_json = True
                    continue
                if in_json:
                    json_lines.append(line)
            content = '\n'.join(json_lines)
        
        animation_data = json.loads(content)
        
        # Validation basique
        if not all(k in animation_data for k in ['skill_id', 'duration', 'phases']):
            print(f"Animation incomplete pour {skill_id}")
            return None
        
        return animation_data
        
    except Exception as e:
        print(f"Erreur generation animation LLM pour {skill_id}: {e}")
        return None


def get_or_generate_animation(
    skill_id: str,
    skill_name: str = "",
    skill_description: str = "",
    skill_category: str = "combat",
    force_regenerate: bool = False
) -> Dict[str, Any]:
    """
    Recupere une animation depuis le cache ou la genere via LLM.
    Sauvegarde automatiquement les nouvelles animations.
    
    Args:
        skill_id: Identifiant unique du skill
        skill_name: Nom du skill (pour generation)
        skill_description: Description (pour generation)
        skill_category: Categorie du skill
        force_regenerate: Force la regeneration meme si existe en cache
    
    Returns:
        Descripteur d'animation (ou animation par defaut si echec)
    """
    # 1. Verifier le cache
    if not force_regenerate:
        cached = get_cached_animation(skill_id)
        if cached:
            print(f"Animation '{skill_id}' chargee depuis cache")
            return cached
    
    # 2. Generer via LLM
    print(f"Generation animation pour '{skill_id}' via LLM...")
    generated = generate_animation_with_llm(
        skill_id, skill_name, skill_description, skill_category
    )
    
    if generated:
        # 3. Sauvegarder dans le cache
        cache = load_cache()
        cache[skill_id] = generated
        if save_cache(cache):
            print(f"Animation '{skill_id}' generee et sauvegardee")
            return generated
        else:
            print(f"Animation generee mais echec sauvegarde pour '{skill_id}'")
            return generated
    
    # 4. Fallback: animation par defaut
    print(f"Utilisation animation par defaut pour '{skill_id}'")
    return get_default_animation(skill_id, skill_category)


def get_default_animation(skill_id: str, category: str = "combat") -> Dict[str, Any]:
    """
    Retourne une animation par defaut basique selon la categorie.
    Utilisee quand la generation LLM echoue.
    """
    # Tenter de charger "default_attack" depuis le cache
    cache = load_cache()
    if category in ["combat", "melee"] and "default_attack" in cache:
        anim = cache["default_attack"].copy()
        anim["skill_id"] = skill_id
        return anim
    
    # Fallback absolu: animation minimale
    return {
        "skill_id": skill_id,
        "name": skill_id.replace("_", " ").title(),
        "duration": 600,
        "phases": [
            {
                "name": "action",
                "start": 0,
                "end": 0.5,
                "easing": "easeOut",
                "transforms": {
                    "translateX": [0, 30],
                    "scale": [1.0, 1.1]
                }
            },
            {
                "name": "recovery",
                "start": 0.5,
                "end": 1.0,
                "easing": "easeIn",
                "transforms": {
                    "translateX": [30, 0],
                    "scale": [1.1, 1.0]
                }
            }
        ],
        "particles": [],
        "cameraShake": {"at": 0.3, "intensity": 1.0}
    }


def list_cached_animations() -> list[str]:
    """Retourne la liste des IDs d'animations en cache."""
    cache = load_cache()
    return list(cache.keys())


def clear_animation_cache(skill_ids: Optional[list[str]] = None) -> int:
    """
    Efface le cache d'animations.
    
    Args:
        skill_ids: Liste specifique d'IDs a supprimer, ou None pour tout effacer
    
    Returns:
        Nombre d'entrees supprimees
    """
    cache = load_cache()
    
    if skill_ids is None:
        count = len(cache)
        cache.clear()
    else:
        count = 0
        for skill_id in skill_ids:
            if skill_id in cache:
                del cache[skill_id]
                count += 1
    
    save_cache(cache)
    return count
