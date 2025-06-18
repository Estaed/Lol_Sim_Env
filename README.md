# LoL Simulated Laning Environment (`lol_sim_env`)

A Python-based, OpenAI Gymnasium-compatible simulated environment representing a 2v2 League of Legends bot-lane laning phase, designed for headless Reinforcement Learning agent training on cloud GPU platforms.

## Project Overview

This project creates a custom, lightweight, and fast Python simulation of the LoL 2v2 laning phase, prioritizing game mechanics over visual fidelity. The environment allows configurable game speed to accelerate RL training and focuses on training AI agents, particularly for playing Taric (Support) in a bot lane scenario.

## Key Features

- **OpenAI Gymnasium Compatible**: Standard RL environment interface
- **Headless Operation**: Runs without GUI dependencies for cloud training
- **Configurable Game Speed**: Accelerate training with time multipliers
- **Realistic Game Mechanics**: Based on League of Legends Wiki data
- **2v2 Bot Lane Focus**: Taric + ADC vs Enemy Support + Enemy ADC
- **Modular Architecture**: Extensible system design

## Target Scenario

- **Duration**: Up to 15 minutes of simulated game time
- **Player-controlled**: Taric (Support) - Full kit (Q, W, E, R)
- **Scripted AI Ally**: Configurable ADC archetype
- **Scripted AI Enemies**: Two configurable enemy archetypes
- **Game Elements**: Minions, Turrets, Items, Gold/XP systems

## Documentation

- **[Project Specification](lol_sim_env.md)**: Complete project requirements, features, and detailed implementation plan
- **[Architecture Overview](Architecture_env.md)**: File structure and architectural design

## Development Status

🚧 **Under Development** - This project is currently in active development following an iterative MVP-first approach.

## Related Projects

This environment is designed to work with the **Taric AI Agent** project, which trains AI agents using a combination of Imitation Learning (from live LoL games) and Reinforcement Learning (using this simulation environment).

---

**Version**: 1.1  
**Last Updated**: June 2025
