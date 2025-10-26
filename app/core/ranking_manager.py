from fastapi import WebSocket
from typing import List
import json
import asyncio

from app.services.ranking import get_current_ranking 
from app.core.database import async_session 

class RankingConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.broadcast_task = None # Dùng để quản lý vòng lặp nền

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            # Dùng asyncio.gather để gửi tin nhắn song song, hiệu quả hơn
            await connection.send_text(message) 

    async def start_broadcast_loop(self):
        """Vòng lặp định kỳ truy vấn DB và broadcast dữ liệu (ASYNC)."""
        while True:
            await asyncio.sleep(5) # Cập nhật mỗi 5 giây
            
            # Sử dụng async_session và cú pháp async with
            async with async_session() as db:
                try:
                    # Lấy dữ liệu xếp hạng từ service
                    ranking_data = await get_current_ranking(db, limit=20) 
                    message = json.dumps(ranking_data)
                    
                    if ranking_data:
                        await self.broadcast(message)
                except Exception as e:
                    # Rất quan trọng để bắt lỗi trong background task
                    print(f"LỖI trong background broadcast loop: {e}") 

# Khởi tạo một instance duy nhất của Manager
ranking_manager = RankingConnectionManager()
