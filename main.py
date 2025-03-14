#!/usr/bin/env python3
"""
Solar System Simulation

A 2D simulation of the solar system using Newtonian physics.
This is the main entry point for the application.
"""
import argparse
import sys
from typing import List, Optional

from solarsim.simulation.simulator import Simulator


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Solar System Simulation",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--fps", 
        type=int, 
        default=60,
        help="Frames per second for the simulation"
    )
    
    return parser.parse_args()


def main() -> int:
    """
    Main entry point for the application.
    
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    # Parse command line arguments
    args = parse_arguments()
    
    try:
        # Create and run the simulator
        simulator = Simulator()
        simulator.initialize_solar_system()
        simulator.run(fps=args.fps)
        
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main()) 