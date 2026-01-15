from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

class MovieBase(SQLModel):
    title: str = Field(index=True)
    release_date: str  # YYYY-MM-DD
    director: str
    genre: str
    poster_url: Optional[str] = None

class Movie(MovieBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    reviews: List["Review"] = Relationship(back_populates="movie")

class MovieCreate(MovieBase):
    pass

class MovieRead(MovieBase):
    id: int


class ReviewBase(SQLModel):
    movie_id: int = Field(foreign_key="movie.id")
    user_name: str
    content: str
    rating: int = Field(default=0)
    
class Review(ReviewBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sentiment_score: float = Field(default=0.0) # 0.0 ~ 1.0 (or -1 ~ 1 depending on model, let's say probability of positive)
    sentiment_label: str = Field(default="neutral") # positive, negative
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    movie: Movie = Relationship(back_populates="reviews")

class ReviewCreate(ReviewBase):
    pass

class ReviewRead(ReviewBase):
    id: int
    sentiment_score: float
    sentiment_label: str
    created_at: datetime
