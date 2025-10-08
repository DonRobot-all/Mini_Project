import os
import time
import random
import math

# -------------------------------
# Настройки
# -------------------------------
WIDTH = 20
HEIGHT = 15
FRAME_DELAY = 0.1  # базовая задержка между кадрами
EXP_GROWTH = 1.08  # коэффициент экспоненциального роста сложности

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

# -------------------------------
# Функции
# -------------------------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def draw():
    canvas = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # рисуем объекты
    for o in objects:
        if 0 <= int(o["y"]) < HEIGHT:
            canvas[int(o["y"])][o["x"]] = "*"

    # рисуем игрока
    for i in range(player["w"]):
        px = player["x"] + i - player["w"] // 2
        if 0 <= px < WIDTH:
            canvas[player["y"]][px] = "@"

    clear()
    for row in canvas:
        print("".join(row))
    print(f"Score: {score} | Level: {level:.1f} | Speed: {base_speed:.2f}")

def intersects(a, b):
    """AABB-проверка столкновений"""
    return (
        a["x"] - a["w"]/2 < b["x"] + b["w"]/2 and
        a["x"] + a["w"]/2 > b["x"] - b["w"]/2 and
        a["y"] < b["y"] + b["h"] and
        a["y"] + a["h"] > b["y"]
    )

def update_objects():
    global score, level, base_speed

    caught = []
    missed = []

    for o in objects:
        o["y"] += o["speed"]
        if o["y"] >= player["y"] - 0.5 and intersects(player, o):
            caught.append(o)
        elif o["y"] >= HEIGHT:
            missed.append(o)

    # обновляем счёт
    for c in caught:
        score += 1
        # растёт сложность экспоненциально
        level += 0.2
        base_speed = base_speed * EXP_GROWTH

    # удаляем пойманные и пропущенные
    for o in caught + missed:
        if o in objects:
            objects.remove(o)

def spawn_objects():
    global spawn_accumulator
    spawn_accumulator += base_spawn_rate * (EXP_GROWTH ** level)

    if spawn_accumulator >= 1:
        spawn_accumulator = 0
        new_obj = {
            "x": random.randint(0, WIDTH - 1),
            "y": 0,
            "w": 1,
            "h": 1,
            "speed": base_speed
        }
        objects.append(new_obj)

def move_player(direction):
    if direction == "a":
        player["x"] = max(player["x"] - 1, player["w"] // 2)
    elif direction == "d":
        player["x"] = min(player["x"] + 1, WIDTH - player["w"] // 2 - 1)

# -------------------------------
# Главный цикл игры
# -------------------------------
try:
    while True:
        draw()
        spawn_objects()
        update_objects()

        print("← a | → d | q - выход")
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
