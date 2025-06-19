# Project 1 PRD: LoL Simulated Laning Environment (`lol_sim_env`)

**Version:** 1.2
**Date:** May 28, 2025
**Project Goal:** To develop a Python-based, OpenAI Gym-compatible **simulated environment** representing a 2v2 League of Legends bot-lane laning phase. This environment will feature Taric and relevant archetypes (ADC, enemy support, enemy ADC), focusing on core mechanics and ability interactions. It must be designed to run efficiently headless for Reinforcement Learning agent training, particularly on cloud GPU platforms, and allow for configurable game speed. Development will be iterative, with NPC AI and complex interactions simplified for MVP and expanded later.

---

## I. Vision & Scope

* **Problem:** Training RL agents for League of Legends directly in the live game is slow and resource-intensive. Cloud GPU training requires an environment that doesn't depend on a live game client GUI. Existing community environments are often outdated or hard to adapt.
* **Solution:** Create a custom, lightweight, and fast Python simulation of the LoL 2v2 laning phase. Prioritize game mechanics over visual fidelity. Allow configurable game speed to accelerate RL training.
* **Target Scenario:** 2v2 bot lane, simulated up to 15 minutes of game time.
* **Key Entities to Model (MVP focus in parentheses):**
    * Player-controlled: Taric (Support) (MVP: Q, basic movement & attacks).
    * Scripted AI Ally: Configurable "Generic ADC" archetype (MVP: moves, basic attacks).
    * Scripted AI Enemies: Two configurable archetypes from a pool (e.g., "Generic Enemy ADC", "Poke Mage Support", "Engage Support") (MVP: move, basic attacks, one placeholder ability).
    * Minions (Melee, Caster, Siege) (MVP: spawn, move, basic attacks, can be killed).
    * Turrets (Outer bot lane turret for each side) (MVP: static, can attack, can be damaged).
