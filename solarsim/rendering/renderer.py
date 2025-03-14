"""
Rendering module for the solar system simulation.

This module handles all drawing operations for the simulation,
including celestial bodies and their orbits.
"""
from typing import List, Tuple, Optional, Dict, Any, Callable
import pygame

from solarsim.models.celestial_body import CelestialBody
from solarsim.config.constants import (
    WIDTH, HEIGHT, BLACK, WHITE, FONT_NAME, FONT_SIZE, SCALE,
    BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_MARGIN, CONTROL_PANEL_HEIGHT,
    INFO_PANEL_WIDTH, INFO_PANEL_HEIGHT, INFO_PANEL_MARGIN, INFO_TEXT_MARGIN,
    INFO_LINE_HEIGHT, LIGHT_GREY, TRANSPARENT_BLACK, TITLE_FONT_SIZE, INFO_FONT_SIZE,
    TIME_SPEEDS
)


class Button:
    """
    A clickable button for the UI.
    
    This class represents a button that can be clicked to trigger an action.
    """
    
    def __init__(
        self, 
        x: int, 
        y: int, 
        width: int, 
        height: int, 
        text: str, 
        color: Tuple[int, int, int],
        hover_color: Tuple[int, int, int],
        text_color: Tuple[int, int, int],
        font: pygame.font.Font,
        action: Callable[[], None]
    ):
        """
        Initialize a button.
        
        Args:
            x: X-coordinate of the button
            y: Y-coordinate of the button
            width: Width of the button
            height: Height of the button
            text: Text to display on the button
            color: Background color of the button
            hover_color: Background color when hovering
            text_color: Color of the button text
            font: Font for the button text
            action: Function to call when the button is clicked
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = font
        self.action = action
        self.hovered = False
        
    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the button on the given surface.
        
        Args:
            surface: Surface to draw on
        """
        # Draw button background
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, self.text_color, self.rect, width=2, border_radius=5)
        
        # Draw button text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Update the button state based on mouse position.
        
        Args:
            mouse_pos: Current mouse position
        """
        self.hovered = self.rect.collidepoint(mouse_pos)
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse events for the button.
        
        Args:
            event: Pygame event to handle
            
        Returns:
            True if the button was clicked, False otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()
                return True
        return False


class Renderer:
    """
    Handles all rendering operations for the solar system simulation.
    
    This class is responsible for initializing the display window and
    rendering celestial bodies and their orbits.
    """
    
    def __init__(self, window_title: str):
        """
        Initialize the renderer.
        
        Args:
            window_title: Title for the simulation window
        """
        # Initialize pygame if not already done
        if not pygame.get_init():
            pygame.init()
            
        # Create the display window
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(window_title)
        
        # Initialize fonts
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.title_font = pygame.font.SysFont(FONT_NAME, TITLE_FONT_SIZE)
        self.info_font = pygame.font.SysFont(FONT_NAME, INFO_FONT_SIZE)
        
        # Initialize UI elements
        self.buttons = []
        self.selected_body = None
        self.time_speed_index = 2  # Default to normal speed (1.0x)
        
        # Create transparent surface for panels
        self.transparent_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    def clear_screen(self) -> None:
        """Clear the screen with black background."""
        self.window.fill(BLACK)
        self.transparent_surface.fill((0, 0, 0, 0))  # Clear transparent surface
    
    def render_body(self, body: CelestialBody) -> None:
        """
        Render a celestial body and its orbit.
        
        Args:
            body: The celestial body to render
        """
        # Get screen position
        x, y = body.calculate_position()
        
        # Render orbit if there are enough points
        if len(body.orbit) > 2:
            # Convert orbit points to screen coordinates
            updated_points = []
            for point in body.orbit:
                orbit_x, orbit_y = point
                screen_x = orbit_x * SCALE + WIDTH / 2
                screen_y = orbit_y * SCALE + HEIGHT / 2
                updated_points.append((screen_x, screen_y))
            
            # Draw orbit line
            pygame.draw.lines(self.window, body.color, False, updated_points, 2)
        
        # Draw the celestial body
        pygame.draw.circle(self.window, body.color, (int(x), int(y)), body.radius)
        
        # Draw selection indicator if this body is selected
        if self.selected_body is body:
            pygame.draw.circle(self.window, WHITE, (int(x), int(y)), body.radius + 5, 2)
        
        # Render distance text for non-sun bodies
        if not body.is_sun and body.distance_to_sun > 0:
            self._render_distance_text(body, x, y)
    
    def _render_distance_text(self, body: CelestialBody, x: float, y: float) -> None:
        """
        Render the distance text for a celestial body.
        
        Args:
            body: The celestial body
            x: Screen x-coordinate
            y: Screen y-coordinate
        """
        # Create distance text
        distance_text = self.font.render(
            f"{round(body.distance_to_sun/1000, 1)}km", 
            True, 
            WHITE
        )
        
        # Position text centered on the body
        text_x = x - distance_text.get_width() / 2
        text_y = y - distance_text.get_height() / 2
        
        # Draw text
        self.window.blit(distance_text, (text_x, text_y))
    
    def render_time_controls(self, time_speed_index: int) -> None:
        """
        Render time control buttons.
        
        Args:
            time_speed_index: Index of the current time speed
        """
        # Store the current time speed index
        self.time_speed_index = time_speed_index
        
        # Create control panel background
        pygame.draw.rect(
            self.transparent_surface, 
            TRANSPARENT_BLACK, 
            (0, 0, WIDTH, CONTROL_PANEL_HEIGHT)
        )
        
        # Draw time speed text
        speed_text = f"Time Speed: {TIME_SPEEDS[time_speed_index]}x"
        text_surface = self.info_font.render(speed_text, True, WHITE)
        self.transparent_surface.blit(
            text_surface, 
            (WIDTH // 2 - text_surface.get_width() // 2, 10)
        )
        
        # Blit transparent surface to window
        self.window.blit(self.transparent_surface, (0, 0))
    
    def render_info_panel(self, body: Optional[CelestialBody]) -> None:
        """
        Render information panel for the selected celestial body.
        
        Args:
            body: The selected celestial body, or None if no body is selected
        """
        # Store the selected body
        self.selected_body = body
        
        # If no body is selected, don't render the panel
        if body is None:
            return
            
        # Get body information
        info = body.get_info()
        
        # Create panel background
        panel_x = WIDTH - INFO_PANEL_WIDTH - INFO_PANEL_MARGIN
        panel_y = INFO_PANEL_MARGIN
        
        pygame.draw.rect(
            self.transparent_surface,
            TRANSPARENT_BLACK,
            (panel_x, panel_y, INFO_PANEL_WIDTH, INFO_PANEL_HEIGHT),
            border_radius=10
        )
        
        # Draw panel border
        pygame.draw.rect(
            self.transparent_surface,
            WHITE,
            (panel_x, panel_y, INFO_PANEL_WIDTH, INFO_PANEL_HEIGHT),
            width=2,
            border_radius=10
        )
        
        # Draw title
        title_surface = self.title_font.render(info["name"], True, WHITE)
        title_x = panel_x + (INFO_PANEL_WIDTH - title_surface.get_width()) // 2
        title_y = panel_y + INFO_TEXT_MARGIN
        self.transparent_surface.blit(title_surface, (title_x, title_y))
        
        # Draw information lines
        y_offset = title_y + title_surface.get_height() + INFO_TEXT_MARGIN
        
        # Information to display (excluding name which is already in the title)
        display_info = [
            ("Mass", info["mass"]),
            ("Diameter", info["diameter"]),
            ("Distance from Sun", info["distance"]),
            ("Velocity", info["velocity"]),
            ("Orbital Period", info["orbital_period"]),
            ("Semi-Major Axis", info["semi_major_axis"])
        ]
        
        for label, value in display_info:
            # Skip orbital information for the sun
            if body.is_sun and label in ["Distance from Sun", "Velocity", "Orbital Period", "Semi-Major Axis"]:
                continue
                
            text = f"{label}: {value}"
            text_surface = self.info_font.render(text, True, WHITE)
            self.transparent_surface.blit(
                text_surface, 
                (panel_x + INFO_TEXT_MARGIN, y_offset)
            )
            y_offset += INFO_LINE_HEIGHT
        
        # Blit transparent surface to window
        self.window.blit(self.transparent_surface, (0, 0))
    
    def update_display(self) -> None:
        """Update the display to show rendered content."""
        pygame.display.update()
    
    def render_bodies(self, bodies: List[CelestialBody]) -> None:
        """
        Render all celestial bodies in the simulation.
        
        Args:
            bodies: List of celestial bodies to render
        """
        for body in bodies:
            self.render_body(body)
    
    def check_body_clicked(self, pos: Tuple[int, int], bodies: List[CelestialBody]) -> Optional[CelestialBody]:
        """
        Check if a celestial body was clicked.
        
        Args:
            pos: Mouse position
            bodies: List of celestial bodies
            
        Returns:
            The clicked body, or None if no body was clicked
        """
        for body in bodies:
            screen_x, screen_y = body.calculate_position()
            distance = ((pos[0] - screen_x) ** 2 + (pos[1] - screen_y) ** 2) ** 0.5
            
            if distance <= body.radius:
                return body
                
        return None 