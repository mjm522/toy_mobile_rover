import os
import pygame

class Wall(pygame.sprite.Sprite):
    """
    This class represents the wall.
    It derives from the "Sprite" class in Pygame.
    """
 
    def __init__(self, color, width, height):
        """ Constructor. Pass in the color of the block,
        and its size. """
 
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

class Agent(pygame.sprite.Sprite):
    """
    This class represents the robot.
    It derives from the "Sprite" class in Pygame.
    """
 
    def __init__(self, color, width, height):
        """ Constructor. Pass in the color of the block,
        and its size. """
 
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        robot_img = pygame.image.load(os.environ['TMR_ROOT_DIR']+'/assets/robot_image.jpg').convert()

        # Create a new blank image
        self.image = pygame.Surface([width, height])#.convert()
 
        # Copy the sprite from the large sheet onto the smaller image
        self.image.blit(robot_img, (0,0))
 
        # Assuming black works as the transparent color
        # image.set_colorkey(constants.BLACK)
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        # self._image = pygame.Surface([width, height])
        # self._image.fill(color)
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

    def update(self, x, y, th):
        self.image = pygame.transform.rotate(self.image, th)
        self.rect.x = x
        self.rect.y = y