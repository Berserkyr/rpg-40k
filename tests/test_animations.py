"""Tests pour le systeme d'animations procedurales."""
import json
from pathlib import Path
import pytest
from backend.animation_generator import (
    load_cache, save_cache, get_cached_animation,
    get_or_generate_animation, get_default_animation,
    list_cached_animations, clear_animation_cache,
    CACHE_FILE,
)


def test_load_cache_retourne_animations_par_defaut():
    """Le cache contient des animations par defaut."""
    cache = load_cache()
    assert isinstance(cache, dict)
    assert "default_attack" in cache
    assert cache["default_attack"]["skill_id"] == "default_attack"


def test_get_cached_animation_existante():
    """Recupere une animation depuis le cache."""
    anim = get_cached_animation("default_attack")
    assert anim is not None
    assert anim["skill_id"] == "default_attack"
    assert "duration" in anim
    assert "phases" in anim


def test_get_cached_animation_inexistante():
    """Retourne None pour une animation absente."""
    anim = get_cached_animation("skill_inexistant_xyz")
    assert anim is None


def test_get_default_animation():
    """L'animation par defaut est valide."""
    anim = get_default_animation("test_skill", "combat")
    assert anim["skill_id"] == "test_skill"
    assert anim["duration"] > 0
    assert len(anim["phases"]) >= 2
    assert all("transforms" in p for p in anim["phases"])


def test_list_cached_animations():
    """Liste les animations en cache."""
    cached = list_cached_animations()
    assert isinstance(cached, list)
    assert "default_attack" in cached


def test_get_or_generate_animation_utilise_cache():
    """get_or_generate utilise le cache si disponible."""
    # Animation existante
    anim = get_or_generate_animation("default_attack", force_regenerate=False)
    assert anim["skill_id"] == "default_attack"


def test_get_or_generate_animation_sans_api_key(monkeypatch):
    """Sans API key, retourne une animation par defaut."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    anim = get_or_generate_animation(
        "nouveau_skill",
        skill_name="Nouveau Skill",
        skill_description="Test",
        force_regenerate=False
    )
    # Devrait retourner une animation par defaut
    assert anim["skill_id"] == "nouveau_skill"
    assert "phases" in anim


def test_save_and_clear_cache():
    """Sauvegarde et efface le cache."""
    # Ajouter une entree temporaire
    cache = load_cache()
    original_count = len(cache)
    
    cache["test_temp_skill"] = {
        "skill_id": "test_temp_skill",
        "duration": 500,
        "phases": []
    }
    save_cache(cache)
    
    # Verifier qu'elle existe
    cached = list_cached_animations()
    assert "test_temp_skill" in cached
    
    # Effacer juste cette entree
    cleared = clear_animation_cache(["test_temp_skill"])
    assert cleared == 1
    
    # Verifier qu'elle n'existe plus
    cached_after = list_cached_animations()
    assert "test_temp_skill" not in cached_after
    assert len(cached_after) == original_count


def test_animation_structure_valide():
    """Verifie la structure d'une animation du cache."""
    anim = get_cached_animation("shoot")
    assert anim is not None
    
    # Champs obligatoires
    assert "skill_id" in anim
    assert "duration" in anim
    assert "phases" in anim
    assert isinstance(anim["phases"], list)
    
    # Structure des phases
    for phase in anim["phases"]:
        assert "name" in phase
        assert "start" in phase
        assert "end" in phase
        assert 0 <= phase["start"] <= 1
        assert phase["start"] <= phase["end"] <= 1
        if "transforms" in phase:
            assert isinstance(phase["transforms"], dict)


def test_phases_progression_valide():
    """Les phases ont des progressions valides (0-1)."""
    cache = load_cache()
    for skill_id, anim in cache.items():
        for i, phase in enumerate(anim["phases"]):
            assert 0 <= phase["start"] <= 1, f"{skill_id} phase {i} start invalide"
            assert 0 <= phase["end"] <= 1, f"{skill_id} phase {i} end invalide"
            assert phase["start"] <= phase["end"], f"{skill_id} phase {i} start > end"


def test_particules_structure():
    """Les particules ont une structure valide."""
    anim = get_cached_animation("shoot")
    if anim and "particles" in anim:
        for p in anim["particles"]:
            assert "type" in p
            assert "at" in p
            assert 0 <= p["at"] <= 1
            if "color" in p:
                assert p["color"].startswith("#")


def test_cache_file_existe():
    """Le fichier de cache existe."""
    assert CACHE_FILE.exists()
    assert CACHE_FILE.suffix == ".json"


def test_cache_json_valide():
    """Le cache est un JSON valide."""
    with open(CACHE_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert isinstance(data, dict)
