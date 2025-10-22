import os
import time
import random
import math

# -------------------------------
# Настройки
# -------------------------------
WIDTH = 20
HEIGHT = 15
FRAME_DELAY = 0.1
EXP_GROWTH = 1.08
TRAP_CHANCE = 0.2          # вероятность появления ловушки
FREEZE_DURATION = 2         # сколько ходов игрок стоит на месте
TRAP_BLINK_TIME = 4         # сколько кадров ловушка мигает перед падением

# ANSI цвета (работает в большинстве терминалов)
RED = "\033[91m"
RESET = "\033[0m"

# -------------------------------
# Игровые объекты
# -------------------------------
player = {"x": WIDTH // 2, "y": HEIGHT - 1, "w": 3, "h": 1}
objects = []
score = 0
level = 1
base_spawn_rate = 0.15
base_speed = 0.3
spawn_accumulator = 0
frozen_steps = 0

# -------------------------------
# Вспомогательные функции
# -------------------------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def draw():
    canvas = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for o in objects:
        if 0 <= int(o["y"]) < HEIGHT:
            if o["is_trap"]:
                # Если ловушка мигает — показываем красный восклицательный знак
                if o.get("blink_timer", 0) > 0:
                    if o["blink_timer"] % 2 == 0:
                        canvas[int(o["y"])][o["x"]] = f"{RED}!{RESET}"
                else:
                    # уже падает — невидима
                    pass
            else:
                canvas[int(o["y"])][o["x"]] = "*"

    # игрок
    for i in range(player["w"]):
        px = player["x"] + i - player["w"] // 2
        if 0 <= px < WIDTH:
            canvas[player["y"]][px] = "@"

    clear()
    for row in canvas:
        print("".join(row))
    print(f"Score: {score} | Level: {level:.1f} | Speed: {base_speed:.2f}")
    if frozen_steps > 0:
        print(f"⛔ Игрок заморожен на {frozen_steps} ход(а)")
    print("← a | → d | q - выход")

def intersects(a, b):
    """AABB-проверка столкновений"""
    return (
        a["x"] - a["w"]/2 < b["x"] + b["w"]/2 and
        a["x"] + a["w"]/2 > b["x"] - b["w"]/2 and
        a["y"] < b["y"] + b["h"] and
        a["y"] + a["h"] > b["y"]
    )

def update_objects():
    global score, level, base_speed, frozen_steps

    caught = []
    missed = []

    for o in objects:
        # Если ловушка мигает — пока не падает
        if o["is_trap"] and o.get("blink_timer", 0) > 0:
            o["blink_timer"] -= 1
            continue

        o["y"] += o["speed"]

        if o["y"] >= player["y"] - 0.5 and intersects(player, o):
            caught.append(o)
        elif o["y"] >= HEIGHT:
            missed.append(o)

    for c in caught:
        if c["is_trap"]:
            score -= 3
            frozen_steps = FREEZE_DURATION
        else:
            score += 1
            level += 0.2
            base_speed = base_speed * EXP_GROWTH

    for o in caught + missed:
        if o in objects:
            objects.remove(o)

def spawn_objects():
    global spawn_accumulator
    spawn_accumulator += base_spawn_rate * (EXP_GROWTH ** level)

    if spawn_accumulator >= 1:
        spawn_accumulator = 0
        is_trap = random.random() < TRAP_CHANCE
        new_obj = {
            "x": random.randint(0, WIDTH - 1),
            "y": 0,
            "w": 1,
            "h": 1,
            "speed": base_speed,
            "is_trap": is_trap,
        }
        if is_trap:
            new_obj["blink_timer"] = TRAP_BLINK_TIME
        objects.append(new_obj)

def move_player(direction):
    if frozen_steps > 0:
        return
    if direction == "a":
        player["x"] = max(player["x"] - 1, player["w"] // 2)
    elif direction == "d":
        player["x"] = min(player["x"] + 1, WIDTH - player["w"] // 2 - 1)

# -------------------------------
# Главный цикл
# -------------------------------
try:
    while True:
        draw()
        spawn_objects()
        update_objects()

        if frozen_steps > 0:
            frozen_steps -= 1

        cmd = input("> ").lower()
        if cmd == "q":
            break
        elif cmd in ["a", "d"]:
            move_player(cmd)

        time.sleep(FRAME_DELAY)
except KeyboardInterrupt:
    pass

clear()
print(f"Игра окончена! Итоговый счёт: {score}")
