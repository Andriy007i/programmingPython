import pygame
import time
import math
from game_engine.core import Engine, GameOver
from config import *

class FroggerGame:
    def __init__(self):
        pygame.init()
        # Збільшуємо висоту екрана на 100 пікселів для нижньої панелі
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 100))
        pygame.display.set_caption("Frogger: Pro Edition")
        self.clock = pygame.time.Clock()
        
        self.font = pygame.font.SysFont("Verdana", 28, bold=True)
        self.small_font = pygame.font.SysFont("Verdana", 14, bold=True)
        self.ui_font = pygame.font.SysFont("Courier New", 16, bold=True)
        
        self.game_engine = Engine(SCREEN_WIDTH // TILE_SIZE, SCREEN_HEIGHT // TILE_SIZE)
        self.running, self.game_over = True, False
        self.msg, self.msg_t = "", 0

        self._create_assets()

    def _create_assets(self):
        # Гравець (Жаба)
        self.img_player = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.ellipse(self.img_player, (50, 205, 50), (5, 8, 40, 35))
        pygame.draw.circle(self.img_player, WHITE, (15, 15), 6)
        pygame.draw.circle(self.img_player, WHITE, (35, 15), 6)
        pygame.draw.circle(self.img_player, BLACK, (15, 15), 3)
        pygame.draw.circle(self.img_player, BLACK, (35, 15), 3)

        # Машина (Спортивна)
        self.img_car = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(self.img_car, (220, 20, 60), (5, 12, 40, 26), border_radius=5)
        pygame.draw.rect(self.img_car, (30, 30, 30), (10, 15, 30, 20), border_radius=3)
        pygame.draw.rect(self.img_car, (173, 216, 230), (32, 18, 8, 14)) # Лобове скло

        # Ресурси
        self.img_fly = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.img_fly, GOLD, (15, 15), 8)
        self.img_apple = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.img_apple, RED, (15, 15), 10)

    def set_message(self, text, dur=1.5):
        self.msg, self.msg_t = text, time.time() + dur

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if self.game_over and event.key == pygame.K_SPACE:
                    self.game_engine.reset_game()
                    self.game_over = False
                    self.msg = ""
                elif not self.game_over:
                    if event.key == pygame.K_UP:    self.game_engine.move_player(0, -1)
                    if event.key == pygame.K_DOWN:  self.game_engine.move_player(0, 1)
                    if event.key == pygame.K_LEFT:  self.game_engine.move_player(-1, 0)
                    if event.key == pygame.K_RIGHT: self.game_engine.move_player(1, 0)
                    
                    if event.key == pygame.K_RETURN: # ENTER - Заморозка
                        if self.game_engine.activate_freeze():
                            self.set_message("TIME FROZEN! ❄️")
                    if event.key == pygame.K_SPACE:  # SPACE - Щит
                        if self.game_engine.activate_shield():
                            self.set_message("SHIELD ACTIVE! 🛡️")

    def _draw_bottom_panel(self):
        # Панель займає низ екрана
        panel_rect = pygame.Rect(0, SCREEN_HEIGHT, SCREEN_WIDTH, 100)
        pygame.draw.rect(self.screen, (20, 20, 25), panel_rect)
        pygame.draw.line(self.screen, (100, 100, 100), (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT), 3)

        # 1. Секція HP (Зліва)
        hp_ratio = self.game_engine.current_hp / 100
        pygame.draw.rect(self.screen, (60, 0, 0), (20, SCREEN_HEIGHT + 20, 200, 25))
        pygame.draw.rect(self.screen, (0, 255, 100), (20, SCREEN_HEIGHT + 20, int(200 * hp_ratio), 25))
        self.screen.blit(self.ui_font.render(f"HEALTH: {self.game_engine.current_hp}%", True, WHITE), (20, SCREEN_HEIGHT + 50))

        # 2. Секція XP та Рівень (По центру)
        xp_ratio = self.game_engine.xp / (self.game_engine.level * 100)
        pygame.draw.rect(self.screen, (40, 40, 50), (250, SCREEN_HEIGHT + 20, 200, 15))
        pygame.draw.rect(self.screen, (160, 32, 240), (250, SCREEN_HEIGHT + 20, int(200 * xp_ratio), 15))
        lvl_info = f"LVL: {self.game_engine.level} | {self.game_engine.rank}"
        self.screen.blit(self.ui_font.render(lvl_info, True, CYAN), (250, SCREEN_HEIGHT + 45))
        self.screen.blit(self.ui_font.render(f"SCORE: {self.game_engine.score}", True, GOLD), (250, SCREEN_HEIGHT + 65))

        # 3. Секція Скілів (Справа)
        now = pygame.time.get_ticks()
        skills = [
            ("FREEZE[Ent]", self.game_engine.is_frozen, self.game_engine.freeze_end_time, self.game_engine.freeze_cooldown_time, CYAN),
            ("SHIELD[Spc]", self.game_engine.shield_active, self.game_engine.shield_end_time, self.game_engine.shield_cooldown_time, (200, 50, 255))
        ]

        for i, (name, active, end, cd, clr) in enumerate(skills):
            x_off = 480 + (i * 160)
            self.screen.blit(self.small_font.render(name, True, WHITE), (x_off, SCREEN_HEIGHT + 15))
            
            # Малюємо прогрес-бар скіла
            bar_color = clr if active else (80, 80, 80)
            if active:
                w = int(120 * ((end - now) / (3000 if i==0 else 5000)))
                status = "ACTIVE"
            else:
                wait = max(0, (cd - now) / 1000)
                w = 120 if wait <= 0 else int(120 * (1 - wait / (10 if i==0 else 15)))
                status = "READY" if wait <= 0 else f"{wait:.1f}s"
            
            pygame.draw.rect(self.screen, (30, 30, 30), (x_off, SCREEN_HEIGHT + 40, 120, 10))
            pygame.draw.rect(self.screen, bar_color, (x_off, SCREEN_HEIGHT + 40, w, 10))
            self.screen.blit(self.small_font.render(status, True, WHITE), (x_off, SCREEN_HEIGHT + 55))

    def _draw_elements(self):
        # Ігрове поле
        game_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        game_surf.fill((35, 35, 40))

        # Трава та дорога
        for r in range(self.game_engine.height_tiles):
            if r in [0, 6, 9]:
                pygame.draw.rect(game_surf, (30, 80, 30), (0, r*TILE_SIZE, SCREEN_WIDTH, TILE_SIZE))
            else:
                pygame.draw.line(game_surf, (55, 55, 60), (0, r*TILE_SIZE), (SCREEN_WIDTH, r*TILE_SIZE), 1)

        # Предмети
        for item in self.game_engine.items:
            img = self.img_fly if item['type'] == "fly" else self.img_apple
            game_surf.blit(img, (item['x']+10, item['y']+10))

        # Машини
        for car in self.game_engine.cars:
            img = self.img_car
            if car[2] == -1: img = pygame.transform.flip(img, True, False)
            game_surf.blit(img, (int(car[0]), int(car[1])))

        # Щит
        if self.game_engine.shield_active:
            pulse = int((math.sin(time.time() * 15) + 1) * 3)
            pygame.draw.circle(game_surf, (200, 50, 255), (self.game_engine.player_x+25, self.game_engine.player_y+25), 40 + pulse, 3)

        # Гравець
        game_surf.blit(self.img_player, (self.game_engine.player_x, self.game_engine.player_y))
        
        # Виводимо ігрове поле на основний екран
        self.screen.blit(game_surf, (0, 0))
        
        # Малюємо нижню панель
        self._draw_bottom_panel()

        # Повідомлення
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT + 100), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 220))
            self.screen.blit(overlay, (0, 0))
            txt = self.font.render("GAME OVER! [SPACE TO RESTART]", True, RED)
            self.screen.blit(txt, (SCREEN_WIDTH//2 - txt.get_width()//2, SCREEN_HEIGHT//2))
        elif time.time() < self.msg_t:
            txt = self.font.render(self.msg, True, YELLOW)
            self.screen.blit(txt, (SCREEN_WIDTH//2 - txt.get_width()//2, 100))

        pygame.display.flip()

    def run(self):
        while self.running:
            self._handle_input()
            if not self.game_over:
                self.game_engine.update_logic()
                self.game_engine.update_cars(CAR_SPEED)
                try:
                    if self.game_engine.check_collision(): self.set_message("HIT! -25 HP")
                    if self.game_engine.check_win(): self.set_message("VICTORY! +XP")
                except GameOver:
                    self.game_over = True
            self._draw_elements()
            self.clock.tick(FPS)
        pygame.quit()

    if __name__ == "__main__":
        FroggerGame().run()