import pygame
import random
from config import candy_colors, candy_width, candy_height, screen, candy_size
from statistics import update_score

class Candy:
    def __init__(self, row_num, col_num):
        self.row_num = row_num
        self.col_num = col_num
        self.color = random.choice(candy_colors)
        image_name = f'{self.color}.png'
        self.image = pygame.image.load(image_name)
        self.image = pygame.transform.smoothscale(self.image, candy_size)
        self.rect = self.image.get_rect()
        self.rect.left = col_num * candy_width
        self.rect.top = row_num * candy_height

    def draw(self):
        screen.blit(self.image, self.rect)

    def snap(self):
        self.snap_row()
        self.snap_col()

    def snap_row(self):
        self.rect.top = self.row_num * candy_height

    def snap_col(self):
        self.rect.left = self.col_num * candy_width

def swap(candy1, candy2, board):
    temp_row = candy1.row_num
    temp_col = candy1.col_num
    candy1.row_num = candy2.row_num
    candy1.col_num = candy2.col_num
    candy2.row_num = temp_row
    candy2.col_num = temp_col
    board[candy1.row_num][candy1.col_num] = candy1
    board[candy2.row_num][candy2.col_num] = candy2
    candy1.snap()
    candy2.snap()

def find_matches(candy, matches, board):
    matches.add(candy)
    if candy.row_num > 0:
        neighbor = board[candy.row_num - 1][candy.col_num]
        if candy.color == neighbor.color and neighbor not in matches:
            matches.update(find_matches(neighbor, matches, board))
    if candy.row_num < len(board) - 1:
        neighbor = board[candy.row_num + 1][candy.col_num]
        if candy.color == neighbor.color and neighbor not in matches:
            matches.update(find_matches(neighbor, matches, board))
    if candy.col_num > 0:
        neighbor = board[candy.row_num][candy.col_num - 1]
        if candy.color == neighbor.color and neighbor not in matches:
            matches.update(find_matches(neighbor, matches, board))
    if candy.col_num < len(board[0]) - 1:
        neighbor = board[candy.row_num][candy.col_num + 1]
        if candy.color == neighbor.color and neighbor not in matches:
            matches.update(find_matches(neighbor, matches, board))
    return matches

def match_three(candy, board):
    matches = find_matches(candy, set(), board)
    if len(matches) >= 3:
        return matches
    return set()
