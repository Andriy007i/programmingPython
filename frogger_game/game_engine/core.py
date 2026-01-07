import pygame
import random
import math
from config import *

class GameOver(Exception):
    pass

class Engine:
    def __init__(self, width_tiles, height_tiles):
        self.width_tiles = width_tiles
        self.height_tiles = height_tiles
        self.max_hp = 100
        self.current_hp = 100
        self.score = 0
        self.xp = 0
        self.level = 1
        self.start_time = pygame.time.get_ticks()
        # Таймеры
        self.is_frozen = False
        self.freeze_end_time = 0
        self.freeze_cooldown_time = 0
        
        self.shield_active = False
        self.shield_end_time = 0
        self.shield_cooldown_time = 0
        
        self.items = []
        self.reset_game()

    def reset_game(self):
        self.player_x = PLAYER_START_X * TILE_SIZE
        self.player_y = PLAYER_START_Y * TILE_SIZE
        self.current_hp = self.max_hp
        self.score = 0
        self.xp = 0
        self.level = 1
        self.is_frozen = False
        self.shield_active = False
        self.freeze_cooldown_time = 0
        self.shield_cooldown_time = 0
        self._init_cars()
        self._spawn_item()

    def activate_freeze(self):
        now = pygame.time.get_ticks()
        if now > self.freeze_cooldown_time:
            self.is_frozen = True
            self.freeze_end_time = now + 3000 
            self.freeze_cooldown_time = now + 10000 
            return True
        return False

    def activate_shield(self):
        now = pygame.time.get_ticks()
        if now > self.shield_cooldown_time:
            self.shield_active = True
            self.shield_end_time = now + 5000 
            self.shield_cooldown_time = now + 15000 
            return True
        return False

    def update_logic(self):
        now = pygame.time.get_ticks()
        if self.is_frozen and now > self.freeze_end_time:
            self.is_frozen = False
        if self.shield_active and now > self.shield_end_time:
            self.shield_active = False
        
        p_rect = pygame.Rect(self.player_x, self.player_y, TILE_SIZE, TILE_SIZE)
        for item in self.items[:]:
            if p_rect.colliderect(pygame.Rect(item['x'], item['y'], TILE_SIZE, TILE_SIZE)):
                if item['type'] == "fly":
                    self.score += 50
                    self.xp += 30
                elif item['type'] == "apple":
                    self.current_hp = min(self.max_hp, self.current_hp + 25)
                self.items.remove(item)
                self._spawn_item()

        if self.xp >= self.level * 100:
            self.xp -= self.level * 100
            self.level += 1

    def move_player(self, dx, dy):
        nx, ny = self.player_x + dx * TILE_SIZE, self.player_y + dy * TILE_SIZE
        if 0 <= nx < SCREEN_WIDTH and 0 <= ny < SCREEN_HEIGHT:
            self.player_x, self.player_y = nx, ny

    def update_cars(self, speed):
        if self.is_frozen: return
        for car in self.cars:
            car[0] += car[2] * speed
            if car[0] > SCREEN_WIDTH: car[0] = -TILE_SIZE
            if car[0] < -TILE_SIZE: car[0] = SCREEN_WIDTH

    def check_collision(self):
        if self.shield_active: return False
        player_rect = pygame.Rect(self.player_x, self.player_y, TILE_SIZE, TILE_SIZE)
        for car in self.cars:
            if player_rect.colliderect(pygame.Rect(car[0], car[1], TILE_SIZE, TILE_SIZE)):
                self.current_hp -= 25
                self.player_x, self.player_y = PLAYER_START_X * TILE_SIZE, PLAYER_START_Y * TILE_SIZE
                if self.current_hp <= 0: raise GameOver()
                return True
        return False

    def check_win(self):
        if self.player_y <= 0:
            self.score += 100
            self.xp += 40
            self.player_x, self.player_y = PLAYER_START_X * TILE_SIZE, PLAYER_START_Y * TILE_SIZE
            return True
        return False
        level_time = (pygame.time.get_ticks() - self.start_time) / 1000
        print(f"Рівень пройдено за: {level_time} сек")
        self.start_time = pygame.time.get_ticks()

    def _init_cars(self):
        self.cars = []
        for lane_y in ROAD_LANES:
            direction = random.choice([1, -1])
            self.cars.append([float(random.randint(0, SCREEN_WIDTH)), float(lane_y * TILE_SIZE), direction])

    def _spawn_item(self):
        lane = random.choice(ROAD_LANES + [6])
        x = random.randint(0, (SCREEN_WIDTH // TILE_SIZE) - 1) * TILE_SIZE
        item_type = "apple" if random.random() < 0.2 else "fly"
        self.items = [{'x': x, 'y': lane * TILE_SIZE, 'type': item_type}]

    @property
    def rank(self):
        if self.level < 3: return "Новичок"
        if self.level < 6: return "Мастер"
        return "Легенда"