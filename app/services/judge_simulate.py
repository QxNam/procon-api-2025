# app/services/judge.py

from copy import deepcopy
from typing import List, Dict, Any, Optional

# Cần thiết cho async DB
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Import Question Model (Giả định nằm trong app/models/models.py)
from app.models.models import Question 

# --- HÀM HỖ TRỢ LOGIC ---

def rotate_subsquare(board, x, y, k):
    ''' Xoay một khối con k x k 90 độ theo chiều kim đồng hồ. '''
    sub = [row[y:y+k] for row in board[x:x+k]]
    # Xoay ma trận 90 độ (bằng cách đảo ngược hàng rồi chuyển vị)
    rotated = list(zip(*sub[::-1])) 
    for i in range(k):
        for j in range(k):
            # Lưu ý: 'rotated' là tuple của tuple, cần truy cập theo chỉ mục
            board[x+i][y+j] = rotated[i][j]

def count_pairs(board) -> int:
    ''' Đếm số cặp phần tử liền kề bằng nhau trên bảng. '''
    n = len(board)
    count = 0
    for i in range(n):
        for j in range(n):
            # Kiểm tra hàng ngang
            if j + 1 < n and board[i][j] == board[i][j+1]:
                count += 1
            # Kiểm tra hàng dọc
            if i + 1 < n and board[i][j] == board[i+1][j]:
                count += 1
    return count

# --- HÀM CHÍNH XỬ LÝ LOGIC ---

async def get_problem_and_judge(
    db: AsyncSession, 
    starts_at: int, 
    ops: List[Dict[str, int]]
) -> Dict[str, Any]:
    '''
    Tìm problem theo startsAt, chạy logic judge và trả về các bước simulation.
    '''
    
    # 1. Tải Question/Problem từ DB (sử dụng startsAt)
    stmt = select(Question).where(Question.startsAt == starts_at)
    result = await db.execute(stmt)
    problem_obj: Optional[Question] = result.scalars().first()

    if not problem_obj:
        raise ValueError(f"Problem with startsAt={starts_at} not found.")

    # Giả định problem['content'] chứa 'entities' (trạng thái board ban đầu) và 'size'
    problem = {
        'entities': problem_obj.content.get('problem').get('field').get('entities'), 
        'size': problem_obj.size
    }
    
    # 2. Bắt đầu Judge/Simulation
    board = deepcopy(problem['entities'])
    n = problem['size']

    # Danh sách các bước simulation để gửi về frontend
    simulation_steps = [
        {
            "step": 0,
            "op": None,
            "board": deepcopy(board)
        }
    ]

    for i, op in enumerate(ops, start=1):
        x, y, k = op['x'], op['y'], op['n']
        
        # Kiểm tra ràng buộc
        if not (2 <= k <= n):
            raise ValueError(f"Invalid subsquare size k={k}")
        if x + k > n or y + k > n:
            raise ValueError("Rotation out of bounds")

        rotate_subsquare(board, x, y, k)
        
        # Ghi lại trạng thái board và thao tác sau mỗi bước
        simulation_steps.append(
            {
                "step": i,
                "op": op,
                "board": deepcopy(board),
                "pair_count_after": count_pairs(board) # Đếm cặp sau thao tác
            }
        )

    return {
        "final_board": board,
        "simulation_steps": simulation_steps,
        "pair_count": count_pairs(board)
    }