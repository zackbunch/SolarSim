# Solar System Simulation

A 2D simulation of the solar system using Newtonian physics. This project simulates the motion of planets around the sun using gravitational forces.

## Features

- Accurate simulation of gravitational forces between celestial bodies
- Visual representation of planets and their orbits
- Real-time display of distances between planets and the sun
- Configurable simulation parameters
- Time controls (pause, slow down, speed up)
- Planet information panel with detailed orbital data

## Requirements

- Python 3.7+
- Pygame

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/zackbunch/SolarSim.git
   cd SolarSim
   ```

2. Install the required dependencies:
   ```
   pip install pygame
   ```

## Usage

Run the simulation with default settings:

```
python main.py
```

### Command Line Options

- `--fps`: Set the frames per second for the simulation (default: 60)

Example:
```
python main.py --fps 30
```

### Controls

- **Click on a planet**: Select it to view detailed information
- **Click on empty space**: Deselect the current planet
- **Pause/Play button**: Toggle simulation pause
- **Slower button**: Decrease simulation speed
- **Faster button**: Increase simulation speed

## Project Structure

```
SolarSim/
├── main.py                     # Main entry point
├── solarsim/                   # Main package
│   ├── config/                 # Configuration
│   │   ├── constants.py        # Constants and settings
│   ├── models/                 # Data models
│   │   ├── celestial_body.py   # Celestial body class
│   ├── rendering/              # Rendering logic
│   │   ├── renderer.py         # Renderer class
│   ├── simulation/             # Simulation logic
│   │   ├── simulator.py        # Main simulator class
├── README.md                   # This file
└── LICENSE                     # License information
```

## Customization

You can customize the simulation by modifying the constants in `solarsim/config/constants.py`:

- Change the scale factor to zoom in or out
- Adjust the time step to speed up or slow down the simulation
- Modify planet properties (mass, radius, color, initial position, velocity)
- Add new planets or other celestial bodies
- Adjust UI settings and appearance

## How It Works

The simulation uses Newton's law of universal gravitation to calculate the forces between celestial bodies:

F = G * (m1 * m2) / r²

Where:
- F is the gravitational force between two bodies
- G is the gravitational constant
- m1 and m2 are the masses of the two bodies
- r is the distance between the centers of the two bodies

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by various physics simulations and educational tools
- Planet data based on real astronomical measurements
