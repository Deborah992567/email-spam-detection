"""
User management router.
"""
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.connection import get_db
from backend.app.models.models import User, EmailAnalysis
from backend.app.schemas.schemas import UserResponse, UserUpdate
from backend.app.auth.auth import get_current_user, hash_password, verify_password

router = APIRouter(prefix="/api/users", tags=["Users"])


class PasswordChangeRequest(BaseModel):
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=6, max_length=128, description="New password")


@router.get("/me", response_model=UserResponse, summary="Get current user profile")
def get_profile(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)


@router.get("/me/stats", summary="Get current user's analysis statistics")
def my_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    total = db.query(EmailAnalysis).filter(EmailAnalysis.user_id == current_user.id).count()
    spam = db.query(EmailAnalysis).filter(
        EmailAnalysis.user_id == current_user.id,
        EmailAnalysis.prediction == "spam",
    ).count()
    ham = db.query(EmailAnalysis).filter(
        EmailAnalysis.user_id == current_user.id,
        EmailAnalysis.prediction == "ham",
    ).count()
    return {
        "total": total,
        "spam": spam,
        "ham": ham,
        "member_since": current_user.created_at.isoformat() if current_user.created_at else None,
    }


@router.put("/me", response_model=UserResponse, summary="Update current user profile")
def update_profile(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if data.name is not None:
        current_user.name = data.name
    if data.email is not None:
        existing = db.query(User).filter(
            User.email == data.email, User.id != current_user.id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
        current_user.email = data.email

    db.commit()
    db.refresh(current_user)
    return UserResponse.model_validate(current_user)


@router.put("/me/password", summary="Change password")
def change_password(
    data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not verify_password(data.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    current_user.password_hash = hash_password(data.new_password)
    db.commit()
    return {"message": "Password updated successfully"}
