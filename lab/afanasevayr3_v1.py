import itertools
import random
import numpy as np
import matplotlib.pyplot as plt

def task1(elements: list):
    return list(itertools.permutations(elements))

def task2(elements: list, k: int):
    return list(itertools.combinations(elements, k))

def task3(elements: list):
    def backtrack(path, used, result):
        if len(path) == len(elements):
            result.append(tuple(path))
            return
        for i in range(len(elements)):
            if not used[i]:
                used[i] = True
                path.append(elements[i])
                backtrack(path, used, result)
                path.pop()
                used[i] = False
    result = []
    backtrack([], [False] * len(elements), result)
    return result

def task4(elements: list, k: int, max_sum: float = None):
    all_combinations = task2(elements, k)
    if max_sum is not None:
        filtered = [comb for comb in all_combinations if sum(comb) <= max_sum]
        return filtered
    
    return all_combinations

def task5(n: int, k: int, m: int = 1000):
    successful_cases = 0
    all_distributions = []
    
    threshold = np.ceil(n / k)

    for _ in range(m):
        distribution = [0] * k
        for _ in range(n):
            container = random.randint(0, k-1)
            distribution[container] += 1
        
        all_distributions.append(distribution)

        if max(distribution) >= threshold:
            successful_cases += 1
    
    probability = successful_cases / m
    return probability, all_distributions


    

test_elements = [1, 2, 3]

print("Практическое задание 1:")
perms = task1(test_elements)
print(f"Перестановки {test_elements}: {perms}")

print("\nПрактическое задание 2:")
combs = task2(test_elements, 2)
print(f"Сочетания из {test_elements} по 2: {combs}")

print("\nПрактическое задание 3:")
opt_perms = task3(test_elements)
print(f"Оптимизированные перестановки: {opt_perms}")

print("\nПрактическое задание 4:")
test_elements_constrained = [1, 2, 3, 4, 5]
constrained_combs = task4(test_elements_constrained, 3, max_sum=8)
print(f"Элементы: {test_elements_constrained}")
print(f"Сочетания из 3 элементов с суммой ≤ 8: {constrained_combs}")
print(f"Количество: {len(constrained_combs)}")

print("\nПрактическое задание 5:")
prob, distributions = task5(10, 3, 1000)

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
flat_dist = [item for sublist in distributions for item in sublist]
plt.hist(flat_dist, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
plt.axvline(x=10/3, color='red', linestyle='--', label=f'Среднее значение ({10/3:.1f})')
plt.xlabel('Количество объектов в контейнере')
plt.ylabel('Частота')
plt.title('Распределение объектов (n=10, k=3)')
plt.legend()
plt.grid(alpha=0.3)
plt.subplot(1, 2, 2)
n_values = range(3, 30, 3)
probabilities = []

for n_val in n_values:
    prob, _ = task5(n_val, 3, 200)
    probabilities.append(prob)

plt.plot(n_values, probabilities, 'bo-', linewidth=2, markersize=4)
plt.xlabel('Количество объектов (n)')
plt.ylabel('Вероятность выполнения принципа')
plt.title('Зависимость вероятности от количества объектов')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
print(f"Вероятность выполнения принципа Дирихле: {prob:.3f}")

print("\nЗадача 1:")
symbols1 = ['–', '.']
words_length2 = [''.join(p) for p in itertools.permutations(symbols1, 2)]
print(f"Символы: {symbols1}")
print(f"Все слова длины 2: {words_length2}")
print(f"Количество слов: {len(words_length2)}")

print("\nЗадача 2:")
letters = ['A', 'B', 'C']
comb_2_letters = task2(letters, 2)
print(f"Буквы: {letters}")
print(f"Комбинации из 2 букв: {comb_2_letters}")
print(f"Количество комбинаций: {len(comb_2_letters)}")

print("\nЗадача 3:")
landmarks = ['A', 'B', 'C', 'D']
distance_matrix = [
    [0, 2, 9, 10],
    [1, 0, 6, 4],
    [15, 7, 0, 8],
    [6, 3, 12, 0]
]

routes = []
for perm in task3(landmarks[1:]):
    route = ['A'] + list(perm) + ['A']
    routes.append(route)

route_distances = []
for route in routes:
    total_distance = 0
    for i in range(len(route)-1):
        from_idx = landmarks.index(route[i])
        to_idx = landmarks.index(route[i+1])
        total_distance += distance_matrix[from_idx][to_idx]
    route_distances.append((route, total_distance))

min_route = min(route_distances, key=lambda x: x[1])
print(f"Достопримечательности: {landmarks}")
print(f"Всего маршрутов: {len(routes)}")
print(f"Самый короткий маршрут: {min_route[0]} - {min_route[1]} км")

print("\nЗадача 4:")
employees = ['A', 'B', 'C', 'D', 'E']

def valid_committee(committee):
    return not ('A' in committee and 'B' in committee)

all_committees = task2(employees, 3)
valid_committees = [comm for comm in all_committees if valid_committee(comm)]

print(f"Сотрудники: {employees}")
print(f"Все комитеты из 3 человек: {len(all_committees)}")
print(f"Допустимые комитеты (A и B не вместе): {valid_committees}")
print(f"Количество допустимых комитетов: {len(valid_committees)}")

print("\nЗадача 5:")
print("367 человек и 365 дней в году")
birthdays = [random.randint(1, 365) for _ in range(367)]
unique_birthdays = len(set(birthdays))

has_match = (unique_birthdays < 367)
print(f"Уникальных дней рождения: {unique_birthdays}")
print(f"Есть совпадения: {'да' if has_match else 'нет'}")
print("Вывод: Принцип Дирихле подтверждается - как минимум у двух человек день рождения совпадает.")

