# 영화 리뷰 및 감성 분석 서비스

## 프로젝트 소개
Streamlit(프론트엔드)과 FastAPI(백엔드)를 활용하여 영화 정보를 관리하고 리뷰를 작성할 수 있는 웹 애플리케이션입니다. 작성된 리뷰는 Hugging Face Transformers 모델을 통해 자동으로 감성(긍정/부정)이 분석됩니다.

## 팀원
- Team_Antigravity

## 실행 방법

### 1. 환경 설정
Python 3.8+ 환경이 필요합니다.

```bash
# Backend 의존성 설치
cd backend
pip install -r requirements.txt

# Frontend 의존성 설치
cd ../frontend
pip install -r requirements.txt
```

### 2. 실행

#### Backend 실행
```bash
cd backend
uvicorn main:app --port 8001 --reload
```
서버는 `http://localhost:8001`에서 실행됩니다.
Swagger 문서는 `http://localhost:8001/docs`에서 확인할 수 있습니다.

#### Frontend 실행
새로운 터미널을 열고 실행하세요.
```bash
cd frontend
streamlit run app.py
```
브라우저에서 자동으로 `http://localhost:8501`이 열립니다.

## 주요 기능
- **영화 관리**: 영화 등록, 조회, 삭제
- **리뷰 관리**: 영화별 리뷰 작성, 조회, 삭제, 평점 시각화
- **감성 분석**: 한국어 리뷰 텍스트 감성 분석 (긍정/부정) 및 점수 표출

## 기술 스택
- **Backend**: FastAPI, SQLModel (SQLite), Transformers (Sentiment Analysis)
- **Frontend**: Streamlit, Python Requests
- **Model**: `daekeun-ml/ko-electra-small-v3-nsmc` (Hugging Face)
