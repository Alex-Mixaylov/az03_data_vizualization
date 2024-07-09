import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Параметры нормального распределения
mean = 0  # Среднее значение
std_dev = 1  # Стандартное отклонение
num_samples = 1000  # Количество образцов

# Генерация случайных чисел, распределенных по нормальному распределению
data = np.random.normal(mean, std_dev, num_samples)

# Создание DataFrame из данных
df = pd.DataFrame(data, columns=['Value'])

# Построение гистограммы
plt.figure(figsize=(10, 6))
plt.hist(df['Value'], bins=30, edgecolor='black', alpha=0.7)
plt.title('Гистограмма случайных чисел, распределенных по нормальному распределению')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
