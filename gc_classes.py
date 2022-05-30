import pygame
import os
import sys
import Database as db

pygame.init()
size = width, height = 1900, 500
screen = pygame.display.set_mode(size)

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
end_group = pygame.sprite.Group()
start_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
blade_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
death_group = pygame.sprite.Group()
portal1_group = pygame.sprite.Group()
portal2_group = pygame.sprite.Group()
groups = [tiles_group, wall_group, end_group, start_group, spike_group, blade_group, portal1_group,
          portal2_group]


def load_image(name, colorkey=None): #загрузка изображений
    fullname = os.path.join('gc_data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image.convert_alpha()


class AnimatedSprite(pygame.sprite.Sprite): #класс позволяет создать анимированный спрайт
    def __init__(self, sheet, columns, rows, x, y, spin):
        super().__init__(all_sprites, death_group)
        self.frames = []
        self.spin = spin
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        if self.spin:
            self.image = pygame.transform.rotate(self.frames[self.cur_frame], 90)
        else:
            self.image = self.frames[self.cur_frame]

    def move(self, x, y):
        if x and y:
            self.rect.x = x
            self.rect.y = y


tile_images = {
    'wall2': load_image('objects/block1.png'),
    'wall': load_image('objects/gc_block.jpg'),
    'end': load_image('objects/gc_block.jpg'),
    'start': load_image('objects/gc_block.jpg'),
    'blade': load_image('objects/sawblade.png'),
    'blade1': load_image('objects/blade.png'),
    'blade2': load_image('objects/sawblade1.png'),
    'spike': load_image('objects/spike1.png'),
    'spike2': pygame.transform.flip(load_image('objects/spike1.png'), False, True),
    'empty': load_image('objects/gc_blue.png'),
    'empty2': load_image('objects/gc_pink.jpg'),
    'portal1': load_image('objects/portal1.png', -1),
    'portal2': load_image('objects/portal2.png', -1)
}
player_image1 = load_image('pictures/gcship.png', -1)
player_image2 = load_image('pictures/gc_icon1.png', 1)
player_image3 = load_image('pictures/gcship.png', 1)
tile_width = tile_height = tile_size = 50
player = None


class Tile(pygame.sprite.Sprite): #класс позволяет создать объекты (препятствия, шипы, пилы, порталы и т.д.)
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'wall' or tile_type == 'wall2':
            super().__init__(wall_group, all_sprites)
        elif tile_type == 'end':
            super().__init__(end_group, all_sprites)
        elif tile_type == 'start':
            super().__init__(start_group, all_sprites)
        elif tile_type == 'spike' or tile_type == 'spike2':
            super().__init__(spike_group, all_sprites)
        elif tile_type == 'blade' or tile_type == 'blade1' or tile_type == 'blade2':
            super().__init__(blade_group, all_sprites)
        elif tile_type == 'portal1':
            super().__init__(portal1_group, all_sprites)
        elif tile_type == 'portal2':
            super().__init__(portal2_group, all_sprites)
        elif tile_type == 'empty' or tile_type == 'empty2':
            super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 25, tile_height * pos_y + 25)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.x = self.rect.x
        self.y = self.rect.y

    def rotate(self):
        self.image = pygame.transform.rotate(self.image, 90)


class Player(pygame.sprite.Sprite): #класс отвечает за игрока, его движение, соприкосновение с другими объектами
    def __init__(self, pos_x, pos_y, player_image):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.x = pos_x
        self.y = pos_y
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15 + 25, tile_height * pos_y + 5 + 25)

    def move(self, x, y):
        self.rect.x += x * tile_width
        self.rect.y += y * tile_height

    def careful_move(self, x, y, group):
        self.move(x, -y)
        if pygame.sprite.spritecollideany(self, group):
            self.move(-x, y)
            return 0, 0
        return x, y

    def collide_check(self, group):
        return pygame.sprite.spritecollideany(self, group)


class Camera: #класс сдвигает все объекты относительно игрока
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy += 1


