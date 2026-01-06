import os

# Глобальна змінна для налаштувань (демонстрація global)
GAME_TITLE = "Frogger Console Edition"
SCORE = 0

def start_game():
    # Поле: # - стіна, . - дорога, G - мета (Goal), T - тротуар, P - гравець
    # Рядки str для ігрового поля
    level_map = [
        "GGGGGGGGGG",
        "TTTTTTTTTT",
        "..........", # Дорога 1
        "..........", # Дорога 2
        "TTTTTTTTTT",
        "PTTTTTTTTT"  # Старт
    ]
    
    player_pos = [5, 0] # Рядок, Стовпчик
    is_running = True

    # Вкладена функція (Nested function)
    def check_bounds(r, c):
        # Використання виразу виду a < b < c
        return 0 <= r < len(level_map) and 0 <= c < len(level_map[0])

    # Функція з keyword arguments та використанням / (positional-only)
    def render_screen(msg="Рухайтеся до G!", /):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"--- {GAME_TITLE} ---")
        for r_idx, row in enumerate(level_map):
            display_row = ""
            for c_idx, char in enumerate(row):
                if r_idx == player_pos[0] and c_idx == player_pos[1]:
                    display_row += "🐸"
                else:
                    display_row += char
            print(display_row)
        print(f"Рахунок: {SCORE}")
        print(msg)

    # Функція для руху (демонстрація nonlocal)
    def move_player(direction):
        nonlocal player_pos
        global SCORE
        
        dr, dc = 0, 0
        # Лямбда-вираз для перевірки символу
        get_tile = lambda r, c: level_map[r][c]

        if direction == 'w': dr = -1
        elif direction == 's': dr = 1
        elif direction == 'a': dc = -1
        elif direction == 'd': dc = 1
        else: return # Некоректна клавіша

        new_r, new_c = player_pos[0] + dr, player_pos[1] + dc

        # Логічні операції and, or, not + перевірка меж
        if not check_bounds(new_r, new_c) or get_tile(new_r, new_c) == "#":
            return
        
        player_pos[0], player_pos[1] = new_r, new_c
        
        # Перевірка умови виграшу (Приз)
        if get_tile(new_r, new_c) == "G":
            SCORE += 100
            return "WIN"
        return None

    # Ігровий цикл (while)
    while is_running:
        render_screen()
        key = input("Введіть (W/A/S/D): ").lower()
        
        if key == 'q': 
            break # break
            
        result = move_player(key)
        
        if result == "WIN":
            render_screen("ВИТАЮ! Ви дісталися мети!")
            break
        
        # Використання range та for для "анімації" (імітація)
        for _ in range(1):
            if SCORE < 0:
                continue # continue
    else:
        # else для циклу (виконається, якщо не було break)
        print("Гра завершена.")

# Запуск
if __name__ == "__main__":
    start_game()
