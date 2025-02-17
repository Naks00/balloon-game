import pygame

# ---------------------------
# Entity Base Class
# ---------------------------
class Entity:
    """Template class for all game entities providing position, collision, and rendering capabilities."""

    def __init__(self, x, y, width, height):
        """Initialize entity with position and dimensions.
        
        Args:
            x (int): X-coordinate position
            y (int): Y-coordinate position
            width (int): Entity width in pixels
            height (int): Entity height in pixels
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    

    def update(self, dt):
        """Abstract method to update entity state. To be overridden by subclasses.
        
        Args:
            dt (float): Delta time in seconds since last frame
        """
        raise NotImplementedError("Subclasses must implement apply method.")

    

    def draw(self, surface):
        """Abstract method to draw an entity on specified surface. To be overridden by subclasses.
        
        Args:
            surface (pygame.Surface): Game display surface
        """
        raise NotImplementedError("Subclasses must implement apply method.")
    
    
    def collides_with(self, other):
        """Check collision with another entity using AABB (Axis-Aligned Bounding Box) detection.
        
        Args:
            other (Entity): Other entity to check collision against
        
        Returns:
            bool: True if collision detected, False otherwise
        """
        return (self.x < other.x + other.width and 
                self.x + self.width > other.x and 
                self.y < other.y + other.height and 
                self.y + self.height > other.y)
