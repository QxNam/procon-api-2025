from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.ranking_manager import get_current_ranking
import asyncio
import json

router = APIRouter(
    prefix="/ws",
    tags=["WebSocket"],
)

# @router.websocket("/ranking") # Đường dẫn hoàn chỉnh sẽ là /v1/ranking (nếu include router)
# async def websocket_ranking_endpoint(websocket: WebSocket):
#     await ranking_manager.connect(websocket)
#     try:
#         # Giữ kết nối mở, client có thể gửi ping/message nếu cần
#         while True:
#             await websocket.receive_text() 
#     except WebSocketDisconnect:
#         ranking_manager.disconnect(websocket)
#         print("Client ranking disconnected.")

@router.websocket("/rank")
async def websocket_rank(websocket: WebSocket, db: AsyncSession = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            ranking = await get_current_ranking(db, limit=20)
            await websocket.send_text(json.dumps(ranking, ensure_ascii=False))
            await asyncio.sleep(5)  # Cập nhật mỗi 5 giây
    except WebSocketDisconnect:
        print("❌ Client disconnected")
