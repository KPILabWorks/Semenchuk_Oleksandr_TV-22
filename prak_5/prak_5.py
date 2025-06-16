""" 
Практична 5. Семенчук ТВ-22. Варінат 19
19. Оптимізація коду для обробки великих наборів даних: Створити функцію для ефективної обробки 
великих наборів даних, використовуючи оптимізовані алгоритми та паралельні обчислення.
"""
import random
import time
from concurrent.futures import ProcessPoolExecutor
import multiprocessing 
import math 

# перевірка на простоту числа (CPU-bound завдання)
def is_prime(n):
    if n < 2:
        return False
    # Перевірка - подільність до квадратного кореня числа
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True
# ф-я обчислення суми квадратів для пр. ч.
def compute_sum_of_squares_for_primes(number_item):
    if is_prime(number_item):
        total_sum_of_squares = 0
        for i in range(1, number_item + 1):
            total_sum_of_squares += i * i 
        return total_sum_of_squares
    return None

# ф-я послідовної обробки
def sequential_data_processing(input_data):
    processed_results = []
    for item_val in input_data:
            result = compute_sum_of_squares_for_primes(item_val)
            if result is not None:
                processed_results.append(result)
    return processed_results

# ф-я паралельної обробки 
def parallel_data_processing(input_data, workers_count=None):
    if workers_count is None:
        workers_count = multiprocessing.cpu_count()    
    # В-я ProcessPoolExecutor для паралельного виконання
    with ProcessPoolExecutor(max_workers=workers_count) as executor:
        results_iterator = executor.map(compute_sum_of_squares_for_primes, input_data, 
                                        chunksize=len(input_data) // workers_count)
    final_processed_data = [res for res in results_iterator if res is not None]
    return final_processed_data


if __name__ == "__main__":
    # П-ри для генерації набору даних:
    DATASET_SIZE = 100000 
    MIN_VALUE = 100
    MAX_VALUE = 5000 

    print(f"Генеруємо набір даних з {DATASET_SIZE} випадкових чисел...")
    # генерация набір даних, що містить цілі числа
    large_dataset = [random.randint(MIN_VALUE, MAX_VALUE) for _ in range(DATASET_SIZE)]
    print("Набір даних згенеровано.\n")

# Тестування послідовної обробки 
    print("Запускаємо послідовну обробку...")
    start_time_seq = time.perf_counter()# Фіксуємо час початку виконання
    # обробка елементів один за одним, використовуючи лише один потік CPU,за доп ф-ї sequential_data_processing
    processed_seq_results = sequential_data_processing(large_dataset)
    # Фіксуємо час завершення виконання
    end_time_seq = time.perf_counter()
    # загальний час виконання послідовної версії
    time_seq_execution = end_time_seq - start_time_seq
    print(f"Послідовна обробка завершена.")
    print(f"Кількість оброблених елементів (послідовно): {len(processed_seq_results)}")
    print(f"Час виконання послідовної обробки: {time_seq_execution:.4f} секунд\n")

    # Тестування паралельної обробки
    print("Запускаємо паралельну обробку...")
    num_cpu_cores = multiprocessing.cpu_count() # всі доступні ядра
    # (start)час початку виконання паралельної версії
    start_time_par = time.perf_counter()
    processed_par_results = parallel_data_processing(large_dataset, workers_count=num_cpu_cores)
    # ProcessPoolExecutor розподіляє завдання між кількома процесами, що виконуються паралельно
    end_time_par = time.perf_counter()# (end) час завершення виконання

    # загальний час виконання паралельної версії
    time_par_execution = end_time_par - start_time_par
    print(f"Паралельна обробка завершена.")
    print(f"Кількість оброблених елементів (паралельно): {len(processed_par_results)}")
    print(f"Час обробки в багатопроцесорній обробці ({num_cpu_cores} ядер): {time_par_execution:.4f} секунд\n")

    # порівняння результатів
    print("\n Порівняння часу виконання")
    print(f"Час послідовної обробки: {time_seq_execution:.4f} с")
    print(f"Час паралельної обробки: {time_par_execution:.4f} с")
    
    if time_par_execution < time_seq_execution:
        speedup_factor = time_seq_execution / time_par_execution
        print(f"Прискорення в {speedup_factor:.2f} разів завдяки паралельній обробці!")
    else:
        print("Паралельна обробка не призвела до прискорення (можливо, накладні витрати великі або завдання не CPU-bound).")

    # Перевірка, що результати однакові (по кількіості елементів)
    if len(processed_seq_results) == len(processed_par_results):
        print("\nКiлькiсть елементів, оброблених обома методами, однакова. Результати коректні.")
    else:
        print("\nУвага: Кількість оброблених елементів різна. Можлива помилка в логіці.")
