import os
import json
import pandas as pd
from top_words import build_top_words

# Каталог з файлами
data_dir = "raw data/"

# === КРОК 1. Завантаження першого датасету (JSON) ===
records = []
with open(data_dir + "news_1.json", "r", encoding="utf-8") as f:
    for line in f:
        try:
            record = json.loads(line)
            records.append(record)
        except json.JSONDecodeError as e:
            print("JSON decode error:", e)
            continue

df1 = pd.DataFrame(records)

df1 = df1.rename(columns={
    'headline': 'title',
    'link': 'link',
    'authors': 'publisher',
    'date': 'pubDate',
    'category': 'category_general'
})

df1 = df1[['title', 'link', 'publisher', 'pubDate', 'category_general']]


category_map = {
    'entertainment': 'entertainment',
    'entertainment': 'entertainment',
    'arts & culture': 'entertainment',
    'culture & arts': 'entertainment',
    'comedy': 'entertainment',

    'business': 'business',
    'money': 'business',

    'science': 'science',
    'tech': 'science',
    'science & tech': 'science',

    'health': 'health',
    'healthy living': 'health',
    'wellness': 'health',

    'politics': 'politics',
    'world news': 'politics',
    'u.s. news': 'politics',
    'the worldpost': 'politics',
    'worldpost': 'politics',

    'sports': 'sports',

    'style': 'lifestyle',
    'style & beauty': 'lifestyle',
    'weddings': 'lifestyle',
    'divorce': 'lifestyle',
    'home & living': 'lifestyle',
    'taste': 'lifestyle',
    'travel': 'lifestyle',
    'food & drink': 'lifestyle',

    'queer voices': 'politics',
    'latino voices': 'politics',
    'black voices': 'politics',
    'impact': 'entertainment',
    'women': 'lifestyle',

    'education': 'science',
    'college': 'science',
    'parents': 'lifestyle',
    'parenting': 'lifestyle',
    'fifty': 'lifestyle',
    'good news': 'entertainment',
    'media': 'politics',
    'crime': 'politics',
    'green': 'science',
    'religion': 'lifestyle',
    'weird news': 'entertainment',
    'arts': 'entertainment',
}
df1['category_general'] = df1['category_general'].str.lower()
df1['category_general'] = df1['category_general'].map(category_map)
df1 = df1.dropna(subset=['category_general'])  # видаляємо невідомі категорії


# === КРОК 2. Завантаження другого датасету (CSV) ===
df2 = pd.read_csv(data_dir + "news_2.csv")

category_map = {
    'b': 'business',
    't': 'science',
    'e': 'entertainment',
    'm': 'health'
}
df2['category_general'] = df2['CATEGORY'].map(category_map)

df2 = df2.rename(columns={
    'TITLE': 'title',
    'URL': 'link',
    'PUBLISHER': 'publisher',
    'TIMESTAMP': 'pubDate'
})


df2['pubDate'] = pd.to_datetime(df2['pubDate'], unit='s', errors='coerce')

df2 = df2[['title', 'link', 'publisher', 'pubDate', 'category_general']]



# === КРОК 3. Об'єднання двох датасетів ===
sports_df = pd.read_csv(data_dir + "news_sport.csv")

sports_df = sports_df.rename(columns={
    'Headline': 'title',
    'Sport': 'sport', 
    'Date': 'date'
})

sports_df['category_general'] = 'sports'

sports_df = sports_df[['title', 'category_general']]





# === КРОК 3. Об'єднання двох датасетів ===
combined_df = pd.concat([df1, df2], ignore_index=True)
combined_df = combined_df.dropna(subset=['title', 'category_general'])

combined_df['category_general'] = combined_df['category_general'].str.lower()

combined_df = pd.concat([combined_df, sports_df], ignore_index=True)

# === КРОК 4. Збереження у CSV ===
combined_df.to_csv("dataset_news.csv", index=False, encoding='utf-8')

print("The merged dataset is saved as 'dataset_news.csv'")
print(f"Кількість записів у результаті: {combined_df.shape[0]}")


print("Start counting top words...")
build_top_words("dataset_news.csv", "top_words.json")
print("The words dataset is saved as 'top_words.json'")
