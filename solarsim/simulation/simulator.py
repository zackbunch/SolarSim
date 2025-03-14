"""
Simulator module for the solar system simulation.

This module contains the main simulation logic for the solar system,
handling the creation of celestial bodies and the simulation loop.
"""
from typing import List, Dict, Any, Optional, Tuple
import pygame

from solarsim.models.celestial_body import CelestialBody, create_celestial_body
from solarsim.rendering.renderer import Renderer, Button
from solarsim.config.constants import (
    PLANET_CONFIGS, WINDOW_TITLE, AU, BUTTON_WIDTH, BUTTON_HEIGHT, 
    BUTTON_MARGIN, CONTROL_PANEL_HEIGHT, BLACK, WHITE, LIGHT_GREY,
    TIME_SPEEDS, DEFAULT_TIME_SPEED_INDEX
)


class Simulator:
    """
    Main simulator class for the solar system simulation.
    
    This class is responsible for creating celestial bodies, running the
    simulation loop, and handling user input.
    """
    
    def __init__(self):
        """Initialize the simulator with default settings."""
        self.running = False
        self.clock = pygame.time.Clock()
        self.bodies: List[CelestialBody] = []
        self.renderer = Renderer(WINDOW_TITLE)
        
        # Time control variables
        self.time_speed_index = DEFAULT_TIME_SPEED_INDEX
        self.paused = False
        
        # UI state
        self.selected_body = None
        
        # Initialize time control buttons
        self._init_time_controls()
        
    def _init_time_controls(self) -> None:
        """Initialize time control buttons."""
        # Create button actions
        def decrease_speed():
            self.time_speed_index = max(0, self.time_speed_index - 1)
            
        def increase_speed():
            self.time_speed_index = min(len(TIME_SPEEDS) - 1, self.time_speed_index + 1)
            
        def toggle_pause():
            self.paused = not self.paused
            
        # Create buttons
        button_y = CONTROL_PANEL_HEIGHT // 2 - BUTTON_HEIGHT // 2
        
        # Slower button
        slower_button = Button(
            x=BUTTON_MARGIN,
            y=button_y,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            text="Slower",
            color=BLACK,
            hover_color=LIGHT_GREY,
            text_color=WHITE,
            font=self.renderer.info_font,
            action=decrease_speed
        )
        
        # Pause/Play button
        pause_button = Button(
            x=BUTTON_MARGIN * 2 + BUTTON_WIDTH,
            y=button_y,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            text="Pause",
            color=BLACK,
            hover_color=LIGHT_GREY,
            text_color=WHITE,
            font=self.renderer.info_font,
            action=toggle_pause
        )
        
        # Faster button
        faster_button = Button(
            x=BUTTON_MARGIN * 3 + BUTTON_WIDTH * 2,
            y=button_y,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            text="Faster",
            color=BLACK,
            hover_color=LIGHT_GREY,
            text_color=WHITE,
            font=self.renderer.info_font,
            action=increase_speed
        )
        
        # Add buttons to renderer
        self.buttons = [slower_button, pause_button, faster_button]
        
    def initialize_solar_system(self) -> None:
        """
        Initialize the solar system with default planets.
        
        Creates the sun and planets based on configuration values.
        """
        self.bodies = []
        
        # Create celestial bodies from configuration
        for name, config in PLANET_CONFIGS.items():
            body = create_celestial_body(
                name=name,
                x=config["x"],
                y=config["y"],
                radius=config["radius"],
                color=config["color"],
                mass=config["mass"],
                is_sun=config["is_sun"],
                y_vel=config["y_vel"]
            )
            self.bodies.append(body)
    
    def handle_events(self) -> bool:
        """
        Handle pygame events.
        
        Returns:
            Boolean indicating whether the simulation should continue running
        """
        mouse_pos = pygame.mouse.get_pos()
        
        # Update button hover states
        for button in self.buttons:
            button.update(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            # Handle button clicks
            for button in self.buttons:
                if button.handle_event(event):
                    # Update pause button text
                    if button.text in ["Pause", "Play"]:
                        button.text = "Play" if self.paused else "Pause"
                    break
            
            # Handle planet selection
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked_body = self.renderer.check_body_clicked(event.pos, self.bodies)
                if clicked_body:
                    self.selected_body = clicked_body
                elif self.selected_body and event.pos[1] > CONTROL_PANEL_HEIGHT:
                    # Deselect if clicking empty space below control panel
                    self.selected_body = None
                
        return True
    
    def update(self) -> None:
        """Update the positions of all celestial bodies."""
        # Skip updates if paused
        if self.paused:
            return
            
        # Apply time speed multiplier
        time_multiplier = TIME_SPEEDS[self.time_speed_index]
        
        # Skip updates if speed is 0
        if time_multiplier == 0:
            return
            
        # Update multiple times for faster speeds
        update_count = 1
        if time_multiplier > 1:
            update_count = int(time_multiplier)
            
        for _ in range(update_count):
            for body in self.bodies:
                body.update_position(self.bodies)
    
    def render(self) -> None:
        """Render the current state of the simulation."""
        self.renderer.clear_screen()
        
        # Render celestial bodies
        self.renderer.render_bodies(self.bodies)
        
        # Render UI elements
        self._render_ui()
        
        self.renderer.update_display()
    
    def _render_ui(self) -> None:
        """Render UI elements."""
        # Render time controls
        self.renderer.render_time_controls(self.time_speed_index)
        
        # Render time control buttons
        for button in self.buttons:
            button.draw(self.renderer.transparent_surface)
            
        # Render info panel if a body is selected
        self.renderer.render_info_panel(self.selected_body)
    
    def run(self, fps: int = 60) -> None:
        """
        Run the main simulation loop.
        
        Args:
            fps: Frames per second for the simulation
        """
        self.running = True
        
        # Initialize solar system if not already done
        if not self.bodies:
            self.initialize_solar_system()
        
        # Main simulation loop
        while self.running:
            # Limit frame rate
            self.clock.tick(fps)
            
            # Handle events
            self.running = self.handle_events()
            
            # Update simulation state
            self.update()
            
            # Render current state
            self.render()
        
        # Clean up
        pygame.quit()
    
    def add_body(self, 
                name: str,
                x: float, 
                y: float, 
                radius: float, 
                color: tuple, 
                mass: float, 
                is_sun: bool = False, 
                y_vel: float = 0) -> None:
        """
        Add a custom celestial body to the simulation.
        
        Args:
            name: Name of the celestial body
            x: X-coordinate in meters
            y: Y-coordinate in meters
            radius: Radius for display
            color: RGB color tuple
            mass: Mass in kg
            is_sun: Whether this body is a sun
            y_vel: Initial y-velocity in m/s
        """
        body = create_celestial_body(
            name=name,
            x=x,
            y=y,
            radius=radius,
            color=color,
            mass=mass,
            is_sun=is_sun,
            y_vel=y_vel
        )
        self.bodies.append(body) 