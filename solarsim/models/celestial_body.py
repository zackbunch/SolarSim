"""
Celestial body models for the solar system simulation.

This module contains the base CelestialBody class and its subclasses
representing different types of celestial bodies in the solar system.
"""
from typing import List, Tuple, Optional, Sequence
import math

from solarsim.config.constants import G, TIMESTEP, SCALE, WIDTH, HEIGHT, AU


class CelestialBody:
    """
    Base class for all celestial bodies in the solar system.
    
    This class implements the physics of gravitational attraction and orbital mechanics
    for celestial bodies. It also provides methods for rendering the body and its orbit.
    
    Attributes:
        name (str): Name of the celestial body
        x (float): X-coordinate in meters
        y (float): Y-coordinate in meters
        radius (float): Radius of the body for display purposes
        color (Tuple[int, int, int]): RGB color tuple for rendering
        mass (float): Mass of the body in kg
        is_sun (bool): Whether this body is the central star
        x_vel (float): Velocity in x-direction in m/s
        y_vel (float): Velocity in y-direction in m/s
        orbit (List[Tuple[float, float]]): List of previous positions for orbit rendering
        distance_to_sun (float): Current distance to the sun in meters
    """

    def __init__(
        self,
        x: float,
        y: float,
        radius: float,
        color: Tuple[int, int, int],
        mass: float,
        name: str = "Unknown",
        is_sun: bool = False,
        x_vel: float = 0,
        y_vel: float = 0
    ):
        """
        Initialize a celestial body.
        
        Args:
            x: X-coordinate in meters
            y: Y-coordinate in meters
            radius: Radius of the body for display purposes
            color: RGB color tuple for rendering
            mass: Mass of the body in kg
            name: Name of the celestial body
            is_sun: Whether this body is the central star
            x_vel: Initial velocity in x-direction in m/s
            y_vel: Initial velocity in y-direction in m/s
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name
        self.is_sun = is_sun
        self.x_vel = x_vel
        self.y_vel = y_vel
        
        self.orbit: List[Tuple[float, float]] = []
        self.distance_to_sun = 0.0
        self.orbital_period = 0.0  # in Earth days
        self.semi_major_axis = 0.0  # in AU
        self.velocity = 0.0  # in m/s

    def calculate_position(self) -> Tuple[float, float]:
        """
        Calculate the screen position for rendering.
        
        Returns:
            Tuple containing the x and y screen coordinates
        """
        screen_x = self.x * SCALE + WIDTH / 2
        screen_y = self.y * SCALE + HEIGHT / 2
        return screen_x, screen_y

    def calculate_attraction(self, other: 'CelestialBody') -> Tuple[float, float]:
        """
        Calculate the gravitational attraction force between this body and another.
        
        Args:
            other: Another celestial body
            
        Returns:
            Tuple containing the x and y components of the force
        """
        # Calculate distance vector components
        distance_x = other.x - self.x
        distance_y = other.y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        
        # Update distance to sun if the other body is the sun
        if other.is_sun:
            self.distance_to_sun = distance
            
            # Calculate orbital properties if not the sun
            if not self.is_sun:
                self._calculate_orbital_properties()
        
        # Skip if bodies are at the same position (avoid division by zero)
        if distance == 0:
            return 0, 0
            
        # Calculate gravitational force
        force = G * self.mass * other.mass / distance**2
        
        # Calculate force components using angle
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        
        return force_x, force_y
        
    def _calculate_orbital_properties(self) -> None:
        """Calculate orbital properties based on current state."""
        # Calculate current velocity
        self.velocity = math.sqrt(self.x_vel**2 + self.y_vel**2)
        
        # Estimate semi-major axis (simplified for circular orbits)
        self.semi_major_axis = self.distance_to_sun / AU
        
        # Estimate orbital period using Kepler's third law (in Earth days)
        # T^2 ∝ a^3, where T is period and a is semi-major axis
        if self.semi_major_axis > 0:
            # Period in seconds = 2π * sqrt(a^3 / GM)
            period_seconds = 2 * math.pi * math.sqrt(
                (self.distance_to_sun**3) / (G * 1.98892e30)
            )
            # Convert to Earth days
            self.orbital_period = period_seconds / (24 * 3600)

    def update_position(self, bodies: Sequence['CelestialBody']) -> None:
        """
        Update the position of this body based on gravitational forces from all other bodies.
        
        Args:
            bodies: Sequence of all celestial bodies in the simulation
        """
        # Skip position updates for the sun
        if self.is_sun:
            return
            
        # Calculate total force from all other bodies
        total_fx = total_fy = 0
        for body in bodies:
            if self is body:
                continue
                
            fx, fy = self.calculate_attraction(body)
            total_fx += fx
            total_fy += fy
        
        # Update velocity based on acceleration (F = ma)
        self.x_vel += total_fx / self.mass * TIMESTEP
        self.y_vel += total_fy / self.mass * TIMESTEP
        
        # Update position based on velocity
        self.x += self.x_vel * TIMESTEP
        self.y += self.y_vel * TIMESTEP
        
        # Record position for orbit rendering
        self.orbit.append((self.x, self.y))
        
        # Limit orbit history to prevent memory issues
        if len(self.orbit) > 1000:
            self.orbit = self.orbit[-1000:]
            
    def get_info(self) -> dict:
        """
        Get detailed information about this celestial body.
        
        Returns:
            Dictionary containing information about the body
        """
        # Calculate diameter in km (assuming Earth-like density for simplicity)
        # This is just for display purposes, not physically accurate
        diameter_km = 2 * (self.radius / 16) * 12742  # Earth's diameter is ~12,742 km
        
        return {
            "name": self.name,
            "mass": f"{self.mass:.2e} kg",
            "diameter": f"{diameter_km:,.0f} km",
            "distance": f"{self.distance_to_sun / 1000:,.0f} km",
            "velocity": f"{self.velocity / 1000:.2f} km/s",
            "orbital_period": f"{self.orbital_period:.2f} days",
            "semi_major_axis": f"{self.semi_major_axis:.2f} AU"
        }


def create_celestial_body(
    name: str,
    x: float,
    y: float,
    radius: float,
    color: Tuple[int, int, int],
    mass: float,
    is_sun: bool = False,
    y_vel: float = 0
) -> CelestialBody:
    """
    Factory function to create a celestial body with the given parameters.
    
    Args:
        name: Name of the celestial body (for reference)
        x: X-coordinate in meters
        y: Y-coordinate in meters
        radius: Radius of the body for display purposes
        color: RGB color tuple for rendering
        mass: Mass of the body in kg
        is_sun: Whether this body is the central star
        y_vel: Initial velocity in y-direction in m/s
        
    Returns:
        A new CelestialBody instance
    """
    return CelestialBody(
        name=name,
        x=x,
        y=y,
        radius=radius,
        color=color,
        mass=mass,
        is_sun=is_sun,
        y_vel=y_vel
    ) 