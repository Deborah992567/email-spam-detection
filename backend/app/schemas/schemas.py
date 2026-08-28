"""
Pydantic schemas for request/response validation.
"""
import json
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255, description="User's full name")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=6, max_length=128, description="Password (min 6 chars)")


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    role: str
    created_at: datetime


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    email: Optional[EmailStr] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class AnalysisRequest(BaseModel):
    sender: Optional[str] = Field(None, max_length=255, description="Sender email address")
    subject: Optional[str] = Field(None, max_length=500, description="Email subject line")
    body: str = Field(..., min_length=1, max_length=50000, description="Email body text")


class AnalysisResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())
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

    @field_validator("indicators", mode="before")
    @classmethod
    def _parse_indicators(cls, v):
        """Indicators are stored as a JSON string in the DB; normalize to a list."""
        if isinstance(v, str):
            try:
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return None
        return v


class AnalysisListResponse(BaseModel):
    items: List[Dict[str, Any]]
    total: int
    page: int
    per_page: int
    pages: int


class TrainingSampleCreate(BaseModel):
    message: str = Field(..., min_length=1, description="Training text")
    label: str = Field(..., pattern="^(spam|ham)$", description="'spam' or 'ham'")


class TrainingSampleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    message: str
    label: str
    source: str
    created_at: datetime


class TrainingSampleListResponse(BaseModel):
    items: List[TrainingSampleResponse]
    total: int
    page: int
    per_page: int
    pages: int


class ModelVersionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    version: str
    algorithm: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    trained_at: datetime


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
    recent_analyses: List[Dict[str, Any]]
    daily_stats: List[Dict[str, Any]]
    risk_distribution: Dict[str, int] = Field(default_factory=dict)


class AdminStats(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
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
