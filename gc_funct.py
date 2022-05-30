from gc_classes import *

def start_level(event, flag, shop): #запуск выбранного уровня от нажатия кнопки мыши
    if event.type == pygame.MOUSEBUTTONDOWN and flag and not shop.active:
        if 450 <= event.pos[0] <= 645 and 250 <= event.pos[1] <= 455:
            level = 1
            audio = pygame.mixer.Sound('gc_data/music/gc_mus1.mp3')
        elif 850 <= event.pos[0] <= 1045 and 250 <= event.pos[1] <= 455:
            level = 2
            audio = pygame.mixer.Sound('gc_data/music/gc_mus2.mp3')
        elif 1250 <= event.pos[0] <= 1445 and 250 <= event.pos[1] <= 455:
            level = 3
            audio = pygame.mixer.Sound('gc_data/music/gc_mus3.mp3')
        else:
            level = 0
        if level != 0:
            percentage = 0
            flag = False
            pygame.mixer.pre_init()
            pygame.mixer.init()
            audio.play()
            return percentage, flag, audio, level
    return False


def count_percent(level_x, tiles_group, player, percent): #подсчет процентов от прохождения уровня
    koeff = (level_x + 1) / 100
    for i in tiles_group:
        if i.rect:
            if i.rect.x - 15 <= player.rect.x - 40 <= i.rect.x + 15:
                percentage = int(i.pos_x / koeff) + 2
                return percentage
    return percent


def renew(): #обнуление всех групп спрайтов
    all_sprites.empty()
    tiles_group.empty()
    wall_group.empty()
    end_group.empty()
    spike_group.empty()
    blade_group.empty()
    player_group.empty()
    portal1_group.empty()
    portal2_group.empty()
    start_group.empty()
    death_group.empty()


def jump(camera, jumping, fps_c, player, stage): #функция отвечает за прыжки персонажа
    if jumping and fps_c % 3 == 0:
        jump_stages = [-0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25,
                       0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.44]
        jump = jump_stages[stage]
        player.move(0, jump)
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)


def terminate(): #завершение работы программы
    pygame.quit()
    sys.exit()


def load_level(filename): #загрузка карты уровня из файла
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level, player_image, num=1): #преобразование элементов текстового файла в уровень
    new_player, x, y = None, None, None
    if num == 1:
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('empty', x, y)
                if level[y][x] == '*':
                    Tile('blade', x, y)
                if level[y][x] == '^':
                    Tile('blade1', x, y)
                if level[y][x] == '%':
                    Tile('blade2', x, y)
                if x == len(level[y]) - 1 and 0 < y < 10:
                    Tile('end', x, y)
                elif x == 0:
                    Tile('start', x, y)
                elif level[y][x] == '#':
                    Tile('wall', x, y)
                if level[y][x] == ':':
                    Tile('empty', x, y)
                    Tile('empty', x, y + 1)
                    Tile('portal1', x, y)
                if level[y][x] == '<':
                    Tile('empty', x, y)
                    Tile('spike', x, y)
                if level[y][x] == '>':
                    Tile('empty', x, y)
                    Tile('spike2', x, y)
                if level[y][x] == ';':
                    Tile('empty', x, y)
                    Tile('empty', x, y + 1)
                    Tile('portal2', x, y)
                if level[y][x] == '@':
                    Tile('empty', x, y)
                    new_player = Player(x, y, player_image)
        return new_player, x, y
    if num == 2 or num == 3:
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('empty2', x, y)
                if level[y][x] == '*':
                    Tile('blade', x, y)
                if level[y][x] == '^':
                    Tile('blade1', x, y)
                if level[y][x] == '%':
                    Tile('blade2', x, y)
                if x == len(level[y]) - 1:
                    Tile('end', x, y)
                if x == 0:
                    Tile('start', x, y)
                if level[y][x] == '#':
                    Tile('wall2', x, y)
                if level[y][x] == ':':
                    Tile('empty2', x, y)
                    Tile('empty2', x, y + 1)
                    Tile('portal1', x, y)
                if level[y][x] == ';':
                    Tile('empty2', x, y)
                    Tile('empty2', x, y + 1)
                    Tile('portal2', x, y)
                if level[y][x] == '<':
                    Tile('empty2', x, y)
                    Tile('spike', x, y)
                if level[y][x] == '>':
                    Tile('empty2', x, y)
                    Tile('spike2', x, y)
                if level[y][x] == '@':
                    Tile('empty2', x, y)
                    new_player = Player(x, y, player_image)
        return new_player, x, y
