# Практична 2. СеменчукТВ-22. Варіант 19
#Об'єднання дублікатів. Напишіть функцію, яка знаходить схожі значення (нд., з різницею в 1 св.) та об'єднує їх. 
import pandas as pd
import Levenshtein
# Для вимірювання часу 
from contextlib import contextmanager
import time

@contextmanager
def timer():
    start = time.time()
    yield
    end = time.time()
    print(f"Час виконання блоку: {end - start:.4f} секунд")
# Знаходить і об'єднує схожі текстові значення в серії Pandas, використовуючи відстань Левенштейна
def find_and_merge_similar(df_col: pd.Series, threshold: int = 1) -> pd.Series:
    df_col_processed = df_col.astype(str).str.lower().str.strip() #all to lowercase +remove spaces
    print(f"Починаємо обробку колонки. Всього записів: {len(df_col_processed)}. Кількість унікальних значень (після попередньої обробки): {df_col_processed.nunique()}")

    unique_values = df_col_processed.dropna().unique()
    mapping = {} # cлавник для зберігання відповідностей: "погане" значення -> "чисте" значення

    unique_values_sorted = sorted(unique_values, key=lambda x: (len(x), x)) # для вибору  кращих значень

    # вимірювання часу для порівняння уникальних значень
    with timer():
        for current_val in unique_values_sorted:
            if current_val in mapping:
                continue

            master_val = current_val
            mapping[current_val] = master_val

            for other_val in unique_values_sorted:
                if other_val == current_val or other_val in mapping:
                    continue

                distance = Levenshtein.distance(master_val, other_val)

                if distance <= threshold:
                    mapping[other_val] = master_val
    print(f"Завершено порівняння. Знайдено {len(set(mapping.values()))} унікальних об'єднаних значень.")
    return df_col_processed.map(mapping) # Тидишь - мапінг до оригинальної колоночки

if __name__ == "__main__":
    file_path = 'data.txt'

    print(f"Читаємо дані з файлу '{file_path}'...")
    data_list = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                data_list.append(line.strip()) # читаємо кожен рядок і видаляємо символи нового рядка
        print(f"Прочитано {len(data_list)} рядків.")

        df = pd.DataFrame({'product_name': data_list})

        print("\nПерші 10 рядків оригінального DataFrame:")
        print(df.head(10))
        print("-" * 30)

        print("\nЗапускаємо функцію об'єднання схожих назв...")
        with timer(): 
            df['cleaned_product_name'] = find_and_merge_similar(df['product_name'], threshold=1)

        print("\nПерші 20 рядків DataFrame після об'єднання схожих назв:")
        print(df.head(20))
        print("-" * 30)

        print("\nГрупування за очищеною назвою та підрахунок елементів:")
        # новий датафрем, щоб показати унікальні очищені значення та їх кількість
        grouped_df = df.groupby('cleaned_product_name').size().reset_index(name='count').sort_values(by='count', ascending=False)
        print(grouped_df.head(20)) # перші 20 найчастіших
        print(f"\nЗагальна кількість унікальних (об'єднаних) назв: {len(grouped_df)}")
        print("-" * 30)

    except FileNotFoundError:
        print(f"Помилка: Файл '{file_path}' не знайдено. Переконайтеся, що файл існує в тій самій папці.")
    except Exception as e:
        print(f"Виникла несподівана помилка при читанні файлу: {e}")