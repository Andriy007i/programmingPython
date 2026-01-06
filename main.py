import os
import random

# 1. Глобальні змінні (Global scope)
GAME_TITLE = "FROGGER: ULTIMATE SURVIVAL"
HIGH_SCORE_FILE = "highscore.txt"

def load_high_score():
    """Вбудована функція відкриття файлу та обробка винятків."""
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0

def play_game(level_difficulty=1.0):
    # 2. Початкові дані
    # Траса (str), де 'M' - машина, '.' - дорога, 'G' - мета, 'T' - тротуар
    world_map = [
        "GGGGGGGGGG",
        "TTTTTTTTTT",
        "M.M.M.M.M.",  # Смуга руху 1
        ".M.M.M.M.M",  # Смуга руху 2
        "TTTTTTTTTT",
        "TTTTPTTTTT"   # P - гравець
    ]
    
    # Перетворюємо рядки у списки для можливості зміни (Mutable)
    grid = [list(row) for row in world_map]
    player_pos = [5, 4]  # [row, col]
    score = 0
    is_alive = True

    # 3. Вкладена функція (Nested function) для перевірки колізій
    def is_collision(r, c):
        # Використання виразу a < b < c (Requirement)
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
            return grid[r][c] == 'M'
        return False

    # 4. Функція з * та / (Special parameters)
    def update_world(step_count, /, *, speed=1):
        """Зсуває машини на дорозі після кожного кроку."""
        nonlocal grid  # Використання nonlocal (Requirement)
        for r in range(2, 4):  # Тільки ряди з дорогою
            if r == 2: # Машини їдуть вправо
                grid[r] = grid[r][-1:] + grid[r][:-1]
            else: # Машини їдуть вліво
                grid[r] = grid[r][1:] + grid[r][:1]

    # 5. Лямбда-вираз для швидкого відображення символів
    get_icon = lambda char: "🚗" if char == 'M' else ("🟩" if char == 'T' else ("🏆" if char == 'G' else "⬛"))

    def render():
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"=== {GAME_TITLE} | SCORE: {score} ===")
        
        for r in range(len(grid)):
            row_str = ""
            for c in range(len(grid[0])):
                if [r, c] == player_pos:
                    row_str += "🐸"
                else:
                    row_str += get_icon(grid[r][c])
            print(row_str)
        print("\nУправління: W, A, S, D (Enter для підтвердження). Q - вихід.")

    # 6. Основний ігровий цикл
    while is_alive:
        render()
        move = input("Ваш хід: ").lower()

        if move == 'q':
            break
        
        # Логіка руху
        dr, dc = 0, 0
        if move == 'w': dr = -1
        elif move == 's': dr = 1
        elif move == 'a': dc = -1
        elif move == 'd': dc = 1
        else: continue # Пропуск ітерації (Requirement)

        new_r, new_c = player_pos[0] + dr, player_pos[1] + dc

        # Перевірка меж та перешкод
        if 0 <= new_r < len(grid) and 0 <= new_c < len(grid[0]):
            player_pos = [new_r, new_c]
            update_world(1, speed=2) # Виклик з keyword argument
            
            # Перевірка на смерть або перемогу
            if is_collision(player_pos[0], player_pos[1]):
                render()
                print("БЕМС! Вас збила машина! 💀")
                is_alive = False
            elif grid[player_pos[0]][player_pos[1]] == 'G':
                score += 100
                render()
                print(f"ПЕРЕМОГА! Ви пройшли рівень! Рахунок: {score} 🎉")
                break
        else:
            print("Там стіна!")
    
    return score

def main():
    """Головна точка входу."""
    high_score = load_high_score()
    print(f"Попередній рекорд: {high_score}")
    
    current_score = play_game()
    
    if current_score > high_score:
        print(f"НОВИЙ РЕКОРД: {current_score}!")
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(current_score))

if __name__ == "__main__":
    main()
