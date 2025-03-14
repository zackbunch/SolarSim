"""
Constants and configuration values for the Solar System Simulation.

This module centralizes all configuration values used throughout the application.
"""
from typing import Tuple, Dict, Any

# Physics constants
AU = 149.6e6 * 1000  # Astronomical Unit in meters
G = 6.67428e-11      # Gravitational constant
TIMESTEP = 3600 * 24  # Simulation timestep (1 day in seconds)

# Display settings
WIDTH = 800           # Window width in pixels
HEIGHT = 800          # Window height in pixels
SCALE = 250 / AU      # Scale factor for display (1 AU = 250 pixels)
WINDOW_TITLE = "Solar System Simulation"
FONT_NAME = "comicsans"
FONT_SIZE = 16
TITLE_FONT_SIZE = 24
INFO_FONT_SIZE = 18

# Colors (R, G, B)
BLACK: Tuple[int, int, int] = (0, 0, 0)
WHITE: Tuple[int, int, int] = (255, 255, 255)
YELLOW: Tuple[int, int, int] = (255, 255, 0)
BLUE: Tuple[int, int, int] = (100, 149, 237)
RED: Tuple[int, int, int] = (188, 39, 50)
DARK_GREY: Tuple[int, int, int] = (80, 78, 81)
ORANGE: Tuple[int, int, int] = (255, 165, 0)
LIGHT_GREY: Tuple[int, int, int] = (200, 200, 200)
TRANSPARENT_BLACK: Tuple[int, int, int, int] = (0, 0, 0, 180)  # RGBA with alpha

# UI settings
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 10
CONTROL_PANEL_HEIGHT = 60
INFO_PANEL_WIDTH = 300
INFO_PANEL_HEIGHT = 300
INFO_PANEL_MARGIN = 20
INFO_TEXT_MARGIN = 10
INFO_LINE_HEIGHT = 25

# Time control settings
TIME_SPEEDS = [0.0, 0.5, 1.0, 2.0, 5.0]  # Multipliers for simulation speed
DEFAULT_TIME_SPEED_INDEX = 2  # Index of default speed (1.0)

# Planet configurations
PLANET_CONFIGS: Dict[str, Dict[str, Any]] = {
    "sun": {
        "x": 0,
        "y": 0,
        "radius": 30,
        "color": YELLOW,
        "mass": 1.98892e30,
        "is_sun": True,
        "y_vel": 0
    },
    "mercury": {
        "x": 0.387 * AU,
        "y": 0,
        "radius": 8,
        "color": DARK_GREY,
        "mass": 3.30e23,
        "is_sun": False,
        "y_vel": -47.4 * 1000
    },
    "venus": {
        "x": 0.723 * AU,
        "y": 0,
        "radius": 14,
        "color": WHITE,
        "mass": 4.8685e24,
        "is_sun": False,
        "y_vel": -35.02 * 1000
    },
    "earth": {
        "x": -1 * AU,
        "y": 0,
        "radius": 16,
        "color": BLUE,
        "mass": 5.9742e24,
        "is_sun": False,
        "y_vel": 29.783 * 1000
    },
    "mars": {
        "x": -1.524 * AU,
        "y": 0,
        "radius": 12,
        "color": RED,
        "mass": 6.39e23,
        "is_sun": False,
        "y_vel": 24.077 * 1000
    }
} 