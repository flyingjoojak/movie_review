from transformers import pipeline

# Load pipeline globally to avoid reloading on every request
# Using a lightweight Korean sentiment model
# daekeun-ml/ko-electra-small-v3-nsmc is trained on NSMC (Naver Sentiment Movie Corpus)
MODEL_NAME = "WhitePeak/bert-base-cased-Korean-sentiment"

sentiment_pipeline = None

def get_sentiment_pipeline():
    global sentiment_pipeline
    if sentiment_pipeline is None:
        print("Loading sentiment model...")
        sentiment_pipeline = pipeline("text-classification", model=MODEL_NAME)
        print("Model loaded.")
    return sentiment_pipeline

def analyze_sentiment(text: str):
    pipe = get_sentiment_pipeline()
    # Truncate text if too long (max 512 tokens usually)
    result = pipe(text[:512])[0]
    # result example: {'label': '1', 'score': 0.9} or {'label': '0', 'score': 0.8}
    # NSMC labels: 0 (Negative), 1 (Positive)
    
    label_map = {"0": "negative", "1": "positive"}
    mapped_label = label_map.get(result['label'], "neutral")
    
    return {
        "label": mapped_label,
        "score": result['score']
    }
