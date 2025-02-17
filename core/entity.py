import pygame

# ---------------------------
# Entity Base Class
# ---------------------------
class Entity:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def update(self, dt):
        """Update entity state. dt is delta time in seconds."""
        pass
    
    def draw(self, surface):
        """Draw entity on the given surface."""
        pass
    
    def collides_with(self, other):
        return (self.x < other.x + other.width and 
                self.x + self.width > other.x and 
                self.y < other.y + other.height and 
                self.y + self.height > other.y)
