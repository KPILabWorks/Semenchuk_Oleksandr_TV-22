import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib
import re

df = pd.read_csv("../data/dataset_news.csv")

df = df[['title', 'category_general']].dropna()

def clean_text(text):
    text = re.sub(r'[^A-Za-z0-9\s]', '', str(text))  # only letters and spaces
    return text.lower()

df['title'] = df['title'].apply(clean_text)
print(df['category_general'].value_counts())

X_train, X_test, y_train, y_test = train_test_split(
    df['title'], df['category_general'], test_size=0.2, random_state=42, stratify=df['category_general']
)

vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=10000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=1000) # або: MultinomialNB()  
model.fit(X_train_vec, y_train)

y_pred = model.predict(X_test_vec)
print(classification_report(y_test, y_pred))

joblib.dump(model, 'model.pkl')

print("Модель збережено.")
