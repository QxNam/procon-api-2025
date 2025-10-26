from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from typing import List, Dict, Any

# Giả định Model ORM của bạn được import từ app/models/models.py
from app.models.models import User, Submission 


async def get_current_ranking(db: AsyncSession, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Hàm bất đồng bộ truy vấn DB, tính toán tổng điểm và trả về bảng xếp hạng.
    """
    
    # Định nghĩa câu lệnh SELECT
    stmt = select(
        User.username,
        func.sum(Submission.score).label("total_score"),
        func.avg(Submission.time_running).label("avg_time")
    ).join(
        Submission, User.id == Submission.user_id
    ).group_by(
        User.username
    ).order_by(
        func.sum(Submission.score).desc() # Sắp xếp giảm dần theo tổng điểm
    ).limit(limit)
    
    # Thực thi truy vấn bất đồng bộ
    result = await db.execute(stmt)
    results = result.all() 
    
    # Xử lý kết quả
    ranking_data = []
    for rank, (username, total_score, avg_time) in enumerate(results):
        ranking_data.append({
            "rank": rank + 1,
            "username": username,
            "score": round(float(total_score) if total_score is not None else 0.0, 2), 
            "time": round(float(avg_time) if avg_time is not None else 0.0, 2)
        })
        
    return ranking_data
