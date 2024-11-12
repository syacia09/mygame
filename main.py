# main.py
import pygame
from pygame.locals import *
from config import screen, width, height, scoreboard_height, candy_width, candy_height, side_panel_width, window_width
from statistics import score, moves, update_score, increment_moves
from candy import Candy, swap, match_three

pygame.init()

left_image = pygame.image.load("genie_left.png")
right_image = pygame.image.load("genie_right.png")

original_left_width, original_left_height = left_image.get_size()
original_right_width, original_right_height = right_image.get_size()

left_image_height = int(original_left_height * (side_panel_width / original_left_width))
right_image_height = int(original_right_height * (side_panel_width / original_right_width))

left_image = pygame.transform.smoothscale(left_image, (side_panel_width, left_image_height))
right_image = pygame.transform.smoothscale(right_image, (side_panel_width, right_image_height))

screen.blit(left_image, (0, 0))
screen.blit(right_image, (window_width - side_panel_width, 0))
left_image = pygame.image.load("genie_left.png")
right_image = pygame.image.load("genie_right.png")

original_left_width, original_left_height = left_image.get_size()
original_right_width, original_right_height = right_image.get_size()

left_image_height = int(original_left_height * (side_panel_width / original_left_width))
right_image_height = int(original_right_height * (side_panel_width / original_right_width))

left_image = pygame.transform.smoothscale(left_image, (side_panel_width, left_image_height))
right_image = pygame.transform.smoothscale(right_image, (side_panel_width, right_image_height))

screen.blit(left_image, (0, 0))
screen.blit(right_image, (window_width - side_panel_width, 0))

available_width = window_width - 2 * side_panel_width

num_candy_cols = available_width // candy_width

board_x = side_panel_width + (available_width - num_candy_cols * candy_width) // 2

