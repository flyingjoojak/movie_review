import requests
import streamlit as st

API_BASE_URL = st.secrets.get("API_URL", "http://localhost:8001")

def get_movies():
    try:
        response = requests.get(f"{API_BASE_URL}/movies/")
        if response.status_code == 200:
            return response.json()
        return []
    except requests.exceptions.RequestException:
        st.error("서버 연결 실패. 백엔드 서버가 실행 중인지 확인하세요.")
        return []

def get_movie(movie_id):
    try:
        response = requests.get(f"{API_BASE_URL}/movies/{movie_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def create_movie(data):
    try:
        response = requests.post(f"{API_BASE_URL}/movies/", json=data)
        if response.status_code == 200:
            return True
        return False
    except:
        return False

def delete_movie(movie_id):
    try:
        response = requests.delete(f"{API_BASE_URL}/movies/{movie_id}")
        return response.status_code == 200
    except:
        return False

def get_reviews(movie_id):
    try:
        response = requests.get(f"{API_BASE_URL}/reviews/", params={"movie_id": movie_id})
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def create_review(movie_id, user_name, content, rating):
    data = {
        "movie_id": movie_id,
        "user_name": user_name,
        "content": content,
        "rating": rating
    }
    try:
        response = requests.post(f"{API_BASE_URL}/reviews/", json=data)
        if response.status_code == 200:
            return response.json() # Returns created review
        return None
    except:
        return None

def delete_review(review_id):
    try:
        response = requests.delete(f"{API_BASE_URL}/reviews/{review_id}")
        return response.status_code == 200
    except:
        return False
