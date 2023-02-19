import sys
import pygame


WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
GRAY = [190, 190, 190]

block_size = 40
left_margin = 300
upper_margin = 80
size = (30*block_size, 15*block_size)

pygame.init()

screen = pygame.display.set_mode(size)
pygame.display.set_caption('block_battle')

horizontal_list = []
vertical_list = []
top_diag_list = []
bottom_diag_list = []
line_status = 0

active_line_list = []


def draw_line():
    for y in range(upper_margin, upper_margin + 11 * block_size, block_size):
        for x in range(left_margin, left_margin + 11 * block_size, block_size):
            if y < 480 and x < 700:
                horizontal_line = pygame.draw.line(screen, GRAY, (x, y), (x + block_size, y), 3)
                vertical_line = pygame.draw.line(screen, GRAY, (x, y), (x, y + block_size), 3)
                top_diag_line = pygame.draw.line(screen, GRAY, (x, y), (x + block_size, y + block_size), 1)
                bottom_diag_line = pygame.draw.line(screen, GRAY, (x, y + block_size), (x + block_size, y), 1)

                horizontal_list.append(horizontal_line)
                vertical_list.append(vertical_line)
                top_diag_list.append(top_diag_line)
                bottom_diag_list.append(bottom_diag_line)

            if y == (upper_margin + 10 * block_size) and x < (left_margin + 10 * block_size):
                horizontal_line = pygame.draw.line(screen, GRAY, (x, y), (x + block_size, y), 3)
                horizontal_list.append(horizontal_line)

            if x == (left_margin + 10 * block_size) and y < (upper_margin + 10 * block_size):
                vertical_line = pygame.draw.line(screen, GRAY, (x, y), (x, y + block_size), 3)
                vertical_list.append(vertical_line)

    # print(horizontal_list)
    # print(vertical_list)
    # print(hor_line_coor)


def line_activate(x, y):
    horizontal_line_status = [[el, line_status] for el in horizontal_list]
    vertical_line_status = [[el, line_status] for el in vertical_list]
    top_diag_line_status = [[el, line_status] for el in top_diag_list]
    bottom_diag_line_status = [[el, line_status] for el in bottom_diag_list]

    for hor_line in horizontal_line_status:
        if pygame.Rect.collidepoint(hor_line[0], x, y):
            hor_line[1] = 1
            start_pose = (hor_line[0][0], hor_line[0][1]+1)
            end_pose = (hor_line[0][0] + block_size, hor_line[0][1]+1)

            active_line_list.append(pygame.draw.line(screen, BLACK, (start_pose[0], start_pose[1]), (end_pose[0], end_pose[1]), 3))

    for ver_line in vertical_line_status:
        if pygame.Rect.collidepoint(ver_line[0], x, y):
            ver_line[1] = 1
            start_pose = (ver_line[0][0]+1, ver_line[0][1])
            end_pose = (ver_line[0][0]+1, ver_line[0][1] + block_size)
            active_line_list.append(pygame.draw.line(screen, BLACK, (start_pose[0], start_pose[1]), (end_pose[0], end_pose[1]), 3))

    # for top_diag_line in top_diag_line_status:
    #     if pygame.Rect.collidepoint(top_diag_line[0], x, y):
    #         top_diag_line[1] = 1
    #         # print(top_diag_line)
    #         start_pose = (top_diag_line[0][0], top_diag_line[0][1])
    #         end_pose = (top_diag_line[0][0] + block_size, top_diag_line[0][1] + block_size)
    #         pygame.draw.line(screen, BLACK, (start_pose[0], start_pose[1]), (end_pose[0], end_pose[1]), 3)
    #
    # for bottom_diag_line in bottom_diag_line_status:
    #     if pygame.Rect.collidepoint(bottom_diag_line[0], x, y):
    #         bottom_diag_line[1] = 1
    #         # print(bottom_diag_line)
    #         start_pose = (bottom_diag_line[0][0], bottom_diag_line[0][1] + block_size)
    #         end_pose = (bottom_diag_line[0][0] + block_size, bottom_diag_line[0][1])
    #         pygame.draw.line(screen, BLACK, (start_pose[0], start_pose[1]), (end_pose[0], end_pose[1]), 3)

    print(active_line_list)


def main():
    game_over = False
    screen.fill(WHITE)

    draw_line()

    pygame.display.update()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                print(x, y)
                line_activate(x, y)
                pygame.display.update()


main()
