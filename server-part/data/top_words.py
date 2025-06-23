import pandas as pd
import re
import json
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

nltk.download("punkt") 
nltk.download("stopwords")

stop_words = set(stopwords.words("english"))

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    # tokens = word_tokenize(text)
    tokens = text.split()
    tokens = [t for t in tokens if t not in stop_words and len(t) > 2]
    return tokens


def build_top_words(input_csv="dataset_news.csv", output_json="top_words_by_category.json"):
    df = pd.read_csv(input_csv)
    category_word_freq = {}

    for category in df["category_general"].unique():
        texts = df[df["category_general"] == category]["title"].dropna().astype(str)
        all_words = []
        for title in texts:
            all_words.extend(clean_text(title))

        word_counts = Counter(all_words)
        most_common = word_counts.most_common(20)
        category_word_freq[category] = most_common

    with open(output_json, "w") as f:
        json.dump(category_word_freq, f, indent=2)


if __name__ == "__main__":
    build_top_words()