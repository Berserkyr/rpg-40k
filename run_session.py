"""
CLI driver complet pour Survivant de Ruche
Integre tous les systemes: combat, inventaire, progression, carte, quetes, relations, monde
"""

from __future__ import annotations

import os
import random
from pathlib import Path
from typing import List, Optional

import typer
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel

try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    pass

# Imports des systemes de base
from src.dice import format_roll, roll_2d6
from src.prompt_builder import build_system_prompt
from src.state import CharacterState
from src.entities import Faction, ThreatLevel, generate_entity, generate_encounter

# Imports des nouveaux systemes
from src.combat import CombatState, Combatant, CombatAction, ActionType, resolve_attack, resolve_flee
from src.inventory import Inventory, generate_loot, WEAPON_TEMPLATES, ARMOR_TEMPLATES
from src.progression import ProgressionState, SKILL_TREE, award_xp, format_skill_tree, get_available_skills
from src.world import WorldMap, create_starting_map, format_zone_info, format_map_overview
from src.quests import QuestLog, create_starting_quests, format_quest_log, format_quest_info
from src.relationships import RelationshipManager, create_starting_relationships, format_relationships_overview
from src.persistence import GameWorld, create_new_game_world, format_world_status, generate_gm_context

app = typer.Typer(help="Survivant de Ruche - RPG solo Warhammer 40K")
console = Console()

HELP_TEXT = """
=== COMMANDES DISPONIBLES ===

GENERAL:
  !help          -> Afficher cette aide
  !status        -> Fiche de personnage
  !roll          -> Lancer 2d6
  !save          -> Sauvegarder
  !quit          -> Quitter

COMBAT:
  !spawn [faction] [niveau]   -> Generer un ennemi
  !fight                      -> Mode combat tactique
  !attack / !defend / !flee   -> Actions de combat

INVENTAIRE:
  !inv           -> Voir l'inventaire
  !loot [niveau] -> Generer du butin

PROGRESSION:
  !xp            -> Voir XP et niveau
  !skills        -> Arbre de competences
  !learn [id]    -> Apprendre une competence

EXPLORATION:
  !map           -> Voir la carte
  !zone          -> Info zone actuelle
  !go [zone_id]  -> Se deplacer

QUETES:
  !quests        -> Journal de quetes
  !quest [id]    -> Details d'une quete

RELATIONS:
  !rep           -> Vue des reputations
  !npcs          -> PNJs rencontres

MONDE:
  !world         -> Etat du monde
"""