* **Inspiration & Reference:** Mechanics implemented will reference the [League of Legends Wiki](https://leagueoflegends.fandom.com/wiki/League_of_Legends_Wiki) for current champion abilities, item effects, minion/turret stats, and game rules (for the *current live patch*). Conceptual inspiration for structuring game logic may be drawn from understanding how other projects represent game elements, but the implementation will be new Python code.
* **Core Deliverable:** A Python package `lol_sim_env` (installable via `pip`) providing the `TaricLaningSimEnv` Gymnasium environment.
* **Development Philosophy:** Iterative development, focusing on core mechanics and agent interface first. NPC AI and complex interactions will be simplified for MVP and expanded in later phases. The environment's design will be continuously informed by the needs of Project 2 (Taric AI Agent), especially regarding observation/action spaces, through early and frequent integration testing of the Gym interface. A section in the README will detail explicit simplifications made compared to the live game.

---

## II. Requirements & Features (R-Sections)

This section outlines the target functionality. The "IV. Detailed Implementation Plan" will break these down into AI-codable tasks.

### R1: OpenAI Gymnasium Compatibility
* R1.1: Environment class (`TaricLaningSimEnv`) inherits from `gymnasium.Env`.
* R1.2: Implements standard methods: `__init__`, `step(action)`, `reset(seed=None, options=None)`, `render()` (text-based debug default), `close()`.
* R1.3: Defines `observation_space` and `action_space` using `gymnasium.spaces`.

### R2: Game Mechanics Simulation (Laning Phase Focus)

* **R2.1: Core Game Elements**
    * R2.1.1: `Entity` & `GameObject` base classes (ID, team, position, radius, stats map: HP, MaxHP, Mana, MaxMana, etc.).
    * R2.1.2: `LaneMap` (configurable dimensions, boundaries, simple pathing helpers).
    * R2.1.3: `GameClock` (simulated time, tick rate, **configurable `game_speed_multiplier`**).
    * R2.1.4: `GameState` (container for all active `GameObject`s, interfaces with systems).
* **R2.2: Units**
    * R2.2.1: `Champion` base class (core stats, Level, XP, Gold, abilities list, items list, methods for stat calculation, leveling, gold/XP, item purchase, basic AI method `get_scripted_action(game_state)`).
    * R2.2.2: `Taric` class:
        * Stats & ability parameters from `configs/champions/taric.yaml` (based on LoL Wiki).
        * Abilities (Q, W, E, R) implemented as `Ability` subclasses, with mechanics reflecting LoL Wiki (simplified for MVP):
            * Q (Starlight's Touch): Heal (AoE), mana cost, CD, scaling.
            * W (Bastion): Link to ally, passive Armor, active Shield, co-casting.
            * E (Dazzle): Linear skillshot, delay, damage, stun.
            * R (Cosmic Radiance): AoE invulnerability after delay.
        * Fixed skill order for leveling.
    * R2.2.3: `AllyADC` class:
        * Stats/abilities from `configs/champions/generic_adc_ally.yaml`.
        * Scripted AI (MVP: focus CS, follow Taric, basic attacks; Later: use 1-2 conceptual abilities like damaging skillshot, AA steroid).
    * R2.2.4: `EnemyChampion` archetypes:
        * Base `EnemyChampion`, subclasses for `EnemyADCArchetype`, `EnemyPokeSupportArchetype`, `EnemyEngageSupportArchetype`.
        * Stats/abilities from respective YAML configs.
        * Scripted AI (MVP: lane, AA, one placeholder ability; Later: more distinct archetype behaviors based on conceptual abilities like poke, engage).
    * R2.2.5: `Minion` class & wave logic:
        * Types (Melee, Caster, Siege). Stats, rewards from `configs/minions.yaml` (scaling with time).
        * Wave spawning via `GameClock` events.
        * AI: Move path, aggro logic (MVP: attack closest enemy; Later: full LoL Wiki aggro rules).
    * R2.2.6: `Turret` class:
        * Outer bot turrets. Stats from `configs/turrets.yaml`.
        * Targeting AI (MVP: attack closest in range; Later: full LoL Wiki prio, damage ramping). No plating for MVP.
* **R2.3: Game Systems**
    * R2.3.1: `AbilitySystem` (casting, resources, cooldowns, projectile/area effects, buffs/debuffs via `CombatSystem` or `GameState`).
    * R2.3.2: `CombatSystem` (resolves attacks, ability damage/healing/shields, status effects considering AD/AP, Armor/MR, damage types).
    * R2.3.3: `MovementSystem` (updates positions, simple collision).
    * R2.3.4: `GoldSystem` (passive gold, CS gold, takedown gold). Taric item purchases (Echoes of Helia, Knight's Vow & their components from `configs/items/`). NPC champs get generic stat boosts.
    * R2.3.5: `ExperienceSystem` (XP gain, champion leveling, fixed skill point allocation).
    * R2.3.6 (Optional): `EventSystem` (for discrete game events).
* **R2.4: Observation Space (Taric Agent)**
    * `gymnasium.spaces.Dict` (all numerical values normalized).
    * Includes: Taric's state (HP, Mana, CDs, Level, Pos, W-link, R-active, Gold, can-buy-item flags), Ally ADC state (relative, HP, Level), Enemy states (relative, HP, Level, CC-status, key CD flags), Minion states (N closest ally/enemy: relative, HP), Turret states (ally/enemy: relative, HP), Game time.
* **R2.5: Action Space (Taric Agent)**
    * `gymnasium.spaces.Discrete(M)`.
    * Includes: Movement (e.g., 8 directions), Abilities (Q, W on Ally, E in K directions, R), Attack (closest minion/champ), Item Purchase (Helia components, Knight's Vow components when at "base"), Recall, Do Nothing.
* **R2.6: Episode Logic & Termination**
    * Episode runs for a fixed simulated 15 minutes.
    * Champion "deaths": result in respawn timer (from `simulation_params.yaml`), return to base (Taric checks gold for purchases).
    * Final reward component at episode end based on: Gold difference, XP difference, Taric KDA, Ally KDA, Turret HP difference.

### R3: Configurability & Extensibility
* R3.1: Game parameters (champion stats, abilities, minions, items, etc.) loadable from YAML configs.
* R3.2: NPC AI logic encapsulated within their respective champion classes, allowing for varied scriptable behaviors.
* R3.3: Modular code structure to facilitate future expansions.

### R4: Performance
* R4.1: `step()` function optimized for speed (target: thousands of steps/sec on CPU).
* R4.2: Primarily use NumPy for numerics.

### R5: Headless Operation
* R5.1: Core simulation must run without GUI dependencies.
* R5.2: Optional `render()` for debugging.

### R6: Debugging & Visualization
* R6.1: Text-based `render()` method in `TaricLaningSimEnv`.
* R6.2 (Optional): Simple Pygame visualizer.
* R6.3: Debug mode flag for verbose logging.

---

## III. Proposed Folder Structure & Key Files
(As defined in `architecture.md` for Project 1)

---
## IV. Detailed Implementation Plan (Task-Oriented for AI Assistant)

This section breaks down the Requirements (R-sections) into granular, sequential tasks for implementation. Each task specifies its objective, target file(s), and precise instructions.

**Phase 1: Core Simulation Engine Setup (Corresponds to old M1.1)**

* ~~**Task 1.1.1: Initialize Project Repository and Core Files**~~ ✅ **COMPLETED**
    * **Objective:** Create main project directory, init Git, create placeholder `setup.py` and `requirements.txt`.
    * **File(s):** `lol_sim_env_project/` (root), `setup.py`, `requirements.txt`.
    * **Instructions for AI:**
        1.  "Create root directory `lol_sim_env_project`."
        2.  "Inside, initialize Git."
        3.  "Create empty `setup.py`."
        4.  "Create `requirements.txt`, add: `numpy gymnasium pyyaml`."
* ~~**Task 1.1.2: Create Initial Package Structure**~~ ✅ **COMPLETED**
    * **Objective:** Set up Python package structure for `lol_sim_env`.
    * **File(s):** Create directories and `__init__.py` files under `lol_sim_env_project/src/` as per `architecture.md`.
    * **Instructions for AI:**
        1.  "Inside `lol_sim_env_project/`, create directory `src`."
        2.  "Inside `src/`, create empty `__init__.py`."
        3.  "Inside `src/`, create subdirectories: `envs`, `game_logic`, `configs`, `utils`."
        4.  "For `envs`, `game_logic`, `configs`, `utils`, create empty `__init__.py` inside each."
        5.  "Inside `src/game_logic/`, create subdirectories: `core`, `units`, `systems`."
        6.  "For `core`, `units`, `systems`, create empty `__init__.py` inside each."
        7.  "Inside `src/configs/`, create subdirectories: `champions`, `items`."
        8.  "Inside `src/configs/items/`, create subdirectory `components`."
        9.  "For `champions`, `items`, `components`, create empty `__init__.py` inside each."
* ~~**Task 1.1.3: Define Base `Entity` Class**~~ ✅ **COMPLETED**
    * **Objective:** Create fundamental `Entity` class. (Ref: R2.1.1)
    * **File(s):** `src/game_logic/core/entity.py`.
    * **Instructions for AI:**
        1.  "In `entity.py`, import `numpy` as `np` and `typing.Any`."
        2.  "Define class `Entity`."
        3.  "`__init__(self, entity_id: str, team_id: int, position: np.ndarray, radius: float)`."
        4.  "Store args as `self.entity_id`, `self.team_id`, `self.position` (ensure `np.array(position, dtype=float)`), `self.radius`."
        5.  "Add placeholder method `update(self, time_delta: float, game_state: Any): pass`."
* ~~**Task 1.1.4: Define Base `GameObject` Class**~~ ✅ **COMPLETED**
    * **Objective:** Extend `Entity` for objects with game stats. (Ref: R2.1.1)
    * **File(s):** `src/game_logic/core/game_object.py`.
    * **Instructions for AI:**
        1.  "In `game_object.py`, import `Entity` from `.entity`, `numpy` as `np`, `typing.Dict, Any`."
        2.  "Define class `GameObject(Entity)`."
        3.  "`__init__(self, entity_id: str, team_id: int, position: np.ndarray, radius: float, base_stats: Dict[str, float])`."
        4.  "Call `super().__init__(entity_id, team_id, position, radius)`."
        5.  "Initialize `self.stats: Dict[str, float] = base_stats.copy()`. Ensure it includes at least `hp`, `max_hp`. Other stats like `mana`, `max_mana`, `ad`, `ap`, `armor`, `mr`, `move_speed`, `attack_range`, `attack_speed_base`, `hp_regen`, `mana_regen` will be added here based on champion/unit type from configs."
        6.  "Method `take_damage(self, amount: float, damage_type: str = 'physical') -> float`: Decrease `self.stats['hp']` by calculated damage (considering resistances later), clamped at 0. Return actual damage taken."
        7.  "Method `heal(self, amount: float) -> float`: Increase `self.stats['hp']` by `amount`, clamped at `self.stats.get('max_hp', self.stats['hp'])`. Return actual healing done."
        8.  "Property `is_alive(self) -> bool`: Returns `self.stats.get('hp', 0) > 0`."
* **Task 1.1.5: Implement `GameClock`**
    * **Objective:** Manage simulation time and speed. (Ref: R2.1.3)
    * **File(s):** `src/game_logic/core/game_clock.py`.
    * **Instructions for AI:**
        1.  "Define class `GameClock`."
        2.  "`__init__(self, tick_duration: float = 0.1, game_speed_multiplier: float = 1.0)`."
        3.  "Attributes: `self.current_time: float = 0.0`, `self.tick_duration: float = tick_duration`, `self.game_speed_multiplier: float = game_speed_multiplier`."
        4.  "Method `tick(self)`: Advances `self.current_time` by `self.tick_duration * self.game_speed_multiplier`."
        5.  "Method `get_time_delta(self) -> float`: Returns `self.tick_duration * self.game_speed_multiplier`."
        6.  "Method `reset(self)`: Sets `self.current_time = 0.0`."
* **Task 1.1.6: Implement `GameState` Container**
    * **Objective:** Hold all game entities and manage global state. (Ref: R2.1.4)
    * **File(s):** `src/game_logic/game_state.py`.
    * **Instructions for AI:**
        1.  "Import `GameClock`, `List, Dict, Type` from `typing`, `GameObject`."
        2.  "Define class `GameState`."
        3.  "`__init__(self, game_clock: GameClock)`: Store `game_clock`. Initialize `self.entities: Dict[str, GameObject] = {}`, `self.champions: List[GameObject] = []`, `self.minions: List[GameObject] = []`, `self.turrets: List[GameObject] = []`, `self.projectiles: List[GameObject] = []` (for future use)."
        4.  "Method `add_entity(self, entity: GameObject)`: Adds entity to `self.entities` (keyed by `entity_id`) and to appropriate list based on type."
        5.  "Method `remove_entity(self, entity_id: str)`: Removes entity."
        6.  "Method `get_entity_by_id(self, entity_id: str) -> GameObject | None`."
        7.  "Method `get_entities_by_team(self, team_id: int) -> List[GameObject]`."
        8.  "Method `reset(self)`: Clear all entity lists/dicts. Reset clock."
* **Task 1.1.7: Implement `LaneMap` Basics**
    * **Objective:** Define lane boundaries. (Ref: R2.1.2)
    * **File(s):** `src/game_logic/core/map.py`.
    * **Instructions for AI:**
        1.  "Import `numpy` as `np`."
        2.  "Define class `LaneMap`."
        3.  "`__init__(self, length: float, width: float)` from `simulation_params.yaml`."
        4.  "Store `self.length`, `self.width`."
        5.  "Method `is_within_bounds(self, position: np.ndarray) -> bool`: Checks if `0 <= position[0] <= self.length` and `0 <= position[1] <= self.width`."
* **Task 1.1.8: Create `utils/vector_math.py`**
    * **Objective:** Basic 2D vector operations.
    * **File(s):** `src/utils/vector_math.py`.
    * **Instructions for AI:**
        1.  "Import `numpy` as `np`."
        2.  "Implement `distance(p1: np.ndarray, p2: np.ndarray) -> float`."
        3.  "Implement `normalize(vector: np.ndarray) -> np.ndarray` (handle zero vector)."
        4.  "Implement `angle_between(v1: np.ndarray, v2: np.ndarray) -> float` (optional for now)."
* **Task 1.1.9: Create `utils/constants.py`**
    * **Objective:** Define global constants.
    * **File(s):** `src/utils/constants.py`.
    * **Instructions for AI:**
        1.  "Define `TEAM_BLUE = 0`."
        2.  "Define `TEAM_RED = 1`."
        3.  "Define `MAX_LEVEL = 18`."

**Phase 2: Champion Implementation & Basic Movement (Corresponds to old M1.2)**

* **Task 2.1: Implement `Champion` Base Class**
    * **Objective:** Define core champion attributes and methods. (Ref: R2.2.1)
    * **File(s):** `src/game_logic/units/champion.py`.
    * **Instructions for AI:**
        1.  "Import `GameObject` from `..core.game_object`, `List, Dict, Type` from `typing`, `Ability` from `..systems.ability_system` (placeholder, will create `Ability` class later)."
        2.  "Define class `Champion(GameObject)`."
        3.  "`__init__(self, entity_id: str, team_id: int, position: np.ndarray, radius: float, base_stats: Dict[str, float], champion_name: str)`: Call super. Store `champion_name`. Initialize `self.level: int = 1`, `self.xp: float = 0.0`, `self.gold: int = 500` (from `simulation_params.yaml` starting gold), `self.abilities: Dict[str, Ability] = {}`, `self.items: List[Any] = []` (will be `Item` objects later), `self.respawn_timer: float = 0.0`."
        4.  "Method `add_xp(self, amount: float, experience_system: Any)`: Adds XP, calls `experience_system.check_level_up(self)`."
        5.  "Method `level_up(self, new_level_stats: Dict[str, float], ability_points_to_allocate: int)`: Updates level, applies `new_level_stats` to `self.stats`. Placeholder for allocating ability points."
        6.  "Method `add_gold(self, amount: int)`."
        7.  "Method `can_afford(self, item_cost: int) -> bool`."
        8.  "Method `purchase_item(self, item_object: Any, gold_system: Any)`: If can afford, add to `self.items`, deduct gold via `gold_system`, recalculate stats."
        9.  "Method `recalculate_final_stats(self)`: Combines base stats with item stats (placeholder)."
        10. "Method `get_scripted_action(self, game_state: Any) -> Any`: Placeholder for NPC AI, return `None` for now."
        11. "Method `update(self, time_delta: float, game_state: Any)`: If `respawn_timer > 0`, tick down timer. Else, allow actions."
* **Task 2.2: Implement `MovementSystem`**
    * **Objective:** Handle entity movement. (Ref: R2.3.3)
    * **File(s):** `src/game_logic/systems/movement_system.py`.
    * **Instructions for AI:**
        1.  "Import `GameObject`, `GameState`, `LaneMap`, `np`."
        2.  "Define class `MovementSystem`."
        3.  "Method `move_entity_towards(self, entity: GameObject, target_position: np.ndarray, time_delta: float, game_map: LaneMap)`: Calculate direction vector. Calculate distance to move (`entity.stats['move_speed'] * time_delta`). New position is current + `direction * distance_to_move`. Ensure new position is within `game_map.is_within_bounds()`. Update `entity.position`."
        4.  "Method `handle_collisions(self, entity: GameObject, all_other_entities: List[GameObject])`: (MVP Simplification) For now, if `entity` overlaps significantly with any other (based on radii), revert its last movement or prevent it. More complex response deferred."
* **Task 2.3: Implement `Taric` Specifics (Stats & Config)**
    * **Objective:** Create `Taric` class and load his base data. (Ref: R2.2.2)
    * **File(s):** `src/game_logic/units/taric.py`, `src/configs/champions/taric.yaml`.
    * **Instructions for AI:**
        1.  "In `taric.py`, import `Champion`."
        2.  "Define class `Taric(Champion)`."
        3.  "`__init__(self, entity_id: str, team_id: int, position: np.ndarray, radius: float, base_stats: Dict[str, float])`: Call `super().__init__(..., champion_name='Taric')`. Later, initialize Taric's specific abilities here."
        4.  "Create `taric.yaml` in `configs/champions/`. Populate with Taric's Level 1 base stats (HP, Mana, AD, Armor, MR, MS, Attack Range, HP Regen, Mana Regen etc.) by referencing the official League of Legends Wiki for *Taric*. Also add growth stats (e.g., `hp_per_level`). Add ability parameters for Q,W,E,R (e.g., `q_base_heal`, `q_mana_cost`, `q_cooldown`)."
* **Task 2.4: Create `Ability` Base and `AbilitySystem` Shell**
    * **Objective:** Define structure for abilities and their management. (Ref: R2.3.1)
    * **File(s):** `src/game_logic/units/ability.py` (or `systems/`), `src/game_logic/systems/ability_system.py`.
    * **Instructions for AI:**
        1.  "In `ability.py` (or `systems/ability.py`), define base class `Ability`."
        2.  "`__init__(self, owner: Champion, name: str, level: int, mana_cost: float, cooldown: float, range: float = 0, ...)` based on common ability params from `taric.yaml`."
        3.  "Attributes: `self.owner`, `self.name`, `self.level`, `self.mana_cost`, `self.base_cooldown`, `self.current_cooldown = 0.0`, `self.range`."
        4.  "Method `is_ready(self) -> bool`: Returns `self.current_cooldown <= 0 and self.owner.stats['mana'] >= self.get_current_mana_cost()`."
        5.  "Method `get_current_mana_cost(self) -> float`: Returns `self.mana_cost` (can be overridden for abilities with scaling costs)."
        6.  "Method `get_current_cooldown(self) -> float`: Returns `self.base_cooldown` (later factor in Ability Haste)."
        7.  "Method `trigger(self, game_state: GameState, target_pos: np.ndarray = None, target_entity_id: str = None)`: Placeholder, to be implemented by subclasses. If cast successfully, sets `self.current_cooldown = self.get_current_cooldown()` and deducts mana from `self.owner`."
        8.  "Method `tick(self, time_delta: float)`: Decrements `self.current_cooldown` by `time_delta`, clamped at 0."
        9.  "In `ability_system.py`, define class `AbilitySystem`."
        10. "Method `attempt_cast(self, caster: Champion, ability_slot_key: str, game_state: GameState, target_pos: np.ndarray = None, target_entity_id: str = None)`: Get ability from `caster.abilities[ability_slot_key]`. If `ability.is_ready()`, call `ability.trigger(...)`."
        11. "Method `tick_cooldowns(self, champion_list: List[Champion], time_delta: float)`: Iterate through champions and their abilities, calling `ability.tick(time_delta)`."
* **Task 2.5: Implement Taric's Q (Starlight's Touch - MVP: Targeted Heal) & `CombatSystem`**
    * **Objective:** Enable Taric's first ability and the system to apply its effects. (Ref: R2.2.2, R2.3.2)
    * **File(s):** `taric.py`, `combat_system.py`.
    * **Instructions for AI:**
        1.  "In `taric.py`, define `StarlightsTouch(Ability)`."
        2.  "Override `trigger()`: If `target_entity_id` is provided, get target from `game_state`. Call `combat_system.apply_heal(caster=self.owner, target=target_entity, base_heal=self.params['base_heal_amount_lvl_1'])`. If no target, heal self. (Params like `base_heal_amount_lvl_1` come from ability instance, loaded from `taric.yaml`)."
        3.  "In Taric's `__init__`, create an instance: `self.abilities['Q'] = StarlightsTouch(self, name='StarlightsTouch', ..., params_from_taric_yaml_for_q)`."
        4.  "In `combat_system.py`, define class `CombatSystem`."
        5.  "Method `apply_damage(self, target: GameObject, amount: float, attacker: GameObject = None, damage_type: str = 'physical')`: Calls `target.take_damage(actual_calculated_amount)`. (For now, `actual_calculated_amount = amount`). Print debug log."
        6.  "Method `apply_heal(self, target: GameObject, amount: float, caster: GameObject = None)`: Calls `target.heal(amount)`. Print debug log."
        7.  "Method `resolve_auto_attack(self, attacker: Champion, target: GameObject)`: Get `attacker.stats['attack_damage']`. Call `self.apply_damage(target, damage, attacker=attacker)`."
* **Task 2.6: Basic Gym Environment Shell (`TaricLaningSimEnv` - CRITICAL INTEGRATION POINT)**
    * **Objective:** Create the runnable Gym environment with Taric's MVP capabilities. (Ref: R1)
    * **File(s):** `src/envs/taric_laning_sim_env.py`.
    * **Instructions for AI:**
        1.  "Import `gymnasium as gym`, `spaces` from `gymnasium`, `np`, relevant classes from `game_logic`."
        2.  "Define `TaricLaningSimEnv(gym.Env)`."
        3.  "`__init__(self, config_path: str = 'default')`: (Load `simulation_params.yaml`, `taric.yaml` using `pyyaml`). Initialize `self.game_clock`, `self.game_state`, `self.lane_map`, `self.taric` (instance of `Taric`), `self.ability_system`, `self.combat_system`, `self.movement_system`."
        4.  "Add `self.taric` to `self.game_state`."
        5.  "**Observation Space (MVP):** `spaces.Dict({'taric_hp_norm': spaces.Box(0,1), 'taric_mana_norm': spaces.Box(0,1), 'taric_q_cd_norm': spaces.Box(0,1), 'taric_pos_norm': spaces.Box(low=0.0, high=1.0, shape=(2,), dtype=np.float32)})`."
        6.  "**Action Space (MVP):** `spaces.Discrete(6)` (0:NoOp, 1:Move_Up, 2:Move_Down, 3:Move_Left, 4:Move_Right, 5:Use_Q_Self (or on fixed dummy target for testing))."
        7.  "Method `_get_obs(self) -> Dict`: Populate observation dict values from `self.taric.stats` and `self.taric.abilities['Q']`, normalize them."
        8.  "Method `reset(self, seed=None, options=None) -> Tuple[Dict, Dict]`: Call `super().reset(seed=seed)`. Reset `self.game_state`, re-initialize/reset `self.taric` (position, HP/Mana). Return `(self._get_obs(), {})`."
        9.  "Method `step(self, action: int) -> Tuple[Dict, float, bool, bool, Dict]`:
            a. Get Taric: `taric = self.game_state.get_entity_by_id('taric_player_1')`.
            b. Map `action` to Taric's behavior:
                If 0 (NoOp): pass.
                If 1-4 (Move): Calculate target position delta. Call `self.movement_system.move_entity_towards(taric, new_pos, self.game_clock.get_time_delta(), self.lane_map)`.
                If 5 (Use Q): Call `self.ability_system.attempt_cast(taric, 'Q', self.game_state, target_entity_id=taric.entity_id)`. (For MVP, Q targets self or a fixed dummy if one is added for testing heals).
            c. Update Taric's cooldowns: `self.ability_system.tick_cooldowns([taric], self.game_clock.get_time_delta())`.
            d. `self.game_clock.tick()`.
            e. `obs = self._get_obs()`.
            f. `reward = 0.0` (MVP).
            g. `terminated = self.game_clock.current_time >= MAX_EPISODE_TIME_MVP` (e.g., 60s MVP).
            h. `truncated = False`.
            i. `info = {}`.
            j. Return `(obs, reward, terminated, truncated, info)`."
        10. "Method `render(self)`: Print `self.taric.stats`, `self.taric.abilities['Q'].current_cooldown`."
        11. "Create `examples/run_random_agent.py`. Instantiate env, loop `env.action_space.sample()`, call `env.step()`, `env.render()`."
        12. "Add `gymnasium.utils.env_checker.check_env(env)` to example script."
    * **Verification:** Random agent runs without errors. `check_env` passes.
    * **(PROJECT 2 INTEGRATION HOOK): At this point, pause Project 1 feature development and perform Project 2's M2.4 (RL Agent Integration MVP) to test this basic interface.**

**Phase 3: Adding Other Units & Basic AI (Corresponds to old M1.4)**
*(Tasks here will be similar in granularity: define class, load config, implement very simple AI method, add to GameState, update Observation/Action space in Env if Taric interacts with them, update CombatSystem)*

* **Task 3.1:** Implement `Minion` class, basic AI (move fixed path, attack nearest if in range), wave spawning.
* **Task 3.2:** Implement `Turret` class, basic AI (attack nearest in range).
* **Task 3.3:** Implement `AllyADC` class, basic AI (follow Taric, attack nearest).
* **Task 3.4:** Implement `EnemyChampion` archetypes (e.g., `EnemyADCArchetype`, `EnemyPokeSupportArchetype`) with 1 placeholder ability each and very simple AI (stay in lane, attack nearest).
* **Task 3.5:** Implement `ExperienceSystem` & `GoldSystem` (passive gain, CS for Taric only for MVP, simplified "item purchase" for Taric as stat block if gold > X and at "base" after recall/respawn action).
* **Task 3.6:** Expand `TaricLaningSimEnv` Observation Space for new units (relative positions, HP).
* **Task 3.7:** Expand `TaricLaningSimEnv` Action Space for Taric (e.g., `ATTACK_ENEMY_MINION_CLOSEST`, `ATTACK_ENEMY_CHAMPION_CLOSEST`).

**Phase 4: Completing Taric's Kit & Core Gameplay Loop (Corresponds to old M1.5 - MVP End)**
*(Tasks to implement full W, E, R for Taric, finalize Obs/Action spaces, implement full episode logic (15 min, respawns), and comprehensive reward function)*

* **Task 4.1:** Implement Taric's W (Bastion) - link, passive armor, active shield.
* **Task 4.2:** Implement Taric's E (Dazzle) - line skillshot, stun (using discrete angle actions).
* **Task 4.3:** Implement Taric's R (Cosmic Radiance) - AoE invulnerability after delay.
* **Task 4.4:** Finalize Observation Space in `TaricLaningSimEnv` (as per R2.4).
* **Task 4.5:** Finalize Action Space in `TaricLaningSimEnv` (as per R2.5, including item purchase & recall).
* **Task 4.6:** Implement full episode logic: 15 min fixed duration, champion respawn timers, return to base logic for Taric to enable item purchases.
* **Task 4.7:** Implement comprehensive Reward Function (in-step sparse rewards + terminal evaluation based on gold/xp/turret/KDA diffs).

---
## V. Risks & Challenges (Project 1)
(As previously detailed: Fidelity vs. Complexity, Simulation Effort, NPC AI complexity post-MVP, Reward Shaping, State/Action Design, Performance. Iterative MVPs and early agent interface testing are key mitigations.)

---