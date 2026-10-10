# NeatPong

A comprehensive NEAT (NeuroEvolution of Augmenting Topologies) implementation for training neural networks to play Pong through evolutionary algorithms. This project serves as an educational and research platform for understanding artificial neural networks, reward systems, and decision-making behaviors in reinforcement learning environments.

## Project Motivation

NeatPong was developed to provide hands-on experience with:
- **Neural Network Evolution**: Understanding how artificial neural networks evolve through genetic algorithms
- **Reward System Design**: Exploring how different fitness functions influence learning behavior
- **Decision-Making Analysis**: Observing and analyzing the decision-making processes of evolved agents
- **Behavioral Emergence**: Studying how complex behaviors emerge from simple reward signals
- **NEAT Algorithm Implementation**: Deep dive into the NeuroEvolution of Augmenting Topologies algorithm

## Overview

This project demonstrates how neural networks can learn complex behaviors through genetic evolution, using only weight and topology changes. The modular architecture provides clean separation between training, simulation, and visualization components, making it an excellent platform for studying neural network evolution and behavior.

## Key Features

- **NEAT Algorithm**: Full implementation of NeuroEvolution of Augmenting Topologies for neural network evolution
- **Real-time Training Visualization**: Live dashboard showing training progress with adjustable speed controls
- **Modular Architecture**: Clean separation between training, game simulation, and visualization layers
- **Comprehensive Checkpoint System**: Save and resume training from any point with automatic directory management
- **Advanced Performance Metrics**: Multi-factor fitness evaluation system for comprehensive agent assessment
- **Configurable Parameters**: Separate configuration files for NEAT genetics and game physics
- **Behavioral Analysis Tools**: Real-time observation of agent decision-making and learning patterns
- **Research-Ready Framework**: Designed for experimentation with different fitness functions and parameters

## Project Structure

```
src/neat_pong/
├── config/          # Configuration files for NEAT and game parameters
│   ├── config.txt   # NEAT genetic algorithm settings
│   └── parameters.py # Game physics and training constants
├── game/            # Pong game simulation engine
│   ├── game.py      # Main game loop and state management
│   ├── ball.py      # Ball physics and movement
│   ├── paddle.py    # Paddle mechanics and collision detection
│   └── tracker.py   # Game state tracking and scoring
├── training/        # NEAT training implementation
│   ├── trainer.py   # Main NEAT trainer and population management
│   └── agent.py     # Neural network agent implementation
├── utils/           # Utility functions and controllers
│   └── speed_controller.py # Training speed and visualization controls
└── visualization/   # Real-time training dashboard
    └── dashboard.py # Live training visualization and network display
```

## Core Components Explained

### Main Entry Point (`main.py`)
The orchestrator that handles different execution modes:
- **Train**: Start new training session with optional visualization
- **Continue**: Resume training from checkpoint
- **Test**: Evaluate best trained model
- **Benchmark**: Compare multiple agents

### NEAT Trainer (`src/neat_pong/training/trainer.py`)
The heart of the evolutionary process:
- Manages NEAT population and evolution
- Handles fitness evaluation through game simulations
- Implements checkpoint system for training persistence
- Coordinates between neural networks and game environment

### Game Engine (`src/neat_pong/game/game.py`)
The simulation environment:
- Manages game state and physics
- Handles collision detection and scoring
- Provides normalized inputs for neural networks
- Implements realistic Pong mechanics

### Visualization Dashboard (`src/neat_pong/visualization/dashboard.py`)
Real-time training monitoring:
- Live display of agent performance
- Network topology visualization
- Training statistics and progress tracking
- Interactive speed controls and training management

## Installation

### Prerequisites
- Python 3.7 or higher
- Git

