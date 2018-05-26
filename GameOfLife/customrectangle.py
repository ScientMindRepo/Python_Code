import pygame
from pygame import Rect


class CustomRect:

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 175)

    def __init__(self, bounds, bg_color):

        # Attributes
        self.custom_surface_default = pygame.Surface((bounds.w, bounds.h))
        self.custom_surface_default = self.custom_surface_default.convert()
        self.x = bounds.x
        self.y = bounds.y
        self.width = bounds.w
        self.height = bounds.h
        self.custom_surface_default.fill(bg_color)
        self.current_surface = self.custom_surface_default    # property used to act on current state
        self.id = [self.x, self.y]    # default id = list of top left coordinates of CurtomRect
        self.state = 0    # default state value

    def get_current_surface(self):
        return self.current_surface

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def get_id(self):
        return self.id

    def set_id(self, tag_list):
        self.id = tag_list

    def set_surface_label(self, bounds, font_size=20, font_color=BLACK, text='Button', surface=None):
        label_font = pygame.font.SysFont('Roboto', font_size)
        texture_surface = label_font.render(text, True, font_color)
        texture_rectangle = (bounds.x, bounds.y, bounds.width, bounds.height)
        surface.blit(texture_surface, texture_rectangle)

    def draw_custom_rect(self, position, surface=None):
        r = self.current_surface.get_rect()
        r.topleft = position
        surface.blit(self.current_surface, r)

    def update_state(self, color, surface=None):
        rect_surface = self.get_current_surface()
        rect_surface.fill(color)
        position = (self.x, self.y, self.width, self.height)

        surface.blit(rect_surface, position)
