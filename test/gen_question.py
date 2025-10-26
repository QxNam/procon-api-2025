import numpy as np
import json
import os
import random
from random import randint, shuffle, seed
from datetime import datetime

MIN_SIZE = 4
MAX_SIZE = 24

os.makedirs("questions", exist_ok=True)

def generate_board(n: int, chaos: float = 1.0) -> np.ndarray:
    """
    Sinh bảng n×n, mỗi số xuất hiện đúng 2 lần.
    chaos = 0.0 → các cặp gần nhau (dễ)
    chaos = 1.0 → hoàn toàn ngẫu nhiên (khó)
    """
    assert n % 2 == 0, "n must be even"
    num_values = (n * n) // 2
    values = [randint(0, num_values - 1) for _ in range(n*n)]

    # Mức độ rối: hoán đổi ít hoặc nhiều
    shuffle(values)
    board = np.array(values).reshape(n, n)

    if chaos < 1.0:
        # Giảm độ rối: ép một phần cặp gần nhau
        num_pairs_to_relocate = int(num_values * (1 - chaos))
        for _ in range(num_pairs_to_relocate):
            v = randint(0, num_values - 1)
            # tìm 2 vị trí của v
            positions = np.argwhere(board == v)
            if len(positions) == 2:
                (x1, y1), (x2, y2) = positions
                # di chuyển 1 ô sao cho gần ô còn lại
                nx = min(n - 1, max(0, x1 + random.choice([-1, 0, 1])))
                ny = min(n - 1, max(0, y1 + random.choice([-1, 0, 1])))
                board[x2, y2], board[nx, ny] = board[nx, ny], board[x2, y2]

    return board


def generate_problem(level: str = "medium", seed_value: int | None = None) -> dict:
    """
    Sinh đề ở nhiều mức độ:
    - easy: n nhỏ, chaos thấp
    - medium: n trung bình, chaos vừa
    - hard: n lớn, chaos cao
    - extreme: n rất lớn, chaos cao nhất
    """
    if seed_value is not None:
        seed(seed_value)
        np.random.seed(seed_value)

    level = level.lower()
    if level == "easy":
        n = random.choice([4, 6, 8])
        chaos = 0.2
    elif level == "medium":
        n = random.choice([8, 10, 12])
        chaos = 0.5
    elif level == "hard":
        n = random.choice([12, 16, 20])
        chaos = 0.8
    elif level == "extreme":
        n = random.choice([20, 22, 24])
        chaos = 1.0
    else:
        raise ValueError("level must be easy/medium/hard/extreme")

    board = generate_board(n, chaos)
    return {
        "startsAt": 0,
        "problem": {
            "field": {
                "size": n,
                "entities": board.tolist()
            }
        }
    }


def save_problem_json(problem: dict, filename: str | None = None):
    """Lưu ra file JSON."""
    if not filename:
        t = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"problem_{t}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(problem, f, ensure_ascii=False, indent=4)
    print(f"✅ Problem saved to {filename}")


if __name__ == "__main__":
    # Ví dụ sinh 4 mức độ
    i = 1
    n_sample = 5

    for lvl in ["easy", "medium", "hard", "extreme"]:
        for _ in range(n_sample):
            prob = generate_problem(lvl)
            save_problem_json(prob, f"questions/{i}.json")
            i += 1
