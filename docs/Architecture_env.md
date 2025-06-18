# Architecture & File Structures

This document outlines the proposed file and folder structures for the two main projects:
1.  `lol_sim_env`: The Python-based simulated 2v2 LoL laning environment for RL training.
2.  `taric_ai_agent`: The Taric AI agent, using IL from live game data and RL within `lol_sim_env`.

## Project 1: LoL Simulated Laning Environment (`lol_sim_env`)

**Goal:** To develop a Python-based, OpenAI Gym-compatible **simulated environment** representing a 2v2 League of Legends bot-lane laning phase, suitable for headless RL agent training on cloud GPU platforms. This project will involve writing custom Python code to simulate game mechanics, referencing the LoL Wiki for specific details (e.g., ability effects, minion/turret stats) and drawing conceptual inspiration from older projects for structuring game mechanics logic. The focus is on a new, maintainable Python simulation that allows for configurable game speed to accelerate RL training.

**Proposed Folder Structure:**

Lol_Sim_Env/
├── lol_sim_env_project/             # The installable Python package
│   ├── init.py
│   ├── envs/                # Gym environment definitions
│   │   ├── init.py
│   │   └── taric_laning_sim_env.py  # TaricLaningSimEnv(gymnasium.Env) class
│   ├── game_logic/          # Core simulation components
│   │   ├── init.py
│   │   ├── core/            # Fundamental game elements
│   │   │   ├── init.py
│   │   │   ├── entity.py        # Base class for all game objects (ID, team, position, radius)
│   │   │   ├── game_object.py   # Extends Entity, for objects with stats (HP, Mana, etc.)
│   │   │   ├── map.py           # Lane map representation, boundaries, pathing helpers
│   │   │   └── game_clock.py    # Manages game time, tick rate, game speed multiplier
│   │   ├── units/           # Game units that interact
│   │   │   ├── init.py
│   │   │   ├── champion.py      # Champion class, inherits GameObject, handles abilities, items, base AI logic
│   │   │   ├── taric.py         # Taric-specific logic, inherits Champion (agent controlled)
│   │   │   ├── ally_adc.py      # Scripted ADC ally logic (archetype), inherits Champion
│   │   │   ├── enemy_champion.py # Scripted enemy archetypes (ADC, Support), inherits Champion
│   │   │   ├── minion.py        # Minion class, wave logic, AI, inherits GameObject
│   │   │   └── turret.py        # Turret class, targeting logic, AI, inherits GameObject
│   │   ├── systems/         # Game systems managing interactions
│   │   │   ├── init.py
│   │   │   ├── ability_system.py # Handles ability casting, effects (damage, heal, CC), cooldowns
│   │   │   ├── combat_system.py # Resolves attacks, damage calculation, healing application
│   │   │   ├── movement_system.py# Handles unit movement and simple collision response
│   │   │   ├── gold_system.py     # Manages gold gain (passive, CS, takedowns) and item purchases
│   │   │   ├── experience_system.py# Manages XP gain and champion leveling
│   │   │   └── event_system.py    # (Optional) For queuing/broadcasting discrete game events
│   │   └── game_state.py    # Holds and manages the current state of all entities & game clock, interfaces with systems
│   ├── configs/             # Default configuration files (YAML or Python dicts)
│   │   ├── init.py
│   │   ├── champions/       # Folder for individual champion config files
│   │   │   ├── taric.yaml   # Taric's base stats, ability params (from LoL Wiki)
│   │   │   ├── generic_adc_ally.yaml # Stats & 1-2 conceptual abilities for ally ADC
│   │   │   ├── generic_enemy_adc.yaml  # Stats & 1-2 conceptual abilities for enemy ADC
│   │   │   ├── enemy_poke_support_archetype.yaml # Stats & 1-2 conceptual poke abilities
│   │   │   └── enemy_engage_support_archetype.yaml# Stats & 1-2 conceptual engage abilities
│   │   ├── items/           # Config for items Taric can purchase (stats, cost, components)
│   │   │   ├── components/      # Item components' stats and cost
│   │   │   │   ├── kindlegem.yaml
│   │   │   │   └── bandleglass_mirror.yaml
│   │   │   ├── echoes_of_helia.yaml # Full item stats, cost, build path from components
│   │   │   └── knights_vow.yaml     # Full item stats, cost, build path from components
│   │   ├── minions.yaml       # Stats (per type, per wave/time), types, wave composition, spawn times, aggro rules (conceptual)
│   │   ├── turrets.yaml       # Stats (HP, AD, range, armor, mr), attack logic, targeting priorities (conceptual)
│   │   └── simulation_params.yaml # General sim parameters (lane dimensions, max game time, XP curves, game_speed_multiplier, tick_rate, respawn_timers)
│   └── utils/               # Utility functions
│       ├── init.py
│       ├── constants.py     # Global game constants (e.g., TEAM_BLUE, TEAM_RED, MAX_LEVEL)
│       └── vector_math.py   # For 2D positions, distances, angles, simple geometry
├── examples/                # Example scripts demonstrating environment usage
│   └── run_random_agent.py  # Simple script to test environment with random actions
│   └── run_scripted_agents_test.py # Test with basic scripted AI for all champs
├── tests/                   # Unit tests for game logic and environment components
│   ├── init.py
│   ├── test_game_logic/     # Subfolder for testing individual game logic modules
│   │   ├── test_champion.py
│   │   ├── test_ability_system.py
│   │   └── test_combat_system.py
│   └── test_taric_laning_sim_env.py # Test Gym environment compliance and core mechanics
├── setup.py                 # For packaging the lol_sim_env as an installable library
├── requirements.txt         # Python package dependencies (e.g., numpy, gymnasium, pyyaml)
└── README.md                # Project overview, setup, usage instructions, API reference for env, explicit list of simplifications