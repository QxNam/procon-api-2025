from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession # Cần thiết để type hint
from app.core.database import get_db # Import dependency
from app.core.ranking_manager import get_current_ranking

router = APIRouter(
    prefix="/rank",
    tags=["Web UI - Ranking"],
)

# Giả định templates đã được thiết lập ở main.py hoặc dùng cách này:
templates = Jinja2Templates(directory="app/templates")

@router.get("/user", response_class=HTMLResponse)
async def get_ranking_page(
    request: Request, 
    # Inject AsyncSession vào router bằng Depends
    db: AsyncSession = Depends(get_db) 
):
    """Render trang bảng xếp hạng với dữ liệu ban đầu từ DB."""
    
    # 1. Gọi hàm service đã được chuyển thành async
    # Lưu ý: Không cần try/finally db.close() vì get_db đã làm điều đó với context manager (async with)
    initial_ranking = await get_current_ranking(db, limit=20)
    
    return templates.TemplateResponse(
        "ranking.html",
        {"request": request, "ranking": initial_ranking, "title": "Bảng Xếp Hạng Real-time"}
    )

# @router.get("/submit", response_class=HTMLResponse)
# async def get_submit_page(
#     request: Request, 
#     # Inject AsyncSession vào router bằng Depends
#     db: AsyncSession = Depends(get_db) 
# ):
#     """Render trang bảng xếp hạng với dữ liệu ban đầu từ DB."""
    
#     # 1. Gọi hàm service đã được chuyển thành async
#     # Lưu ý: Không cần try/finally db.close() vì get_db đã làm điều đó với context manager (async with)
#     initial_ranking = await get_current_ranking(db, limit=20)
    
#     return templates.TemplateResponse(
#         "ranking.html",
#         {"request": request, "ranking": initial_ranking, "title": "Bảng Xếp Hạng Real-time"}
#     )


