from sys import exit as win_exit
from random import randint, choice
import pygame

#Создание классов и функций
class Player:
    def __init__(self, skin, start_pos, control):
        # control = (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d)
        self.image = pygame.image.load(skin).convert()
        self.image_rect = self.image.get_rect(topleft=start_pos)
        self.p_start_x, self.p_start_y = start_pos
        self.death_count = 0
        self.gift_count = 0
        self.control = control
        self.player_speed = 0; self.k_speed = 5
        self.player_gravity = 0
        self.jump_height = -7
        self.moving_right = False; self.moving_left = False; self.is_jumping = False

    def move(self, keys, tile_rects, in_water):
        movement = [0, 0]  
        collision_types = {'top': False, 'bottom': False}

        if keys[self.control[3]]:  
            movement[0] += (self.k_speed + self.player_speed)  
        if keys[self.control[1]]:  
            movement[0] -= (self.k_speed + self.player_speed) 

        if in_water:
            if keys[self.control[0]]: 
                movement[1] -= 5  
            else:
                movement[1] += 4  
        else:
            if keys[self.control[0]] and not self.is_jumping:  # Прыжок
                self.player_gravity = self.jump_height 
                self.is_jumping = True
            self.player_gravity += 0.5 
            movement[1] += self.player_gravity
            
        self.image_rect.x += movement[0] # проверка на горизонтальное столкновение
        for tile in self.__collision_test(self.image_rect, tile_rects):
            if movement[0] > 0: 
                self.image_rect.right = tile.left
            elif movement[0] < 0:  
                self.image_rect.left = tile.right

        self.image_rect.y += movement[1] 
        for tile in self.__collision_test(self.image_rect, tile_rects): #проверка на вертикальное столкновение с блоками
            if movement[1] > 0:  # Движение вниз
                self.image_rect.bottom = tile.top
                self.player_gravity = 0
                collision_types['bottom'] = True
                self.__reset_jump()
            elif movement[1] < 0:  # Движение вверх
                self.image_rect.top = tile.bottom
                self.player_gravity = 1  # Падение при коллизии
        self.__gravity_limit()

    def __collision_test(self, rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list
    
    def check_collisions(self, rects):
        for rect in rects:
            if self.image_rect.colliderect(rect):
                return True
        return False
    
    def __gravity_limit(self):
        if self.player_gravity > 15:
            self.player_gravity = 15

    def set_position(self, pos):
        self.image_rect.x, self.image_rect.y = pos

    def __reset_jump(self):
        self.is_jumping = False

    def draw(self, scroll):
        screen.blit(self.image, (self.image_rect.x - scroll[0], self.image_rect.y - scroll[1]))


class Monster:
    def __init__(self, path, position, speed, direction):
        self.image = pygame.image.load(path)
        self.image_rect = self.image.get_rect(topleft=position)
        self.speed = speed
        self.direction = direction

    def is_visible(self, player):
        return player.image_rect.x - 700 < self.image_rect.x < player.image_rect.x + 700

    def update(self, tile_rects, player, scroll):
        if self.is_visible(player):
            self.move(tile_rects, player, scroll)  # Передаем player
            self.draw(scroll)
        

    def move(self, tile_rects, player, scroll):
        movement = self.direction * self.speed * 2
        collision_types = {'left': False, 'right': False}

        # Движение монстра
        self.image_rect.x += movement
        for tile in self.__collision_test(self.image_rect, tile_rects):
            if movement > 0:  # Движение вправо
                self.image_rect.right = tile.left
                collision_types['left'] = True
            elif movement < 0:  # Движение влево
                self.image_rect.left = tile.right
                collision_types['right'] = True
                
        if collision_types['right']:
            self.direction = -1
            if movement == 0:
                self.image_rect.x -= 20
        elif collision_types['left']:
            self.direction = 1
            if movement == 0:
                self.image_rect.x += 20

    def __collision_test(self, rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def draw(self, scroll):
        screen.blit(self.image, (self.image_rect.x - scroll[0], self.image_rect.y - scroll[1]))

        
class Star: #класс звезда
    def __init__(self, image, pos): #создание снежинки
        self.image = image
        self.image_rect = self.image.get_rect(center=pos)

    def draw(self, scroll):
        screen.blit(self.image, (self.image_rect.x - scroll[0], self.image_rect.y - scroll[1]))


class Background: #класс заднего фона, нужен чтобы в окне options менять фон
    def __init__(self, color):
        self.__color = color

    def set_bg_color(self, new_color):
        self.__color = new_color

    def get_bg_color(self):
        return self.__color

    def draw(self):
        screen.fill(self.__color)


class Snowflake: #класс снежинка
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = randint(2, 5)  
        self.fall_speed = randint(1, 3)
        self.random_wind_speed = randint(0, 3)

    def update(self): #падение снежинки
        self.y += self.fall_speed  
        self.x += self.random_wind_speed
        if self.y > 900:  
            self.reset()  

    def reset(self): #изменение координат снежинки
        self.y = randint(-200, 50)  
        self.x = randint(0, 9000)  

    def draw(self, scroll): #отрисовка снежинки
        pygame.draw.circle(screen, (255, 255, 255), (self.x - scroll[0], self.y), self.size)


class Shaurma: #класс шаурма
    def __init__(self, image, pos):
        self.image = image
        self.image_rect = self.image.get_rect(topleft=pos)
        self.pos = pos
        self.collected = False  # Флаг для отслеживания, собрана ли шаурма
    
    def draw(self, scroll): #отрисовка
        if not self.collected:  # рисуем только если шаурма не собрана
            screen.blit(self.image, (self.image_rect.x - scroll[0], self.image_rect.y - scroll[1]))
    
    def collision(self, player_rect): #проверка столкновения шаурмы и игрока
        return self.image_rect.colliderect(player_rect) and not self.collected


class Button: #Класс кнопка(её нет в pygame)
    def __init__(self, image, pos, text_input, command, screen):
        self.command = command
        self.image = image
        self.position = pos
        self.rect = self.image.get_rect(center=(self.position[0], self.position[1]))
        self.text_input = text_input
        self.screen = screen
        self.text = Label(text_input, 50, 'white', (self.position[0], self.position[1])) 

    def update(self):
        screen.blit(self.image, self.rect)
        if self.text != '':
            self.text.draw(self.screen)  

    def checkForInput(self, position, event): #нажатие кнопки и выполнение команды
        if self.rect.collidepoint(position) and event.type == pygame.MOUSEBUTTONDOWN:
            buttonsound.play()
            self.command()

    def changeColor(self, position): #изменить цвет есил навелась
        if self.rect.collidepoint(position):
            self.text.color = "green"  
        else:
            self.text.color = "white"  
        self.text.update_text()  
    

class Label: #мой класс для текста
    def __init__(self, text, font_size, color, pos):
        self.text_input = text
        self.font_size = font_size
        self.color = color
        self.position = pos
        self.update_text()

    @staticmethod
    def get_font(size):
        return pygame.font.Font("fonts/font.ttf", size)

    def update_text(self): #обновить текст при изменении текста
        self.text_surface = self.get_font(self.font_size).render(self.text_input, True, self.color)
        self.text_rect = self.text_surface.get_rect(center=self.position)

    def draw(self, screen): # отрисовка
        screen.blit(self.text_surface, self.text_rect)

    def set_text(self, new_text): #изменить текст
        self.text_input = new_text
        self.update_text()


class MusicPlayer: #класс для удобного использования фоновой музыки
    def __init__(self):
        self.tracks = [
            "music/bgmusic1.mp3",
            "music/bgmusic2.ogg",
            "music/barbariki.mp3"]
        self.track_index = 0
        self.volume = 0.1
        self.is_playing = False
        
    def play(self): #проигрывание музыки
        if self.is_playing:
            pygame.mixer.music.stop()
        pygame.mixer.music.load(self.tracks[self.track_index])
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1) 
        self.is_playing = True

    def next_track(self): #следующий трек
        self.track_index = (self.track_index + 1) % len(self.tracks)
        self.play()

    def previous_track(self): #прошлый трек
        self.track_index = (self.track_index - 1) % len(self.tracks)
        self.play()

    def up_volume(self): #повысить громкость
        self.volume += 0.1  
        if self.volume > 1.0: 
            self.volume = 1.0
        pygame.mixer.music.set_volume(self.volume) 

    def down_volume(self): #понизить громкость
        self.volume -= 0.1  
        if self.volume < 0.0:  
            self.volume = 0.0
        pygame.mixer.music.set_volume(self.volume) 

    def stop(self): #остановить музыку
        pygame.mixer.music.stop()
        self.is_playing = False

def set_coords_condition(): #изменение состояния Label координат(нужно для отображения на экране)
    global coords_condition_label
    if coords_condition_label == True:
        coords_condition_label = False
    else:
        coords_condition_label = True

def set_skin(path): #Установить скин игрока
    global skin
    skin = path

def handle_events(buttons):
    OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            win_exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                button.checkForInput(OPTIONS_MOUSE_POS, event)

def load_map(filename): #считывание карты из текстового файла и присваивание в переменную
    game_map = []
    with open(filename, 'r') as file:
        for line in file:
            game_map.append(list(line.strip()))  
    return game_map

#инициализация игры, загрузка игровых карт, первоначальная настройка
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Shaurm Cubeater")
pygame.display.set_icon(pygame.image.load('images/skins/eln.png'))
music_player = MusicPlayer()
BG = Background(((81, 120, 219))) #создание экземляра класса задний фон, задает изначальный цвет.
map1 = load_map('maps/map1.txt')
map2 = load_map('maps/map2.txt')
map3 = load_map('maps/map3.txt')
win_size = [1280, 700]; bg_color = (81, 120, 219)
screen = pygame.display.set_mode((win_size[0], win_size[1]))
coords_condition_label = False
current_window = 'main_menu'


#Создание картинок для блоков, скинов, и прочего.
skin = 'images/skins/player.png'
bg = pygame.image.load('images/other/polskkorova.jpg').convert(); bg_rect = bg.get_rect(topleft=(0, 0))
button1 = pygame.image.load('images/other/mybutton.png').convert()
button2 = pygame.image.load("images/other/button2.png").convert()
shaurma_image = pygame.image.load('images/other/shaurma.png').convert_alpha()
dirt, grass, stone, spike, snow_grass, dark_dirt, star_image, water, stoun_brick, spike_rotated, ice_spike, cloud, dirt_wall, stone_wall, ice_stone, ice_wall, ice_spike_rotated, glass, brick_wall = (
    pygame.image.load('images/blocks/dirt.jpg').convert(),
    pygame.image.load('images/blocks/grass.jpg').convert(),
    pygame.image.load('images/blocks/stone.jpg').convert(),
    pygame.image.load('images/blocks/spike.png').convert_alpha(),
    pygame.image.load('images/blocks/snow_grass.jpg').convert(),
    pygame.image.load('images/blocks/dark_dirt.jpg').convert(),
    pygame.image.load('images/other/star.png').convert_alpha(),
    pygame.image.load('images/blocks/water.png').convert_alpha(),
    pygame.image.load('images/blocks/stoun_brick.jpg').convert(),
    pygame.transform.rotate(pygame.image.load('images/blocks/spike.png'), 180).convert_alpha(),
    pygame.image.load('images/blocks/ice_spike.png').convert_alpha(),
    pygame.image.load('images/blocks/cloud.png').convert(),
    pygame.image.load('images/blocks/dirt_wall.jpg').convert(),
    pygame.image.load('images/blocks/stone_wall.jpg').convert(),
    pygame.image.load('images/blocks/ice_stone.png').convert(),
    pygame.image.load('images/blocks/ice_stone_wall.png').convert(),
    pygame.transform.rotate(pygame.image.load('images/blocks/ice_spike.png'), 180).convert_alpha(),
    pygame.image.load('images/blocks/glass.png').convert_alpha(),
    pygame.image.load('images/blocks/brick_wall.jpg').convert())

tile_mapping_map1 = {
    '1': dirt,
    '2': grass,
    '3': stone,
    '4': spike,
    '6': spike_rotated,
    '9': stone_wall,
    'w': water,
    '8': dirt_wall,
    'c': cloud,
    '0': None }

tile_mapping_map2 = {
    '1': dark_dirt,
    '2': snow_grass,
    '3': ice_stone,
    '4': ice_spike,
    '6': ice_spike_rotated,
    '9': ice_wall,
    's': stoun_brick,
    'S': brick_wall,
    'c': cloud, 
    '0': None }

tile_mapping_map3 = {
    '1': dark_dirt,
    '2': snow_grass,
    '4': ice_spike,
    '6': ice_spike_rotated,
    '8': dirt_wall,
    's': stoun_brick,
    '0': None,
    'c': cloud}

# создание звуков
buttonsound = pygame.mixer.Sound("music/button.ogg"); buttonsound.set_volume(0.5) 
win_sound = pygame.mixer.Sound('music/win.ogg')
eating_sound = pygame.mixer.Sound('music/eating_shaurma.ogg')

#функции для создания игровых окон
def play(game_map, skin, map_name):
    global coords_condition_label
    global current_window
    current_window = 'play'
    if map_name == 1:
        p_start_x = 2500
    else:
        p_start_x = 2000
    p_start_y = 950
    tile_size = 50
    scroll = [0, 0]

    fps = pygame.time.Clock()
    player = Player(skin, (p_start_x, p_start_y), (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d))
    #Создание снежков, звёзд, шаурм, Label, Некоторых кнопок
    snowflakes = [Snowflake(randint(-1500, 7500), randint(-200, 0)) for i in range(100)]
    stars = [Star(star_image, (randint(0, 9500), randint(0, 900))) for i in range(100)]
    shaurms_1 = [Shaurma(shaurma_image, (4150, 1350)), Shaurma(shaurma_image, (1700, 1850)),
                Shaurma(shaurma_image, (3000, 950)), Shaurma(shaurma_image, (5500, 1550)),
                Shaurma(shaurma_image, (5350, 850)), Shaurma(shaurma_image, (3400, 0))]
    shaurms_2 = [Shaurma(shaurma_image, (3000, 950)), Shaurma(shaurma_image, (1300, 950)),
                 Shaurma(shaurma_image, (2450, 1350)), Shaurma(shaurma_image, (p_start_x + 100, 950)),
                 Shaurma(shaurma_image, (1900, 2050)), Shaurma(shaurma_image, (7250, 1100)),
                 Shaurma(shaurma_image, (10750, 800))]
    shaurms_3 = [Shaurma(shaurma_image, (p_start_x + 200, p_start_y)), Shaurma(shaurma_image, (p_start_x + 200, p_start_y)),
                 Shaurma(shaurma_image, (4400, 250)), Shaurma(shaurma_image, (4400, 250)),
                 Shaurma(shaurma_image, (6000, 850)), Shaurma(shaurma_image, (6500, 700)),
                 Shaurma(shaurma_image, (4950, 200)), Shaurma(shaurma_image, (11000, 800))]
    monsters = [Monster('images/skins/horror2.png', (3400, 2050), -4, 1), Monster('images/skins/knight.jpg', (7250, 1100), -1.5, 1),
                Monster('images/skins/axol.png', (10900, 1400), -2, 1), Monster('images/skins/knight.jpg', (8400, 1100), -5, 1)]
    monsters_2 = [Monster('images/skins/horror2.png', (5000, 850), -3, 1), Monster('images/skins/horror.png', (4200, 950), -2, 1),
                  Monster('images/skins/horror.png', (5900, 850), -2, 1),
                  Monster('images/skins/horror2.png', (6500, 850), -3, -1),
                  Monster('images/skins/knight.jpg', (10200, 850), 3, -1), Monster('images/skins/apple_dirt_snake.png', (9500, 850), 3, 1),
                  Monster('images/skins/horror2.png', (9800, 850), 4, -1), Monster('images/skins/horror2.png', (7200, 500), 2, -1),]
    fps_label = Label(f'фпс: {round(fps.get_fps())}/60', 40, 'white', (120, 110))
    coords_label = Label(f'x: {player.image_rect.x}, y: {player.image_rect.y}', 40, 'white', (1000, 50))
    shaurm_count = Label(f'Собрано шаурм: {player.gift_count}', 40, 'white', (120, 80))
    death_count_label = Label(f'Смертей: {player.death_count}', 50, (150, 190, 199), (80, 40))
    skins = ['horror.png', 'horror2.png', 'snake.png', 'knight.jpg', 'anything.png']
    def iteration_shaurm(shaurms, count):
        for shaurm in shaurms:
            shaurm.draw(scroll)  
            if shaurm.collision(player.image_rect):  
                player.gift_count += 1
                player.jump_height -= 1
                player.player_speed += 1
                shaurm_count.set_text(f'Собрано шаурм: {player.gift_count}/{count}')
                shaurm.collected = True  # Устанавливаем флаг шаурма собрана
                shaurms.remove(shaurm)  # Удаляем собранную шаурму из списка 
                eating_sound.play()
                # random_x_monster = randint(200, 500); random_speed_monster = randint(1, 5); rand_skin = choice(skins)
                # random_direction = choice([-1, 1])
                # monsters.append(Monster(f'images/skins/{rand_skin}', 
                #     (player.image_rect.x - random_x_monster, player.image_rect.y), random_speed_monster, random_direction))

    def iteration_monsters(monsters, tile_rects, player, scroll):
        for monster in monsters:
            monster.update(tile_rects, player, scroll)  # Передаем игрока
        
    
    if map_name == 1:
        tile_mapping = tile_mapping_map1
    elif map_name == 2:
        tile_mapping = tile_mapping_map2
    else:
        tile_mapping = tile_mapping_map3
    running = True
    visible_width = 1280  
    monster_added = False
    visible_height = win_size[1] 
    while current_window == 'play':
        keys = pygame.key.get_pressed()
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        if running:
            scroll[0] = player.image_rect.x - win_size[0] // 2 + 25
            scroll[1] = player.image_rect.y - win_size[1] // 2 + 25
            BG.draw()

            tile_rects = []; spike_rects = []; water_rects = []
            left_bound = ((player.image_rect.x - visible_width // 2) // tile_size) 
            right_bound = ((player.image_rect.x + visible_width // 2) // tile_size) + 1
            top_bound = ((player.image_rect.y - visible_height // 2) // tile_size) 
            bottom_bound = ((player.image_rect.y + visible_height // 2) // tile_size) + 1
            if BG.get_bg_color() == (0, 0, 0):
                for star in stars:
                    star.draw(scroll)
            if map_name == 1:
                for y in range(max(0, top_bound), min(len(game_map), bottom_bound + 1)):
                    for x in range(max(0, left_bound), min(len(game_map[y]), right_bound + 1)):
                        tile = game_map[y][x]
                        tile_x = x * tile_size - scroll[0]
                        tile_y = y * tile_size - scroll[1]
                        if tile not in ('0', '4', '6', 'w', '8', '9'):
                            tile_rects.append(pygame.Rect(x*tile_size, y * tile_size, tile_size, tile_size))
                            image = tile_mapping[tile]
                            screen.blit(image, (tile_x, tile_y))
                            tile_rects.append(pygame.Rect(tile_x, tile_y, tile_size, tile_size))
                        if tile == 'w':
                            screen.blit(water, (tile_x, tile_y))
                            water_rect = pygame.rect.Rect(x*tile_size, y * tile_size, tile_size, tile_size)
                            water_rects.append(water_rect)
                        elif tile in ('8', '9'):
                            image = tile_mapping[tile]
                            screen.blit(image, (tile_x, tile_y))
                        elif tile == '4':
                            if game_map[y+1][x] == '1':
                                screen.blit(dirt_wall, (tile_x, tile_y))
                            elif game_map[y+1][x] == '3':
                                screen.blit(stone_wall, (tile_x, tile_y))
                            spike_rect = pygame.Rect(x * tile_size + 10, y * tile_size + 28, 27, 22)
                            spike_rects.append(spike_rect) 
                            screen.blit(spike, (tile_x, tile_y ))
                        elif tile == '6':
                            if game_map[y-1][x] == '1':
                                screen.blit(dirt_wall, (tile_x, tile_y))
                            elif game_map[y-1][x] == '3':
                                screen.blit(stone_wall, (tile_x, tile_y))
                            spike_rect = pygame.rect.Rect(x * tile_size + 10, y * tile_size + 28, 27, 22)
                            spike_rects.append(spike_rect) 
                            screen.blit(spike_rotated, (tile_x, tile_y ))
                iteration_shaurm(shaurms_1, 6)
                if player.gift_count == 6:
                    win_window()
            elif map_name == 2:
                for snowflake in snowflakes:
                    snowflake.update()
                    snowflake.draw(scroll)
                for y in range(max(0, top_bound), min(len(game_map), bottom_bound + 1)):
                    for x in range(max(0, left_bound), min(len(game_map[y]), right_bound + 1)):
                        tile = game_map[y][x]
                        tile_x = x * tile_size - scroll[0]
                        tile_y = y * tile_size - scroll[1]
                        if tile not in ('0', '4', '6', 'w', 's', '8', 'g'):
                            tile_rects.append(pygame.Rect(x*tile_size, y * tile_size, tile_size, tile_size))
                            image = tile_mapping[tile]
                            screen.blit(image, (tile_x, tile_y))
                            tile_rects.append(pygame.Rect(tile_x, tile_y, tile_size, tile_size))
                        elif tile == '8':
                            screen.blit(dirt_wall, (tile_x, tile_y))
                        elif tile == 'w':
                            screen.blit(water, (tile_x, tile_y))
                            water_rect = pygame.rect.Rect(x*tile_size, y * tile_size, tile_size, tile_size)
                            water_rects.append(water_rect)
                        elif tile == 's':
                            screen.blit(stoun_brick, (tile_x, tile_y))
                        elif tile == '4':
                            if game_map[y+1][x] == '1':
                                screen.blit(dirt_wall, (tile_x, tile_y))
                            spike_rect = pygame.Rect(x * tile_size + 10, y * tile_size + 28, 27, 22)
                            spike_rects.append(spike_rect) 
                            screen.blit(ice_spike, (tile_x, tile_y ))
                        elif tile == '6':
                            if game_map[y-1][x] == '1' or game_map[y+1][x] == '1':
                                screen.blit(dirt_wall, (tile_x, tile_y))
                            spike_rect = pygame.rect.Rect(x * tile_size + 10, y * tile_size + 28, 27, 22)
                            spike_rects.append(spike_rect) 
                            screen.blit(ice_spike_rotated, (tile_x, tile_y ))
                        elif tile == 'g':
                            screen.blit(glass, (tile_x, tile_y))
                iteration_monsters(monsters, tile_rects, player, scroll)
                iteration_shaurm(shaurms_2, 7)
                if player.gift_count == 7:
                    win_window()
            elif map_name == 3:
                for y in range(max(0, top_bound), min(len(game_map), bottom_bound + 1)):
                    for x in range(max(0, left_bound), min(len(game_map[y]), right_bound + 1)):
                        tile = game_map[y][x]
                        tile_x = x * tile_size - scroll[0]; tile_y = y * tile_size - scroll[1]
                        if tile not in ('0', '4', '6', 'w', '8'):
                            tile_rects.append(pygame.Rect(x*tile_size, y * tile_size, tile_size, tile_size))
                            image = tile_mapping[tile]
                            screen.blit(image, (tile_x, tile_y))
                            tile_rects.append(pygame.Rect(tile_x, tile_y, tile_size, tile_size))
                        if tile == 'w':
                            screen.blit(water, (tile_x, tile_y))
                            water_rect = pygame.rect.Rect(x*tile_size, y * tile_size, tile_size, tile_size)
                            water_rects.append(water_rect)
                        elif tile in ('8'):
                            image = tile_mapping[tile]
                            screen.blit(image, (tile_x, tile_y))
                        elif tile == '4':
                            spike_rect = pygame.Rect(x * tile_size + 10, y * tile_size + 28, 27, 22)
                            spike_rects.append(spike_rect) 
                            screen.blit(spike, (tile_x, tile_y ))
                        elif tile == '6':
                            spike_rect = pygame.rect.Rect(x * tile_size + 10, y * tile_size + 28, 27, 22)
                            spike_rects.append(spike_rect) 
                            screen.blit(spike_rotated, (tile_x, tile_y ))
                        elif tile == '8':
                            screen.blit(dirt_wall, (tile_x, tile_y))
                iteration_monsters(monsters_2, tile_rects, player, scroll)
                iteration_shaurm(shaurms_3, 8)
                if player.gift_count == 8:
                    win_window()
            in_spike = player.check_collisions(spike_rects)
            in_water = player.check_collisions(water_rects)
            if in_spike:
                player.image_rect.center = (p_start_x, p_start_y)
                player.player_gravity = 0 
                player.death_count += 1
                death_count_label.set_text(f'Смертей: {player.death_count}')
            player.move(keys, tile_rects, in_water) #движение игрока
            player.draw(scroll=scroll) #отрисовка каждый в каждом кадре
        fps_label.set_text(f'fps: {round(fps.get_fps())}') #фпс меняется каждую секунду, его Label следовательно тоже
        fps_label.draw(screen)
        death_count_label.draw(screen=screen)
        shaurm_count.draw(screen=screen)

        if coords_condition_label: #если состояние текста координат истинно
            coords_label.set_text(f'x: {player.image_rect.x} y: {player.image_rect.y}')
            coords_label.draw(screen)

        for event in pygame.event.get(): #события
            if event.type == pygame.QUIT:
                running = False
                win_exit()
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                current_window = 'main_menu'

        pygame.display.flip()
        fps.tick(60) #Ставим ограничение для кадров в секунду/фпс/fps.

def options(): #Окно настройки
    global bg_color
    global current_window
    current_window = 'options'
    screen.fill('black')
    BG.draw()
    options_label = Label("окно с настройками?", 70, "White", (640, 80))
    select_bg_label = Label("ВЫБЕРИТЕ ФОН", 45, "White", (150, 100))
    select_skin_label = Label("ВЫБЕРИТЕ СКИН", 45, "White", (1100, 100))
    buttons = (
    Button(image=pygame.image.load("images/other/button2.png"), pos=(100, 200), 
            text_input="НОЧНОЙ", command=lambda: BG.set_bg_color((0, 0, 0)), screen=screen),
    Button(image=pygame.image.load("images/other/button2.png"), pos=(220, 200), 
            text_input="ДНЕВНОЙ", command=lambda: BG.set_bg_color((81, 120, 219)), screen=screen),
    Button(image=pygame.image.load("images/skins/eln.png"), pos=(1000, 200),
            text_input="", command=lambda: set_skin('images/skins/eln.png'), screen=screen),
    # Button(image=pygame.image.load("images/skins/ruslan_skin.png"), pos=(1060, 200),
    #         text_input="", command=lambda: set_skin('images/skins/ruslan_skin.png'), screen=screen),
    Button(image=pygame.image.load("images/skins/skin3.png"), pos=(1120, 200),
            text_input="", command=lambda: set_skin('images/skins/skin3.png'), screen=screen),
    Button(image=pygame.image.load("images/skins/cat.png"), pos=(1180, 200),
            text_input="", command=lambda: set_skin('images/skins/cat.png'), screen=screen),
    Button(image=pygame.image.load("images/skins/axol.png"), pos=(1240, 200),
            text_input="", command=lambda: set_skin('images/skins/axol.png'), screen=screen),
    Button(image=pygame.image.load("images/skins/snake.png"), pos=(1000, 260),
            text_input="", command=lambda: set_skin('images/skins/snake.png'), screen=screen),
    Button(image=pygame.image.load("images/skins/bear.png"), pos=(1060, 260),
            text_input="", command=lambda: set_skin('images/skins/bear.png'), screen=screen),
    Button(image=pygame.image.load("images/skins/apple_dirt_snake.png"), pos=(1120, 260),
            text_input="", command=lambda: set_skin('images/skins/apple_dirt_snake.png'), screen=screen),
    Button(image=pygame.image.load("images/skins/steve.png"), pos=(1180, 260),
            text_input="", command=lambda: set_skin('images/skins/steve.png'), screen=screen),
    Button(image=pygame.image.load("images/skins/horror.png"), pos=(1240, 260),
            text_input="", command=lambda: set_skin('images/skins/horror.png'), screen=screen),
    Button(image=pygame.image.load("images/skins/horror2.png"), pos=(1000, 320),
            text_input="", command=lambda: set_skin('images/skins/horror2.png'), screen=screen),
    Button(image=pygame.image.load("images/skins/anything.png"), pos=(1060, 320),
            text_input="", command=lambda: set_skin('images/skins/anything.png'), screen=screen),
    Button(image=pygame.image.load("images/skins/smile.png"), pos=(1120, 320),
            text_input="", command=lambda: set_skin('images/skins/smile.png'), screen=screen),
    Button(image=pygame.image.load("images/skins/skala.png"), pos=(1180, 320),
            text_input="", command=lambda: set_skin('images/skins/skala.png'), screen=screen),
    Button(image=pygame.image.load("images/skins/creeper.png"), pos=(1240, 320),
            text_input="", command=lambda: set_skin('images/skins/creeper.png'), screen=screen),
    Button(image=pygame.image.load("images/skins/steve.png"), pos=(1000, 380),
            text_input="", command=lambda: set_skin('images/skins/steve.png'), screen=screen),
    Button(image=pygame.image.load("images/skins/aig1.png"), pos=(1060, 380),
            text_input="", command=lambda: set_skin('images/skins/aig1.png'), screen=screen),
    Button(image=pygame.image.load("images/skins/aig2.png"), pos=(1120, 380),
            text_input="", command=lambda: set_skin('images/skins/aig2.png'), screen=screen),
    Button(image=pygame.image.load("images/skins/aig3.png"), pos=(1180, 380),
            text_input="", command=lambda: set_skin('images/skins/aig3.png'), screen=screen),
    Button(image=pygame.image.load("images/skins/t2x2.jpg"), pos=(1180, 380),
            text_input="", command=lambda: set_skin('images/skins/t2x2.jpg'), screen=screen),
    Button(image=button1, pos=(640, 600), 
            text_input="ОБРАТНО", command=main_menu, screen=screen),
    Button(image=button1, pos=(640, 400), 
                    text_input="ИГРАТЬ", command=level_selection, screen=screen),
    Button(image=button2, pos=(750, 200), 
            text_input="stop", command=music_player.stop, screen=screen),
    Button(image=button2, pos=(500, 160), 
            text_input="<--", command=music_player.down_volume, screen=screen),
    Button(image=button2, pos=(610, 160), 
            text_input="-->", command=music_player.up_volume, screen=screen),
    Button(image=button2, pos=(500, 260), 
            text_input="<--", command=music_player.next_track, screen=screen),
    Button(image=button2, pos=(610, 260), 
            text_input="-->", command=music_player.previous_track, screen=screen),
    Button(image=button2, pos=(100, 600), 
            text_input="Корды", command=set_coords_condition, screen=screen))

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        screen.fill("black")

        options_label.draw(screen)
        select_bg_label.draw(screen)
        select_skin_label.draw(screen)
        for button in buttons:
            button.changeColor(OPTIONS_MOUSE_POS)  
            button.update()
        handle_events(buttons)
        pygame.display.update()

def win_window():
    global current_window
    current_window = 'win_window'
    buttons = [Button(image=button1, pos=(640, 600), 
                   text_input="МЕНЮ", command=main_menu, screen=screen),
                Button(image=button1, pos=(640, 400), 
                            text_input="ИГРАТЬ", command=level_selection, screen=screen)]
    labels=[Label('Поздравляю, вы прошли уровень', 50, 'white', (700, 100)),
            Label('Вы проявили терпение, бесчисленное количество раз умирая.', 50, 'white', (700, 150)),
            Label('Я уважаю ваши порывы, но за победу вы ничего не получите.', 50, 'white', (700, 200)),
            Label('+ RESPECT, Now get lost!', 50, 'white', (700, 250))]
    win_sound.play()
    while current_window == 'win_window':
        screen.fill('black')
        WIN_mouse_pos = pygame.mouse.get_pos()
        for label in labels:
            label.draw(screen=screen)
        for event in pygame.event.get():  # Обработка событий
            if event.type == pygame.QUIT:
                pygame.quit()
                win_exit
        for button in buttons:
            button.changeColor(WIN_mouse_pos)  
            button.update()
        handle_events(buttons)
        pygame.display.update()

def main_menu():
    global current_window
    current_window = 'main_menu'

    screen.blit(bg, bg_rect)

    while current_window == "main_menu": 
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = Label('Shaurm Cubeater', 100, 'black', (640, 100))

        buttons = [Button(image=button1, pos=(640, 250), 
                            text_input="ИГРАТЬ", command=level_selection, screen=screen),
                   Button(image=button1, pos=(640, 420), 
                            text_input="НАСТРОЙКИ", command=options, screen=screen),
                   Button(image=button1, pos=(640, 590), 
                            text_input="ВЫЙТИ", command=win_exit, screen=screen)]
       
        MENU_TEXT.draw(screen)

        for button in buttons:
            button.changeColor(MENU_MOUSE_POS)
            button.update()
        
        handle_events(buttons)
        pygame.display.update()

def main():
    global current_window

    music_player.play()
    while True:
        if current_window == "main_menu":
            main_menu()
        elif current_window == "options":
            options()
        elif current_window == "level_selection":
            level_selection()
        elif current_window == 'win_window':
            win_window()
        if music_player.is_playing:
            music_player.stop()
        else:
            music_player.play()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                win_exit()
                
def level_selection():
    global current_window
    while True:
        SELECT_MOUSE_POS = pygame.mouse.get_pos()
        screen.fill('black')
        SELECT_TEXT = Label("Выберите уровень", 100, 'white', (640, 100))
        SELECT_TEXT.draw(screen)

        buttons = [Button(image=button1, pos=(640, 250), 
                    text_input="Уровень 1", command=lambda: play(map1, skin, 1), screen=screen),
                   Button(image=button1, pos=(640, 420), 
                    text_input="Уровень 2", command=lambda: play(map2, skin, 2), screen=screen),
                Button(image=button2, pos=(350, 420), 
                    text_input="Уровень 3", command=lambda: play(map3, skin, 3), screen=screen),
                   Button(image=button1, pos=(640, 590), 
                    text_input="Назад", command = main_menu, screen=screen)]

        for button in buttons:
            button.changeColor(SELECT_MOUSE_POS)
            button.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                win_exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    button.checkForInput(SELECT_MOUSE_POS, event)

        pygame.display.update()

if __name__ == "__main__":
    main()