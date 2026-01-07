# config.py
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
TILE_SIZE = 50
FPS = 60

# Кольори для нових елементів
GOLD = (255, 215, 0)      # Мухи (Алмази)
PURPLE = (160, 32, 240)   # Досвід (XP)
DARK_RED = (139, 0, 0)    # Яблука (HP)
CYAN = (0, 255, 255)      # Щит

ROAD_LANES = [2, 3, 4, 5, 7, 8] 
CAR_SPEED = 2.5

PLAYER_START_X = (SCREEN_WIDTH // TILE_SIZE) // 2
PLAYER_START_Y = (SCREEN_HEIGHT // TILE_SIZE) - 1
LIVES_START = 3

# Кольори стандартні
WHITE, BLACK, GREEN, RED, YELLOW, BLUE = (255,255,255), (0,0,0), (0,255,0), (255,0,0), (255,255,0), (0,0,255)