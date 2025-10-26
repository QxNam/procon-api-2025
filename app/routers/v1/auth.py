from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import UserCreate, Token
from app.models.models import User
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.utils.logger import create_logging
from app.core.auth import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

logger = create_logging("auth")

@router.post("/register", status_code=201)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    ''' Register a new user '''
    result = await db.execute(select(User).where(User.username == user.username))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed, password=user.password)
    db.add(new_user)
    await db.commit()

    logger.info(f"User registered: {user.username}")
    return {"msg": "User created"}

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    ''' User login to get JWT token '''
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token(data={"sub": user.username})
    logger.info(f"User login: {user.username}")
    return {"access_token": token, "token_type": "bearer"}

# Show information about current user
@router.get("/me")
async def read_current_user(current_user: User = Depends(get_current_user)):
    ''' Get current user information '''
    return {"username": current_user.username, "id": current_user.id}

# Additional endpoints for user management (optional)
@router.get("/users")
async def list_users(db: AsyncSession = Depends(get_db)):
    ''' List all users '''
    result = await db.execute(select(User))
    users = result.scalars().all()
    return [{"username": user.username} for user in users]

## delete current user
@router.delete("/remove", status_code=204)
async def delete_current_user(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    ''' Delete the current user (DB handles cascade) '''
    await db.delete(current_user) # Chỉ cần xóa user
    await db.commit()
    logger.info(f"User deleted: {current_user.username}")
    return {"msg": "User deleted"}

# @router.delete("/users", status_code=204)
# async def delete_all_users(db: AsyncSession = Depends(get_db)):
#     ''' Delete all users and all submissions '''
#     result = await db.execute(select(User))
#     users = result.scalars().all()
#     for user in users:
#         await db.delete(user)  # Xóa từng user, cascade sẽ xóa submissions
#     await db.commit()
#     logger.info("All users and their submissions deleted")
#     return {"msg": "All users and their submissions deleted"}

@router.get("/forgot-password")
async def forgot_password(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    ''' Retrieve the password for the current user (for testing purposes only) '''
    username = current_user.username
    logger.info(f"Current user: {username}")
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    password = user.password
    if not password:
        raise HTTPException(status_code=400, detail="No password stored for this user")
    logger.info(f"Password retrieval for user: {username}")
    return {"username": username, "password": password}
