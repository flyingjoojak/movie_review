from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from database import create_db_and_tables, get_session
from models import Movie, MovieCreate, MovieRead, Review, ReviewCreate, ReviewRead
from ml.sentiment import analyze_sentiment
import uvicorn
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# --- Movie Endpoints ---

@app.post("/movies/", response_model=MovieRead)
def create_movie(movie: MovieCreate, session: Session = Depends(get_session)):
    db_movie = Movie.model_validate(movie)
    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    return db_movie

@app.get("/movies/", response_model=List[MovieRead])
def read_movies(offset: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    movies = session.exec(select(Movie).offset(offset).limit(limit)).all()
    return movies

@app.get("/movies/{movie_id}", response_model=MovieRead)
def read_movie(movie_id: int, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    session.delete(movie)
    session.commit()
    return {"ok": True}

# --- Review Endpoints ---

@app.post("/reviews/", response_model=ReviewRead)
def create_review(review: ReviewCreate, session: Session = Depends(get_session)):
    # 1. Analyze sentiment
    sentiment_result = analyze_sentiment(review.content)
    
    # 2. Create DB object
    db_review = Review.model_validate(review)
    db_review.sentiment_label = sentiment_result["label"]
    db_review.sentiment_score = sentiment_result["score"]
    
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review

@app.get("/reviews/", response_model=List[ReviewRead])
def read_reviews(movie_id: Optional[int] = None, offset: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    query = select(Review)
    if movie_id:
        query = query.where(Review.movie_id == movie_id)
    query = query.order_by(Review.created_at.desc()).offset(offset).limit(limit)
    reviews = session.exec(query).all()
    return reviews

@app.delete("/reviews/{review_id}")
def delete_review(review_id: int, session: Session = Depends(get_session)):
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    session.delete(review)
    session.commit()
    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
