import streamlit as st
import api
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="영화 리뷰 서비스", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
    }
    .movie-card {
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .sentiment-positive {
        color: green;
        font-weight: bold;
    }
    .sentiment-negative {
        color: red;
        font-weight: bold;
    }
    .sentiment-neutral {
        color: gray;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎬 영화 리뷰 & 감성 분석 서비스")

# Sidebar
menu = st.sidebar.selectbox("메뉴", ["영화 목록", "영화 추가"])

if "selected_movie_id" not in st.session_state:
    st.session_state.selected_movie_id = None

def go_to_movie_detail(movie_id):
    st.session_state.selected_movie_id = movie_id
    # Force rerun handled by streamlit interaction usually, or use st.rerun()
    # st.rerun() in newer streamlit, st.experimental_rerun() in older.
    # Assuming newer version installed.


def REVIEW_RATING_TO_STAR(rating):
    # simple converter 1-10 to 1-5 for visual? or just use rating.
    # User might want to see number.
    # The requirement says display rating.
    # Let's clean up calling logical in markdown.
    return int(rating / 2) + 1 if rating else 0

if menu == "영화 추가":
    st.header("새 영화 등록")
    with st.form("add_movie_form"):
        title = st.text_input("제목")
        director = st.text_input("감독")
        genre = st.text_input("장르")
        release_date = st.date_input("개봉일")
        poster_url = st.text_input("포스터 URL (이미지 주소)")
        
        submitted = st.form_submit_button("등록 하기")
        if submitted:
            if title and director:
                data = {
                    "title": title,
                    "director": director,
                    "genre": genre,
                    "release_date": str(release_date),
                    "poster_url": poster_url
                }
                if api.create_movie(data):
                    st.success(f"'{title}' 영화가 등록되었습니다!")
                else:
                    st.error("영화 등록 실패")
            else:
                st.warning("제목과 감독은 필수 입력입니다.")

elif menu == "영화 목록":
    if st.session_state.selected_movie_id is None:
        st.header("현재 상영작 / 등록된 영화")
        movies = api.get_movies()
        
        if not movies:
            st.info("등록된 영화가 없습니다. '영화 추가' 메뉴에서 등록해주세요.")
        
        # Grid layout
        cols = st.columns(3)
        for idx, movie in enumerate(movies):
            with cols[idx % 3]:
                if movie.get("poster_url"):
                    st.image(movie["poster_url"], use_container_width=True) # use_column_width deprecated
                else:
                    st.image("https://via.placeholder.com/300x450?text=No+Poster", use_container_width=True)
                
                st.subheader(movie["title"])
                st.write(f"**감독**: {movie['director']}")
                st.write(f"**장르**: {movie['genre']}")
                
                if st.button("상세 보기", key=f"btn_{movie['id']}"):
                    st.session_state.selected_movie_id = movie["id"]
                    st.rerun()
                    
    else:
        # Movie Detail View
        if st.button("← 목록으로 돌아가기"):
            st.session_state.selected_movie_id = None
            st.rerun()
            
        movie_id = st.session_state.selected_movie_id
        movie = api.get_movie(movie_id)
        
        if movie:
            st.title(movie["title"])
            
            c1, c2 = st.columns([1, 2])
            with c1:
                if movie.get("poster_url"):
                    st.image(movie["poster_url"], use_container_width=True)
            with c2:
                st.markdown(f"### 정보")
                st.write(f"**감독**: {movie['director']}")
                st.write(f"**장르**: {movie['genre']}")
                st.write(f"**개봉일**: {movie['release_date']}")
                
                if st.button("영화 삭제", type="primary"):
                    if api.delete_movie(movie_id):
                        st.success("삭제되었습니다.")
                        st.session_state.selected_movie_id = None
                        st.rerun()
                    else:
                        st.error("삭제 실패")

            st.divider()
            
            # Reviews
            st.header("리뷰 및 감성 분석")
            
            with st.expander("리뷰 작성하기", expanded=True):
                with st.form("review_form"):
                    col1, col2 = st.columns([4,1])
                    with col1:
                        user_name = st.text_input("작성자 이름")
                        content = st.text_area("리뷰 내용", placeholder="영화에 대한 솔직한 감상평을 남겨주세요.")
                    with col2:
                        rating = st.slider("평점", 1, 10, 8)
                    
                    submit_review = st.form_submit_button("리뷰 등록")
                    if submit_review:
                        if user_name and content:
                            with st.spinner("감성 분석 중..."):
                                res = api.create_review(movie_id, user_name, content, rating)
                                if res:
                                    st.success("리뷰가 등록되었습니다!")
                                    st.rerun()
                                else:
                                    st.error("리뷰 등록 실패")
                        else:
                            st.warning("이름과 내용을 입력하세요.")
            
            reviews = api.get_reviews(movie_id)
            if reviews:
                total_reviews = len(reviews)
                avg_score = sum([r['sentiment_score'] for r in reviews]) / total_reviews if total_reviews > 0 else 0
                
                st.metric("리뷰 수", f"{total_reviews}개")
                
                st.markdown("### 최근 리뷰")
                for review in reviews:
                    with st.container():
                        # Sentiment visual
                        s_label = review['sentiment_label']
                        s_color = "green" if s_label == 'positive' else "red" if s_label == 'negative' else "gray"
                        s_icon = "😊" if s_label == 'positive' else "😢" if s_label == 'negative' else "😐"
                        
                        st.markdown(f"**{review['user_name']}** <span style='color:gold'>{'★'*REVIEW_RATING_TO_STAR(review['rating'])}</span> ({review['created_at'][:10]})", unsafe_allow_html=True)
                        st.write(review['content'])
                        st.markdown(f"감성 분석: <span style='color:{s_color}'>{s_icon} {s_label.upper()} ({review['sentiment_score']:.2f})</span>", unsafe_allow_html=True)
                        
                        if st.button("리뷰 삭제", key=f"del_rev_{review['id']}"):
                            if api.delete_review(review['id']):
                                st.success("삭제됨")
                                st.rerun()
                        st.markdown("---")
            else:
                st.info("아직 작성된 리뷰가 없습니다.")
                            
        else:
            st.error("영화를 찾을 수 없습니다.")
            if st.button("돌아가기"):
                st.session_state.selected_movie_id = None
                st.rerun()