board = [[Candy(row_num, col_num) for col_num in range(num_candy_cols)] for row_num in range(height // candy_height)]
# board = [[Candy(row_num, col_num) for col_num in range(width // candy_width)] for row_num in range(height // candy_height)]

def shrink_candies(matches):
    global score
    update_score(len(matches))
    
    while len(matches) > 0:
        clock.tick(100)
        
        for candy in matches:
            new_width = max(0, candy.image.get_width() - 1)
            new_height = max(0, candy.image.get_height() - 1)
            new_size = (new_width, new_height)
            candy.image = pygame.transform.smoothscale(candy.image, new_size)
            candy.rect.left = candy.col_num * candy_width + (candy_width - new_width) / 2
            candy.rect.top = candy.row_num * candy_height + (candy_height - new_height) / 2

        for row_num in range(len(board)):
            for col_num in range(len(board[row_num])):
                candy = board[row_num][col_num]
                if candy.image.get_width() <= 0 or candy.image.get_height() <= 0:
                    matches.remove(candy)
                    board[row_num][col_num] = Candy(row_num, col_num)

        draw()
        pygame.display.update()
        clock.tick(100)

def draw():
    screen.fill((173, 216, 230))

    screen.blit(left_image, (0, 230))
    screen.blit(right_image, (window_width - side_panel_width, 230))

    for row in board:
        for candy in row:
            candy.rect.x = board_x + candy.col_num * candy_width
            candy.draw()
    font = pygame.font.SysFont('monoface', 18)
    score_text = font.render(f'Score = {score}', 1, (0, 0, 0))
    moves_text = font.render(f'Moves = {moves}', 1, (0, 0, 0))
    screen.blit(score_text, score_text.get_rect(center=(width / 4 + 50, height + scoreboard_height / 2)))
    screen.blit(moves_text, moves_text.get_rect(center=(width * 3 / 4 + 150, height + scoreboard_height / 2)))

clicked_candy = None
swapped_candy = None
click_x, click_y = None, None
clock = pygame.time.Clock()
running = True

while running:
    matches = set()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if clicked_candy is None and event.type == MOUSEBUTTONDOWN:
            for row in board:
                for candy in row:
                    if candy.rect.collidepoint(event.pos):
                        clicked_candy = candy
                        #simpen koor candy yang diklik
                        click_x = event.pos[0]
                        click_y = event.pos[1]

        if clicked_candy is not None and event.type == MOUSEMOTION:
            distance_x = abs(click_x - event.pos[0])
            distance_y = abs(click_y - event.pos[1])

            if swapped_candy is not None:
                swapped_candy.snap()
            if distance_x>distance_y and click_x > event.pos[0]:
                direction = 'left'
            elif distance_x>distance_y and click_x < event.pos[0]:
                direction = 'right'
            elif distance_y>distance_x and click_y > event.pos[1]:
                direction ='up'
            else:
                direction='down'

            if direction in ['left','right']:
                clicked_candy.snap_row()
            else:
                clicked_candy.snap_col()

            if direction == 'left' and clicked_candy.col_num > 0:
                swapped_candy = board[clicked_candy.row_num][clicked_candy.col_num-1]

                clicked_candy.rect.left = clicked_candy.col_num * candy_width - distance_x
                swapped_candy.rect.left = swapped_candy.col_num * candy_width + distance_x

                if clicked_candy.rect.left <= swapped_candy.col_num * candy_width + candy_width / 4:
                    swap(clicked_candy, swapped_candy, board)
                    matches.update(match_three(clicked_candy, board))
                    matches.update(match_three(swapped_candy, board))
                    moves += 1
                    clicked_candy = None
                    swapped_candy = None

            if direction == 'right' and clicked_candy.col_num < width / candy_width - 1:
                swapped_candy = board[clicked_candy.row_num][clicked_candy.col_num + 1]

                clicked_candy.rect.left = clicked_candy.col_num * candy_width + distance_x
                swapped_candy.rect.left = swapped_candy.col_num * candy_width - distance_x

                if clicked_candy.rect.left >= swapped_candy.col_num * candy_width - candy_width / 4:
                    swap(clicked_candy, swapped_candy, board)
                    matches.update(match_three(clicked_candy, board))
                    matches.update(match_three(swapped_candy, board))
                    moves += 1
                    clicked_candy = None
                    swapped_candy = None
            
            if direction == 'up' and clicked_candy.row_num > 0:
                swapped_candy = board[clicked_candy.row_num-1][clicked_candy.col_num ]

                clicked_candy.rect.top = clicked_candy.row_num * candy_height - distance_y
                swapped_candy.rect.top = swapped_candy.row_num * candy_height + distance_y

                if clicked_candy.rect.top <= swapped_candy.row_num * candy_height + candy_height / 4:
                    swap(clicked_candy, swapped_candy, board)
                    matches.update(match_three(clicked_candy, board))
                    matches.update(match_three(swapped_candy, board))
                    moves += 1
                    clicked_candy = None
                    swapped_candy = None
            
            if direction == 'down' and clicked_candy.row_num < height / candy_height - 1:
                swapped_candy = board[clicked_candy.row_num + 1][clicked_candy.col_num]

                clicked_candy.rect.top = clicked_candy.row_num * candy_height + distance_y
                swapped_candy.rect.top = swapped_candy.row_num * candy_height - distance_y

                if clicked_candy.rect.top >= swapped_candy.row_num * candy_height - candy_height / 4:
                    swap(clicked_candy, swapped_candy, board)
                    matches.update(match_three(clicked_candy, board))
                    matches.update(match_three(swapped_candy, board))
                    moves += 1
                    clicked_candy = None
                    swapped_candy = None

        if clicked_candy is not None and event.type == MOUSEBUTTONUP:
            #balikan candy ke asal
            clicked_candy.snap()
            clicked_candy = None
            if swapped_candy is not None:
                swapped_candy.snap()
                swapped_candy = None

    if len(matches) >= 3:
        update_score(len(matches))
        score += len(matches)
        shrink_candies(matches)
        matches.clear()

    draw()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