class Shop: #отвечает за инициализацию товаров магазина и их размещение в нем, отвечает за пополнение и списывание монет из табло
    def __init__(self, name_file):
        self.active = False
        self.name_file = name_file
        self.products = {}
        self.coords = []

    def load(self):
        lst = db.findallProducts()
        for product in lst:
            font_text = pygame.font.Font(None, 40)
            font_text_price = pygame.font.Font(None, 32)
            text = font_text.render(product[2], True, (250, 250, 250))
            text_price = font_text_price.render(str(product[3]), True, (250, 250, 250))
            if product[1] in self.products:
                self.products[product[1]].append({"text": text, "price": int(product[3]), "text_price": text_price, "image": load_image(product[4], -1), 'product': product[2]})
            else:
                self.products[product[1]] = [{"text": text, "price": int(product[3]), "text_price": text_price, "image": load_image(product[4], -1), 'product': product[2]}]

    def show(self, screen, user):
        x = 750
        y = 220
        for el in self.products.items():
            for product in el[1]:
                screen.blit(product["text"], (x, y + 60))
                screen.blit(product["text_price"], (x, y + 90))
                screen.blit(product["image"], (x, y))

                if not db.findUserProduct([user.username, product['product']]):
                    pygame.draw.rect(screen, (0, 250, 0), (x + 15, y + 130, 125, 50))
                    pygame.draw.rect(screen, (0, 0, 0), (x + 15, y + 130, 125, 50), 5)
                    self.coords.append([x + 15, y + 130, 125, 50, product])
                    font = pygame.font.Font(None, 40)
                    text = font.render("КУПИТЬ", True, (0, 0, 0))
                    screen.blit(text, (x + 21, y + 143))
                else:
                    pygame.draw.rect(screen, (230, 230, 230), (x + 15, y + 130, 150, 50))
                    pygame.draw.rect(screen, (0, 0, 0), (x + 15, y + 130, 150, 50), 5)
                    self.coords.append([x + 15, y + 130, 125, 50, product])
                    font = pygame.font.Font(None, 40)
                    text = font.render("КУПЛЕНО", True, (0, 0, 0))
                    screen.blit(text, (x + 21, y + 143))

                coin = pygame.transform.scale(load_image('pictures/coin2.png'), (15, 15))
                screen.blit(coin, (x + 40, y + 93))
                y += 250
            x += 250
            y = 220


    def buy(self, product, user):
        if not db.findUserProduct([user.username, product['product']]):
            if int(user.get_coin()) > product['price']:
                db.insertUserProduct([user.username, product['product'], 1])
                user.lost_coins += product['price']
                user.update()

#отвечает за занесение новых пользователей  в таблицу users базы данных GeometryCrash,
#за сохранение прогресса (процентов уровней и купленных в магазине товаров) пользователя, подсчет накопленных монет,
#смену у игрового персонажа базового скина на купленных в магазине скин
class User: 
    def __init__(self, username='None'):
        user = db.findUser([username])
        if not user:
            db.insertUser([username])
            user = db.findUser([username])
        self.username = username
        self.lvl1_percentage = user[0][2]
        self.lvl2_percentage = user[0][3]
        self.lvl3_percentage = user[0][4]
        self.lost_coins = user[0][5]

    def update(self):
        db.updateUser([self.lvl1_percentage, self.lvl2_percentage, self.lvl3_percentage, self.lost_coins, self.username])

    def get_coin(self):
        return str(self.lvl1_percentage + self.lvl2_percentage + self.lvl3_percentage - self.lost_coins)

    def load_image(self, level, prod):
        products = db.findallUserProducts([self.username])
        if level == 2 or level == 3:
            self.player_image = load_image('pictures/gc_icon2.png', 1)
            if products:
                for el in products:
                    if el[2] == 'Green-cube':
                        self.player_image = prod['lvl1'][0]['image']
        else:
            self.player_image = load_image('pictures/gcship1.png', -1)
            if products:
                for el in products:
                    if el[2] == 'Fast-rocket':
                        self.player_image = prod['lvl2'][0]['image']

    def get_image(self):
        return self.player_image