class GameSession:
    """Session de jeu complete avec tous les systemes."""
    
    def __init__(
        self,
        character_file: Path,
        prompt_file: Path,
        save_dir: Path,
        campaign_name: str = "campagne1",
    ):
        self.save_dir = save_dir / campaign_name
        self.save_dir.mkdir(parents=True, exist_ok=True)
        
        # Charger ou creer le monde
        self.world = GameWorld.load(self.save_dir)
        if not self.world:
            self.world = create_new_game_world(campaign_name)
            console.print("[green]Nouvelle campagne creee![/green]")
        
        # Charger le personnage
        self.character = CharacterState.from_file(character_file)
        
        # Initialiser les sous-systemes
        self._init_subsystems()
        
        # Prompt MJ
        self.prompt_file = prompt_file
        
        # Combat actif
        self.combat: Optional[CombatState] = None
    
    def _init_subsystems(self) -> None:
        """Initialise les sous-systemes."""
        import yaml
        
        # Progression
        prog_file = self.save_dir / "progression.yaml"
        if prog_file.exists():
            with open(prog_file, "r", encoding="utf-8") as f:
                self.progression = ProgressionState.from_dict(yaml.safe_load(f))
        else:
            self.progression = ProgressionState()
        
        # Inventaire
        inv_file = self.save_dir / "inventory.yaml"
        if inv_file.exists():
            with open(inv_file, "r", encoding="utf-8") as f:
                self.inventory = Inventory.from_dict(yaml.safe_load(f))
        else:
            self.inventory = Inventory()
            self.inventory.add_item(WEAPON_TEMPLATES["couteau_improvise"])
            self.inventory.add_item(ARMOR_TEMPLATES["vetements_ouvrier"])
        
        # Carte
        map_file = self.save_dir / "world_map.yaml"
        if map_file.exists():
            with open(map_file, "r", encoding="utf-8") as f:
                self.world_map = WorldMap.from_dict(yaml.safe_load(f))
        else:
            self.world_map = create_starting_map()
        
        # Quetes
        quest_file = self.save_dir / "quests.yaml"
        if quest_file.exists():
            with open(quest_file, "r", encoding="utf-8") as f:
                self.quest_log = QuestLog.from_dict(yaml.safe_load(f))
        else:
            self.quest_log = create_starting_quests()
        
        # Relations
        rel_file = self.save_dir / "relationships.yaml"
        if rel_file.exists():
            with open(rel_file, "r", encoding="utf-8") as f:
                self.relationships = RelationshipManager.from_dict(yaml.safe_load(f))
        else:
            self.relationships = create_starting_relationships()
    
    def save_all(self) -> None:
        """Sauvegarde tous les systemes."""
        import yaml
        
        self.world.save(self.save_dir)
        
        with open(self.save_dir / "progression.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(self.progression.to_dict(), f, allow_unicode=True)
        
        with open(self.save_dir / "inventory.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(self.inventory.to_dict(), f, allow_unicode=True)
        
        with open(self.save_dir / "world_map.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(self.world_map.to_dict(), f, allow_unicode=True)
        
        with open(self.save_dir / "quests.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(self.quest_log.to_dict(), f, allow_unicode=True)
        
        with open(self.save_dir / "relationships.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(self.relationships.to_dict(), f, allow_unicode=True)
        
        console.print(f"[dim]Sauvegarde -> {self.save_dir}[/dim]")
    
    def build_full_prompt(self) -> str:
        """Construit le prompt complet avec contexte."""
        base_prompt = build_system_prompt(self.prompt_file, self.character)
        world_context = generate_gm_context(self.world)
        zone = self.world_map.get_current_zone()
        zone_ctx = f"\nZone actuelle: {zone.name}\n{zone.description}" if zone else ""
        return f"{base_prompt}\n\n{world_context}\n{zone_ctx}"
    
    def handle_command(self, cmd: str) -> Optional[str]:
        """Gere une commande utilisateur."""
        if not cmd.startswith("!"):
            return None
        
        parts = cmd[1:].split()
        command = parts[0].lower() if parts else ""
        args = parts[1:] if len(parts) > 1 else []
        
        if command == "help":
            return HELP_TEXT
        if command == "status":
            return self.character.as_markdown()
        if command == "roll":
            return format_roll(roll_2d6())
        if command == "save":
            self.save_all()
            return "Sauvegarde effectuee."
        
        # Combat
        if command == "spawn":
            return self._cmd_spawn(args)
        if command == "fight":
            return self._cmd_fight()
        if command in ("attack", "defend", "flee"):
            return self._cmd_combat_action(command)
        
        # Inventaire
        if command == "inv":
            return self.inventory.as_markdown()
        if command == "loot":
            level = int(args[0]) if args else 1
            items = generate_loot(level)
            for item in items:
                self.inventory.add_item(item)
            return f"Butin: {', '.join(i.name for i in items)}"
        
        # Progression
        if command == "xp":
            p = self.progression
            return f"Niveau: {p.level}\nXP: {p.current_xp}/{p.xp_for_next_level()}"
        if command == "skills":
            return format_skill_tree(self.progression)
        if command == "learn":
            if not args:
                avail = get_available_skills(self.progression)
                if avail:
                    return "Disponibles:\n" + "\n".join(f"  {s.id}: {s.name}" for s in avail)
                return "Aucune competence disponible."
            skill_id = args[0]
            if skill_id in SKILL_TREE:
                success, msg = self.progression.unlock_skill(SKILL_TREE[skill_id])
                return msg
            return f"Competence '{skill_id}' inconnue."
        
        # Carte
        if command == "map":
            return format_map_overview(self.world_map)
        if command == "zone":
            zone = self.world_map.get_current_zone()
            return format_zone_info(zone) if zone else "Position inconnue."
        if command == "go":
            if not args:
                zones = self.world_map.get_accessible_zones()
                return "Accessibles:\n" + "\n".join(f"  {z.id}: {z.name}" for z in zones)
            success, msg, event = self.world_map.travel_to(args[0], self.world.global_state.current_scene)
            result = msg
            if event:
                result += f"\n[EVENT] {event}"
            return result
        
        # Quetes
        if command == "quests":
            return format_quest_log(self.quest_log)
        if command == "quest":
            if not args:
                return "Usage: !quest [id]"
            quest = self.quest_log.get_quest(args[0])
            return format_quest_info(quest) if quest else "Quete inconnue."
        
        # Relations
        if command == "rep":
            return format_relationships_overview(self.relationships)
        if command == "npcs":
            npcs = self.relationships.get_met_npcs()
            if not npcs:
                return "Aucun PNJ rencontre."
            return "\n".join(f"  {n.name} ({n.role})" for n in npcs)
        
        # Monde
        if command == "world":
            return format_world_status(self.world)
        
        return f"Commande inconnue: !{command}"
    
    def _cmd_spawn(self, args: list) -> str:
        faction_str = args[0] if args else "tyranide"
        level_str = args[1] if len(args) > 1 else "standard"
        faction_map = {"tyranide": Faction.TYRANID, "culte": Faction.GENESTEALER_CULT, "garde": Faction.IMPERIAL_GUARD}
        level_map = {"sbire": ThreatLevel.MINION, "standard": ThreatLevel.STANDARD, "elite": ThreatLevel.ELITE, "boss": ThreatLevel.BOSS}
        faction = faction_map.get(faction_str.lower(), Faction.TYRANID)
        level = level_map.get(level_str.lower(), ThreatLevel.STANDARD)
        return generate_entity(faction, level).as_markdown()
    
    def _cmd_fight(self) -> str:
        if self.combat and self.combat.is_active:
            return "Combat en cours! !attack, !defend ou !flee"
        entity = generate_entity(Faction.TYRANID, ThreatLevel.STANDARD)
        enemy = Combatant.from_entity(entity)
        player = Combatant.from_player_state(self.character)
        self.combat = CombatState(player=player, enemies=[enemy])
        return f"=== COMBAT ===\nEnnemi: {enemy.name} (PV:{enemy.health})\nActions: !attack, !defend, !flee"
    
    def _cmd_combat_action(self, action: str) -> str:
        if not self.combat or not self.combat.is_active:
            return "Pas de combat. Utilisez !fight"
        
        results = []
        player = self.combat.player
        enemies = self.combat.get_living_enemies()
        
        if not enemies:
            self.combat.is_active = False
            return "Plus d'ennemis!"
        
        target = enemies[0]
        
        # Action du joueur
        if action == "attack":
            result = resolve_attack(player, target)
            results.append(result["description"])
            if result["hit"]:
                target.health -= result["damage"]
                if target.health <= 0:
                    target.is_dead = True
                    results.append(f"{target.name} est elimine!")
        elif action == "defend":
            player.is_defending = True
            results.append(f"{player.name} se met en position defensive.")
        elif action == "flee":
            flee_result = resolve_flee(player, enemies)
            results.append(flee_result["description"])
            if flee_result["success"]:
                self.combat.is_active = False
                return "\n".join(results) + "\nVous avez fui!"
        
        # Actions des ennemis vivants
        for enemy in self.combat.get_living_enemies():
            enemy_action = random.choice(["attack", "attack", "defend"])
            if enemy_action == "attack":
                result = resolve_attack(enemy, player)
                results.append(result["description"])
                if result["hit"]:
                    player.health -= result["damage"]
                    if player.health <= 0:
                        player.is_dead = True
            else:
                enemy.is_defending = True
        
        # Reset defense pour le tour suivant
        player.is_defending = False
        for e in enemies:
            e.is_defending = False
        
        # Verifier fin de combat
        is_over, reason = self.combat.is_combat_over()
        if is_over:
            self.combat.is_active = False
            if reason == "victoire":
                xp_amount, xp_msgs = award_xp(self.progression, "victoire_difficile")
                results.append("\nVICTOIRE!")
                results.extend(xp_msgs)
            elif reason == "defaite":
                results.append("\nDEFAITE...")
            self.combat = None
        else:
            results.append(f"\nVous: {player.health}PV | Ennemi: {target.health}PV")
        
        return "\n".join(results)


def _require_api_key() -> str:
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        raise typer.BadParameter(
            "OPENAI_API_KEY est absent. Exportez la variable ou utilisez un fichier .env."
        )
    return key


def _print_panel(title: str, body: str) -> None:
    console.print(Panel(body, title=title, expand=True))


@app.command()
def play(
    character_file: Path = typer.Option(Path("character_sheet.yaml"), exists=True, readable=True),
    prompt_file: Path = typer.Option(Path("prompt_survivant.md"), exists=True, readable=True),
    model: str = typer.Option("gpt-4.1-mini", help="Modele OpenAI a utiliser."),
    save_dir: Path = typer.Option(Path("saves"), help="Dossier de sauvegarde."),
    campaign: str = typer.Option("campagne1", help="Nom de la campagne."),
    auto_start: bool = typer.Option(True, help="Lancer la scene d'ouverture."),
) -> None:
    """Lance une session interactive Survivant de Ruche."""

    api_key = _require_api_key()
    client = OpenAI(api_key=api_key)
    
    # Initialiser la session complete
    session = GameSession(character_file, prompt_file, save_dir, campaign)
    
    # Construire le prompt systeme complet
    system_prompt = session.build_full_prompt()
    messages: List[dict[str, str]] = [{"role": "system", "content": system_prompt}]

    console.print("[bold cyan]SURVIVANT DE RUCHE[/bold cyan]")
    console.print(f"[dim]Campagne: {campaign} | Scene: {session.world.global_state.current_scene}[/dim]")
    _print_panel("Aide", "Tapez !help pour voir les commandes disponibles.")

    # Scene d'ouverture
    if auto_start and session.world.global_state.total_scenes == 0:
        start_message = "Lance la scene d'ouverture. Karimus se reveille dans le chaos de l'invasion tyranide."
        messages.append({"role": "user", "content": start_message})
        assistant_text = _request_completion(client, model, messages)
        _print_panel("MJ", assistant_text)
        session.world.advance_scene()
        session.save_all()

    while True:
        try:
            user_input = console.input("[bold yellow]>>> [/]").strip()
        except (KeyboardInterrupt, EOFError):
            break
        
        if not user_input:
            continue
        
        if user_input.lower() == "!quit":
            session.save_all()
            console.print("[cyan]A bientot, survivant...[/cyan]")
            break
        
        # Verifier si c'est une commande
        cmd_result = session.handle_command(user_input)
        if cmd_result is not None:
            _print_panel("Systeme", cmd_result)
            continue
        
        # Sinon envoyer au MJ
        messages.append({"role": "user", "content": user_input})
        assistant_text = _request_completion(client, model, messages)
        
        # Parser les mises a jour d'etat
        changes = session.character.apply_updates_from_text(assistant_text)
        if changes:
            console.print(f"[dim green]Mise a jour: {', '.join(changes)}[/dim green]")
        
        _print_panel("MJ", assistant_text)
        
        # Avancer le monde
        scene_msgs = session.world.advance_scene()
        for msg in scene_msgs:
            console.print(f"[bold yellow]{msg}[/bold yellow]")
        
        # Avancer les timers de quetes
        expired = session.quest_log.advance_all_timers()
        for exp in expired:
            console.print(f"[bold red]{exp}[/bold red]")
        
        session.save_all()


def _request_completion(client: OpenAI, model: str, messages: List[dict[str, str]]) -> str:
    """Send conversation to OpenAI and capture the assistant reply."""

    response = client.chat.completions.create(model=model, messages=messages)
    answer = response.choices[0].message.content or ""
    messages.append({"role": "assistant", "content": answer})
    return answer


if __name__ == "__main__":
    app()
