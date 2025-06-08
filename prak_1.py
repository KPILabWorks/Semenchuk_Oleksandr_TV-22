# Prak_1.Семенчук ТВ-22. Завдання: Реалізувати менеджер контексту, який відстежує час виконання коду.
import time

class Timer:
    def __enter__(self):
        self.start_time = time.time() # час початку
        print("Початок вимірювання часу виконання...")
        return self

    def __exit__(self, obj_type, obj_val, obj_tb):
        self.end_time = time.time() # час завершення
        self.elapsed_time = self.end_time - self.start_time 
        print(f"Кінець вимірювання. Час виконання коду: {self.elapsed_time:.4f} секунд.")
        return False # повертаємо False щоби побачити виняток

# Приклади використання
if __name__ == "__main__":
    print("Приклад 1: Простий розрахунок")
    with Timer(): # cтворюємо екз. Timer і входимо в його контекст
        _ = sum(range(10000000))

    print("\nПриклад 2: Складніший розрахунок")
    with Timer(): 
        data = [i**2 for i in range(5000000)]
        data.sort()

    print("\nПриклад 3: З помилкою в блоці")
    try:
        with Timer(): 
            print("Це до помилки...")
            1 / 0 
            print("Це після помилки (не буде виконано)...")
    except ZeroDivisionError:
        print("Перехоплено ZeroDivisionError за межами менеджера контексту.")