import numpy as np
import matplotlib.pyplot as plt

# Генерация двух наборов случайных данных
num_samples = 5  # Количество образцов

x_data = np.random.rand(num_samples)
y_data = np.random.rand(num_samples)

# Вывод сгенерированных массивов для проверки
print("x_data:", x_data)
print("y_data:", y_data)

# Построение диаграммы рассеяния
plt.figure(figsize=(10, 6))
plt.scatter(x_data, y_data, alpha=0.7, edgecolors='w', s=100)
plt.title('Scatter Plot of Random Data')
plt.xlabel('X Data')
plt.ylabel('Y Data')
plt.grid(True)
plt.show()