### Setup Instructions
1. Clone the repository:
```bash
git clone https://github.com/Asreonn/NeatPong.git
cd NeatPong
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Verify installation:
```bash
python main.py --help
```

## Usage Guide

### Starting Training
Begin a new training session with live visualization:
```bash
python main.py --mode train --show-training
```

### Resuming Training
Continue from a specific checkpoint:
```bash
python main.py --mode continue --show-training --checkpoint checkpoints/neat-checkpoint-129
```

### Testing Models
Evaluate the best trained agent:
```bash
python main.py --mode test
```

### Benchmarking
Compare multiple agents:
```bash
python main.py --mode benchmark
```

### Command Line Options
```bash
python main.py --mode [train|continue|test|benchmark] [--show-training] [--checkpoint PATH]
```

## Configuration

### NEAT Parameters (`src/neat_pong/config/config.txt`)
Genetic algorithm settings including:
- Population size and mutation rates
- Crossover and selection parameters
- Species threshold and compatibility settings
- Network topology evolution parameters

### Game Parameters (`src/neat_pong/config/parameters.py`)
Simulation constants including:
- Game physics (ball speed, paddle size)
- Training parameters (match duration, fitness weights)
- Neural network input/output specifications

## Training Process

### Fitness Evaluation
Agents are evaluated based on multiple factors:
- **Ball Hitting Accuracy**: Precision of paddle-ball interactions
- **Score Differential**: Point difference between agents
- **Game Duration**: Ability to maintain rallies
- **Match Victory**: Overall game performance

### Evolutionary Process
1. **Initialization**: Random neural network population
2. **Evaluation**: Each agent plays multiple games
3. **Selection**: Best performers are selected for reproduction
4. **Crossover**: Genetic material is combined
5. **Mutation**: Random changes to weights and topology
6. **Speciation**: Networks are grouped by similarity
7. **Repeat**: Process continues until convergence

## Output and Results

### Automatic Directory Creation
- `checkpoints/` - Training checkpoints for resuming sessions
- `models/` - Best performing neural network genomes
- `logs/` - Training logs and performance metrics

### Checkpoint System
- Automatic checkpoint creation every N generations
- Manual checkpoint saving at any time
- Seamless training resumption from any point

## Research Applications

### Neural Network Analysis
- Study how network topology affects learning
- Analyze weight evolution patterns
- Understand feature representation development

### Behavioral Studies
- Observe emergent strategies
- Analyze decision-making patterns
- Study adaptation to different scenarios

### Algorithm Research
- Experiment with different fitness functions
- Test NEAT parameter variations
- Compare with other evolutionary algorithms

## Dependencies

### Core Requirements
- **Python 3.7+**: Modern Python features and performance
- **Pygame**: Game rendering and input handling
- **NEAT-Python**: NEAT algorithm implementation
- **NumPy**: Numerical computations and array operations

### Development Dependencies
- **Matplotlib**: Data visualization and plotting
- **Pandas**: Data analysis and manipulation
- **Jupyter**: Interactive development and analysis

See `requirements.txt` for complete dependency list with versions.

## Performance Considerations

### Training Speed
- Configurable simulation speed for real-time observation
- Batch processing for faster training without visualization
- Optimized game engine for efficient simulation

### Memory Management
- Automatic cleanup of old checkpoints
- Efficient neural network representation
- Optimized data structures for large populations

## Troubleshooting

### Common Issues
1. **Import Errors**: Ensure all dependencies are installed
2. **Performance Issues**: Adjust visualization settings
3. **Training Stagnation**: Modify NEAT parameters
4. **Memory Issues**: Reduce population size or checkpoint frequency

### Getting Help
- Check the configuration files for parameter explanations
- Review the training logs for detailed information
- Adjust visualization settings for better performance

## Contributing

We welcome contributions to improve NeatPong! Please follow these guidelines:

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Code Style
- Follow PEP 8 Python style guidelines
- Add docstrings for new functions
- Include type hints where appropriate
- Write clear commit messages

### Areas for Contribution
- Additional fitness functions
- New visualization features
- Performance optimizations
- Documentation improvements
- Bug fixes and testing

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Asreonn** - [GitHub Profile](https://github.com/Asreonn)

## Acknowledgments

- NEAT algorithm creators: Kenneth O. Stanley and Risto Miikkulainen
- NEAT-Python contributors for the excellent implementation
- Pygame community for the game development framework
- Open source community for inspiration and tools

## Citation

If you use NeatPong in your research, please cite:

```bibtex
@software{neatpong2024,
  title={NeatPong: A NEAT Implementation for Neural Network Evolution in Pong},
  author={Asreonn},
  year={2024},
  url={https://github.com/Asreonn/NeatPong}
}
```

## Future Development

### Planned Features
- Multi-agent training scenarios
- Advanced visualization tools
- Export/import functionality
- Performance benchmarking suite
- Web-based dashboard

### Research Directions
- Alternative fitness functions
- Different game environments
- Hybrid learning approaches
- Real-time adaptation

---

**NeatPong** - Understanding Neural Networks Through Evolution

## Project State

Status: EXPERIMENT
Completion: 50
Last reviewed: 2026-09-22
Family: neat-games
Resume cost: low

### Purpose

NEAT ile Pong oynayan ağ. Git'li ilk commit.

### Current state

README ve src/.

### Missing / unfinished

Eğitilmiş genomun durup durmadığı bakılmadı.

### Next action

README'deki eğitim komutunu tekrarlamadan önce kayıtlı genom var mı bak.

### Important files

Registry id `neat-pong`. Source scan: 17 files, about 998 lines, tests=False.

### Related projects

none

