STEP_FACTOR = 1.0

def rotate_subsquare(board, x, y, k):
    '''
    Rotate a k x k subsquare of the board 90 degrees clockwise.
    Args:
        board (list of list of int): The board state.
        x (int): The starting x-coordinate of the subsquare.
        y (int): The starting y-coordinate of the subsquare.
        k (int): The size of the subsquare.
    '''
    sub = [row[y:y+k] for row in board[x:x+k]]
    rotated = list(zip(*sub[::-1]))
    for i in range(k):
        for j in range(k):
            board[x+i][y+j] = rotated[i][j]

def count_pairs(board) -> int:
    '''
    Count the number of adjacent pairs in the board.
    Args:
        board (list of list of int): The board state.
    Returns:
        int: The count of adjacent pairs.
    '''
    n = len(board)
    count = 0
    for i in range(n):
        for j in range(n):
            if j + 1 < n and board[i][j] == board[i][j+1]:
                count += 1
            if i + 1 < n and board[i][j] == board[i+1][j]:
                count += 1
    return count

def judge(problem: dict, ops: list, simulate:str=False) -> dict:
    '''
    Evaluate the final board state after applying operations and return the pair count.
    Args:
        problem (dict): The problem definition containing the initial board state.
        ops (list): A list of operations to apply to the board.
    Returns:
        dict: A dictionary containing the final board state, the simulation steps, and the pair count.
    '''
    from copy import deepcopy
    board = deepcopy(problem['entities'])
    simulation = [
        {
            "step": 0, 
            "op": None,
            "board": deepcopy(board)
        }
    ]
    n = problem['size']
    for i, op in enumerate(ops, start=1):
        if not (2 <= op['n'] <= n):
            raise ValueError(f"Invalid n={op['n']}")
        if op['x'] + op['n'] > n or op['y'] + op['n'] > n:
            raise ValueError("Rotation out of bounds")
        rotate_subsquare(board, op['x'], op['y'], op['n'])
        if simulate:
            simulation.append(
                {
                    "step": i, 
                    "op": op,
                    "board": deepcopy(board)
                }
            )

    return {
        "final_board": board,
        "simulation": simulation,
        "pair_count": count_pairs(board)
    }

def score_evaluation(problem_id:int, score:int, step_count:int, time_running:float) -> float:
    STEP_FACTOR = problem_id
    return score*STEP_FACTOR + (1 + 1/step_count) + 1/time_running
