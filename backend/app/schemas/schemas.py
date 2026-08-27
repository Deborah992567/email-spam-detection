"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    email: Optional[EmailStr] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class AnalysisRequest(BaseModel):
    sender: Optional[str] = Field(None, max_length=255)
    subject: Optional[str] = Field(None, max_length=500)
    body: str = Field(..., min_length=1, max_length=50000)


class AnalysisResponse(BaseModel):
    id: int
    sender: Optional[str]
    subject: Optional[str]
    body: str
    prediction: str
    confidence: float
    risk_level: str
    indicators: Optional[List[Dict[str, str]]] = None
    model_version: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class AnalysisListResponse(BaseModel):
    items: List[AnalysisResponse]
    total: int
    page: int
    per_page: int
    pages: int


class TrainingSampleCreate(BaseModel):
    message: str = Field(..., min_length=1)
    label: str = Field(..., pattern="^(spam|ham)$")


class TrainingSampleResponse(BaseModel):
    id: int
    message: str
    label: str
    created_at: datetime

    class Config:
        from_attributes = True


class TrainingSampleListResponse(BaseModel):
    items: List[TrainingSampleResponse]
    total: int
    page: int
    per_page: int
    pages: int


class ModelVersionResponse(BaseModel):
    id: int
    version: str
    algorithm: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    trained_at: datetime

    class Config:
        from_attributes = True


class TrainingResultResponse(BaseModel):
    best_model: str
    best_version: str
    results: Dict[str, Any]
    train_size: int
    test_size: int
    total_samples: int


class DashboardStats(BaseModel):
    total_analyses: int
    spam_count: int
    ham_count: int
    spam_percentage: float
    recent_analyses: List[AnalysisResponse]
    daily_stats: List[Dict[str, Any]]


class AdminStats(BaseModel):
    total_users: int
    total_analyses: int
    spam_count: int
    ham_count: int
    spam_percentage: float
    model_versions: int
    training_samples: int


class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    per_page: int
    pages: int
