from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import json
import joblib
import re
from fastapi.middleware.cors import CORSMiddleware

data_dir = "../data/"
model_dir = "../model/"

model = joblib.load(model_dir + "model.pkl")
vectorizer = joblib.load(model_dir + "vectorizer.pkl")


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


with open(data_dir + "top_words.json", "r") as f:
    raw_data = json.load(f)
    print("Loaded JSON keys:", raw_data.keys())
    TOP_WORDS = {key.lower(): value for key, value in raw_data.items()}


class TitleRequest(BaseModel):
    title: str

def clean_text(text: str) -> str:
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    return text.lower()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/predict")
async def predict_category(request: TitleRequest):
    cleaned_title = clean_text(request.title)
    vec = vectorizer.transform([cleaned_title])

    prediction = model.predict(vec)[0]
    proba = model.predict_proba(vec)[0]  
    proba_dict = {
        category: round(float(prob), 4) 
        for category, prob in zip(model.classes_, proba)
    }

    sorted_proba = dict(sorted(proba_dict.items(), key=lambda item: item[1], reverse=True))

    return {
        "title": request.title,
        "predicted_category": prediction,
        "probabilities": sorted_proba
    }


@app.get("/top-words")
async def get_top_words(category: str = Query(..., description="Category name")):
    print("Available categories:", TOP_WORDS.keys())
    print("User requested category:", category.lower())

    words = TOP_WORDS.get(category.lower())
    if not words:
        raise HTTPException(status_code=404, detail="Category not found")

    formatted_words = [{"word": w[0], "count": w[1]} for w in words]
    return formatted_words
