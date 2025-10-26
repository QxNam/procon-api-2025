from pydantic import BaseModel
from fastapi import APIRouter, Depends, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.services.judge_simulate import get_problem_and_judge

# Giả định templates đã được setup
templates = Jinja2Templates(directory="app/templates")
router = APIRouter(
    prefix="/simulation",
    tags=["Web UI - Simulation"],
)

class Operation(BaseModel):
    x: int = Field(..., description="Start x-coordinate (row index)")
    y: int = Field(..., description="Start y-coordinate (column index)")
    n: int = Field(..., description="Subsquare size (k) to rotate")

class SimulationInput(BaseModel):
    starts_at: int
    ops: List[Operation]
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "starts_at": 1700000000,
                "ops": [
                    { "x": 0, "y": 0, "n": 2 }, # Rotate 2x2 at (0, 0)
                    { "x": 1, "y": 1, "n": 3 }  # Rotate 3x3 at (1, 1)
                ]
            }
        }
    }

# Giả định templates đã được setup
templates = Jinja2Templates(directory="app/templates")
router = APIRouter()


@router.get("/simulation", response_class=HTMLResponse)
async def get_simulation_ui(request: Request):
    """Render giao diện nhập liệu simulation."""
    # Không cần load board, UI này chỉ để nhập liệu
    return templates.TemplateResponse(
        "simulation.html",
        {"request": request, "title": "Game Simulation UI"}
    )


@router.post("/simulation/run")
async def run_simulation_logic(
    data: SimulationInput, 
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    
    try:
        # Gọi hàm judge đã được sửa đổi để trả về các bước simulation
        result = await get_problem_and_judge(db, data.starts_at, [op.model_dump() for op in data.ops])
        
        # Trả về các bước simulation để frontend tạo animation
        return {
            "status": "success",
            "simulation_steps": result['simulation_steps']
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred during simulation.")
    