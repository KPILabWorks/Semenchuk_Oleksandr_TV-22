""" 
Практична 4. Семенчук ТВ-22. Варінат 19
19. Моделювання системи попиту та пропозиції
Реалiзувати динамічну модель попиту та пропозиції електроенергії з використанням диференціальних рівнянь. 
Порівняти з методом трендової екстраполяції. Візуалізуйте динаміку попиту та пропозиції з часом.
"""
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Qd = D0 - d * P   (Попит зменшується зі зростанням ціни P)
# Qs = S0 + s * P   (Пропозиція зростає зі зростанням ціни P)

# Параметри функції попиту:
D0 = 1000 # початковий попит
d = 10     # коефіцієнт чутливості попиту до ціни
# Параметри функції пропозиції:
S0 = 100   # початкова пропозиція
s = 20     # коефіцієнт чутливості пропозиції до ціни 
# Параметри динамічної моделі:
alpha = 0.1  # Коефіцієнт швидкості коригування ціни.
P0 = 40      # Початкова ціна 

# Часовий інтервал для моделювання:
time_points = np.linspace(0, 50, 500) # від 0 до 50 одиниць часу, з 500 точками

# Динамічна модель (за диференціальними рівняннями)

# Функції попиту та пропозиції 
def demand_function(price, D0, d):
    return D0 - d * price

def supply_function(price, S0, s):
    return S0 + s * price

# Диференціальне рівняння для ціни
# dP/dt = alpha * (Qd - Qs)
def price_differential_equation(P, t, alpha, D0, d, S0, s):
    Qd = demand_function(P, D0, d)
    Qs = supply_function(P, S0, s)
    dPdt = alpha * (Qd - Qs)
    return dPdt

# odeint повертає масив значень ціни P(t) для кожного моменту часу
prices_dynamic = odeint(price_differential_equation, P0, time_points, args=(alpha, D0, d, S0, s))
prices_dynamic = prices_dynamic.flatten() # Перетворюється на одновимірний масив

# обчисленя попит та пропозицію на основі динамічної ціни
demand_dynamic = demand_function(prices_dynamic, D0, d)
supply_dynamic = supply_function(prices_dynamic, S0, s)

print("--- Динамічна модель (Диференціальні рівняння) ---")
print(f"Початкова ціна P0: {P0:.2f}")
print(f"Ціна на кінець моделювання ({time_points[-1]:.0f} одиниць часу): {prices_dynamic[-1]:.2f}")
# обчислення ціни на рівні рівноваги аналітично: Qd = Qs => D0 - dP = S0 + sP => P = (D0 - S0) / (d + s)
equilibrium_price = (D0 - S0) / (d + s)
print(f"Теоретична рівноважна ціна: {equilibrium_price:.2f}")
print(f"Теоретична рівноважна кількість: {demand_function(equilibrium_price, D0, d):.2f}")
print("-" * 50)

# -Метод трендової екстраполяції

# Для трендової екстраполяції я візьму перші кілька точок з динамічної моделі як історичні дані.
historical_time_points = time_points[:100] # Перші 100 точок (від 0 до 10 одиниць часу)
historical_demand = demand_dynamic[:100]
historical_supply = supply_dynamic[:100]
historical_prices = prices_dynamic[:100]

# Лінійна регресія для попиту
slope_demand, intercept_demand, r_value_demand, p_value_demand, std_err_demand = linregress(historical_time_points, historical_demand)
# Лінійна регресія для пропозиції
slope_supply, intercept_supply, r_value_supply, p_value_supply, std_err_supply = linregress(historical_time_points, historical_supply)
# Лінійна регресія для ціни (для порівняння)
slope_price, intercept_price, r_value_price, p_value_price, std_err_price = linregress(historical_time_points, historical_prices)


# тренд на весь період моделювання
demand_extrapolated = intercept_demand + slope_demand * time_points
supply_extrapolated = intercept_supply + slope_supply * time_points
prices_extrapolated = intercept_price + slope_price * time_points


print("--- Метод трендової екстраполяції (на основі перших 100 точок) ---")
print(f"Рівняння тренду попиту: Qd(t) = {intercept_demand:.2f} + {slope_demand:.2f} * t")
print(f"Рівняння тренду пропозиції: Qs(t) = {intercept_supply:.2f} + {slope_supply:.2f} * t")
print(f"Рівняння тренду ціни: P(t) = {intercept_price:.2f} + {slope_price:.2f} * t")
print("-" * 50)

# Візуалізація та порівняння 

plt.figure(figsize=(14, 6))

# Графік ціни
plt.subplot(1, 2, 1) # 1 рядок, 2 колонки, 1-й графік
plt.plot(time_points, prices_dynamic, label='Динамічна модель ціни', color='blue')
plt.plot(time_points, prices_extrapolated, label='Трендова екстраполяція ціни', color='cyan', linestyle='--')
plt.axhline(equilibrium_price, color='red', linestyle=':', label=f'Ринкова рівновага ({equilibrium_price:.2f})')
plt.title('Динаміка Ціни на Електроенергію')
plt.xlabel('Час')
plt.ylabel('Ціна (у.о./МВт·год)')
plt.legend()
plt.grid(True)

# Графік попиту та пропозиції
plt.subplot(1, 2, 2) # 1 рядок, 2 колонки, 2-й графік
plt.plot(time_points, demand_dynamic, label='Попит (динамічна модель)', color='green')
plt.plot(time_points, supply_dynamic, label='Пропозиція (динамічна модель)', color='orange')
plt.plot(time_points, demand_extrapolated, label='Попит (трендова екстраполяція)', color='lightgreen', linestyle='--')
plt.plot(time_points, supply_extrapolated, label='Пропозиція (трендова екстраполяція)', color='gold', linestyle='--')
plt.title('Динаміка Попиту та Пропозиції Електроенергії')
plt.xlabel('Час')
plt.ylabel('Кількість (МВт·год)')
plt.legend()
plt.grid(True)

plt.tight_layout() # Автоматично налаштовує параметри підграфіків
plt.savefig('model.png')

