import pygame
import pygame_menu
import socket
import select
import sys
import sqlite3


pygame.init()
surface = pygame.display.set_mode((1400, 700))

mas = [[0] * 3 for i in range(3)]
block_list = []


def check_win(x_or_0, turn):
    def end_win(x_or_y):
        window = pygame.display.set_mode((700, 350))
        window.fill([255, 255, 255])
        font = pygame.font.SysFont('couriernew', 40)
        text = font.render(str('Победил: ' + x_or_0), True, [0, 0, 0])
        window.blit(text, (50, 50))

        with sqlite3.connect("../db/database.db") as db:
            cursor = db.cursor()
            cursor.execute("""UPDATE players SET win = win+1 WHERE username =? """, (player_username, ))
            db.commit()

    if mas[0][0] == x_or_0 and mas[1][0] == x_or_0 and mas[2][0] == x_or_0:
        end_win(x_or_0)
    elif mas[0][1] == x_or_0 and mas[1][1] == x_or_0 and mas[2][1] == x_or_0:
        end_win(x_or_0)
    elif mas[0][2] == x_or_0 and mas[1][2] == x_or_0 and mas[2][2] == x_or_0:
        end_win(x_or_0)

    elif mas[0][0] == x_or_0 and mas[0][1] == x_or_0 and mas[0][2] == x_or_0:
        end_win(x_or_0)
    elif mas[1][0] == x_or_0 and mas[1][1] == x_or_0 and mas[1][2] == x_or_0:
        end_win(x_or_0)
    elif mas[2][0] == x_or_0 and mas[2][1] == x_or_0 and mas[2][2] == x_or_0:
        end_win(x_or_0)

    elif mas[0][0] == x_or_0 and mas[1][1] == x_or_0 and mas[2][2] == x_or_0:
        end_win(x_or_0)
    elif mas[2][0] == x_or_0 and mas[1][1] == x_or_0 and mas[0][2] == x_or_0:
        end_win(x_or_0)

    elif turn == 9:
        screen = pygame.display.set_mode((700, 350))
        screen.fill([255, 255, 255])
        font = pygame.font.SysFont('couriernew', 40)
        text = font.render(str('Победила дружба'), True, [0, 0, 0])
        screen.blit(text, (50, 50))


def start_game():
    for_read = []
    for_write = []
    buffer = []
    buf = []

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 6060)
    client.connect(server_address)
    print('Подключено к {} порт {}'.format(*server_address))
    for_read.append(client)
    client.send(str(player_username).encode('utf-8'))
    client.setblocking(False)

    block_size = 90
    left_margin = 400
    upper_margin = 100
    screen_size = (1400, 700)

    white = [255, 255, 255]
    black = [0, 0, 0]

    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("крестики нолики")
    game_over = False
    screen.fill(white)

    turn = 1

    for y in range(upper_margin, upper_margin + 3 * block_size, block_size):
        for x in range(left_margin, left_margin + 3 * block_size, block_size):
            block = pygame.Rect(x, y, block_size, block_size)
            block_list.append(block)

            pygame.draw.rect(screen, black, block, 3)
            pygame.display.update()

    def draw_x_or_0(x, y, what_move):
        col = (x - left_margin) // block_size
        row = (y - upper_margin) // block_size
        for block in block_list:
            if mas[col][row] == 0 and pygame.Rect.collidepoint(block, x, y):
                if what_move == "x":
                    pygame.draw.line(screen, black, (block[0], block[1]),
                                     (block[0] + block_size, block[1] + block_size), 2)
                    pygame.draw.line(screen, black, (block[0], block[1] + block_size),
                                     (block[0] + block_size, block[1]), 2)
                    mas[col][row] = "x"
                    check_win("x", turn)
                elif what_move == "0":
                    pygame.draw.circle(screen, black, (block[0] + block_size // 2, block[1] + block_size // 2),
                                       block_size // 2 - 4, 2)
                    mas[col][row] = "0"
                    check_win("0", turn)

        pygame.display.update()

    while not game_over:
        what_move = 0
        reads, _, _ = select.select(for_read, for_write, for_read, 0)
        for read in reads:
            if read is client:
                try:
                    data = read.recv(2 ** 16)
                    data = data.decode('utf-8')
                    if data != "x" and data != "0":
                        data = (int(data[1] + data[2] + data[3]), int(data[6] + data[7] + data[8]))
                        buf.append(data)
                    else:
                        buffer.append(data)
                except ConnectionResetError:
                    read.close()
                except ConnectionAbortedError:
                    pass

        if buffer[0] == "x" or buffer[0] == "0":
            what_move = buffer[0]

        if buf:
            x, y = buf[0]
            if what_move == "x":
                what_move = "0"
            else:
                what_move = "x"
            draw_x_or_0(x, y, what_move)
            turn += 1
            buf.clear()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                draw_x_or_0(x, y, what_move)
                client.send(str(event.pos).encode('utf-8'))
                turn += 1

        pygame.display.update()


menu = pygame_menu.Menu('Welcome', 1400, 700, theme=pygame_menu.themes.THEME_BLUE)
player_username = str(sys.argv[1])
welcome = menu.add.label("Добро пожаловать " + player_username)
menu.add.button('Play', start_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)
