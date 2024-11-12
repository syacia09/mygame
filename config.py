import pygame

# Window size (includes side panels)


# Basic Configurations
width = 400
height = 400
scoreboard_height = 25
# window_size = (width, height + scoreboard_height)

# Candy Configurations
candy_colors = ['biru', 'ijo', 'oren', 'mera', 'ungu', 'kuning', 'orenn']
candy_width = 40
candy_height = 40
candy_size = (candy_width, candy_height)
side_panel_width = 100

window_width = width + 2 * side_panel_width
window_height = height + 25  # Extra height for the scoreboard
window_size = (window_width, window_height)

# Screen Setup
pygame.init()
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Candy Crush')

# config.py



