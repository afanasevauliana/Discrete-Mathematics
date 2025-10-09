import numpy as np
import matplotlib.pyplot as plt
import itertools

n1 = [0, 4, 7]
n2 = [1, 5, 0, 7]
N1 = set(n1)
N2 = set(n2)
print("Множества:")
print("N1 =", N1)
print("N2 =", N2)
print()

N1_x_N2 = set(itertools.product(N1, N2))
N2_x_N1 = set(itertools.product(N2, N1))
print("N1 x N2 =", N1_x_N2)
print("N2 x N1 =", N2_x_N1)
print()

result1 = N1_x_N2.symmetric_difference(N2_x_N1)  # (N1 x N2) ⇔ (N2 x N1)
result2 = N1_x_N2.union(N2_x_N1)                # (N1 x N2) ∪ (N2 x N1)
result3 = set(itertools.product(N1.symmetric_difference(N2), repeat=2))  # (N1 ⇔ N2) x (N1 ⇔ N2)
result4 = set(itertools.product(N1.union(N2), repeat=2))                 # (N1 ∪ N2) x (N1 ∪ N2)
print("(N1 x N2) ⇔ (N2 x N1) =", result1)
print("(N1 x N2) ∪ (N2 x N1) =", result2)
print("(N1 ⇔ N2) x (N1 ⇔ N2) =", result3)
print("(N1 ∪ N2) x (N1 ∪ N2) =", result4)
print()
def plot_set(ax, set_data, title, color='blue'):
    if not set_data:
        ax.text(0.5, 0.5, 'Пустое множество', ha='center', va='center')
        ax.set_title(title)
        return
    x, y = zip(*set_data)
    ax.scatter(x, y, color=color, s=100)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title(title)
    ax.grid(True)
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
plot_set(axes[0, 0], list(N1_x_N2), 'N1 x N2', 'blue')
plot_set(axes[0, 1], list(N2_x_N1), 'N2 x N1', 'green')
plot_set(axes[1, 0], list(result1), '(N1 x N2) ⇔ (N2 x N1)', 'red')
plot_set(axes[1, 1], list(result2), '(N1 x N2) ∪ (N2 x N1)', 'purple')
plt.tight_layout()
plt.show()

while True: # проверка на ввод мощности мн-ва
    try:
        n = int(input("Введите мощность множества X (1 ≤ n ≤ 100): "))
        if 1 <= n <= 100:
            break
        else:
            print("Ошибка: мощность должна быть в диапазоне от 1 до 100!")
    except ValueError:
        print("Ошибка: введите целое число!")
X = list(range(1, n + 1))
R = [(x, y) for x in X for y in X if x % 2 == 1 and y % 2 == 1]
Q = [(x, y) for x in X for y in X if x <= y and y % 2 == 0]
print("\nОтношение R (x нечётно, y нечётно):")
print(R)
print("\nОтношение Q (x ≤ y, y чётно):")
print(Q)

RoQ = []
for (x, z) in R:
    for (a, y) in Q:
        if z == a:
            RoQ.append((x, y))
RoQ = list(set(RoQ))  # убираем дубликаты
print("\nКомпозиция RoQ:")
print(RoQ)

def relation_matrix(rel, n):
    mat = np.zeros((n, n), dtype=int)
    for (x, y) in rel:
        if 1 <= x <= n and 1 <= y <= n:
            mat[x-1, y-1] = 1
    return mat
MR = relation_matrix(R, n)
MQ = relation_matrix(Q, n)
MRoQ = relation_matrix(RoQ, n)
print("\nМатрица отношения R:")
print(MR)
print("\nМатрица отношения Q:")
print(MQ)
print("\nМатрица отношения RoQ:")
print(MRoQ)

def domain_and_range(rel):
    domain = set(x for (x, y) in rel)
    range_set = set(y for (x, y) in rel)
    return domain, range_set
dom_R, ran_R = domain_and_range(R)
dom_Q, ran_Q = domain_and_range(Q)
print("\nОбласть определения R:", dom_R)
print("Область значений R:", ran_R)
print("Область определения Q:", dom_Q)
print("Область значений Q:", ran_Q)

def check_properties(rel, n):
    X = set(range(1, n + 1))
    matrix = relation_matrix(rel, n)
    reflexive = all(matrix[i, i] == 1 for i in range(n)) # рефлексивность
    irreflexive = all(matrix[i, i] == 0 for i in range(n)) # антирефлексивность
    symmetric = np.array_equal(matrix, matrix.T) # симметричность
    antisymmetric = True 
    for i in range(n):
        for j in range(n):
            if i != j and matrix[i, j] == 1 and matrix[j, i] == 1:
                antisymmetric = False
                break
    transitive = True
    M_sq = np.dot(matrix, matrix)
    for i in range(n):
        for j in range(n):
            if M_sq[i, j] >= 1 and matrix[i, j] == 0:
                transitive = False
                break
    return {
        'рефлексивное': reflexive,
        'антирефлексивное': irreflexive,
        'симметричное': symmetric,
        'антисимметричное': antisymmetric,
        'транзитивное': transitive
    }
props_R = check_properties(R, n)
props_Q = check_properties(Q, n)
print("\nСвойства отношения R:")
for prop, value in props_R.items():
    print(f"- {prop}: {value}")
print("\nСвойства отношения Q:")
for prop, value in props_Q.items():
    print(f"- {prop}: {value}")


def warshal_closure(matrix): # алгоритм Уоршелла - для нечётных вариантов
    n = len(matrix)
    closure = matrix.copy()
    for k in range(n):
        for i in range(n):
            for j in range(n):
                closure[i, j] = closure[i, j] or (closure[i, k] and closure[k, j])
    return closure
def reflexive_closure(matrix): # рефлексивное замыкание
    n = len(matrix)
    closure = matrix.copy()
    for i in range(n):
        closure[i, i] = 1
    return closure
def symmetric_closure(matrix): # симметричное замыкание
    return np.logical_or(matrix, matrix.T).astype(int)
print("РАБОТА С ЗАМЫКАНИЯМИ")

while True:
    print("\nВыберите отношение:")
    print("1 - R")
    print("2 - Q")
    print("0 - Выход")
    choice_rel = input("Ваш выбор: ")
    if choice_rel == '0':
        break
    if choice_rel not in ['1', '2']:
        print("Неверный выбор!")
        continue
    print("\nВыберите тип замыкания:")
    print("1 - Рефлексивное")
    print("2 - Симметричное") 
    print("3 - Транзитивное (алгоритм Уоршелла)")
    print("0 - Назад")
    choice_closure = input("Ваш выбор: ")
    if choice_closure == '0':
        continue
    if choice_closure not in ['1', '2', '3']:
        print("Неверный выбор!")
        continue
    if choice_rel == '1':
        rel_name = "R"
        matrix = MR
        relation = R
    else:
        rel_name = "Q" 
        matrix = MQ
        relation = Q
    print(f"\nИсходное отношение {rel_name}:")
    print(relation)
    print(f"Матрица отношения {rel_name}:")
    print(matrix)
    if choice_closure == '1':
        closure_matrix = reflexive_closure(matrix)
        closure_type = "рефлексивное"
    elif choice_closure == '2':
        closure_matrix = symmetric_closure(matrix)
        closure_type = "симметричное"
    else:
        closure_matrix = warshal_closure(matrix)
        closure_type = "транзитивное"
    closure_pairs = []
    for i in range(n):
        for j in range(n):
            if closure_matrix[i, j] == 1:
                closure_pairs.append((i + 1, j + 1))
    print(f"\n{closure_type.capitalize()} замыкание отношения {rel_name}:")
    print(closure_pairs)
    print(f"Матрица замыкания:")
    print(closure_matrix)
print("\nПрограмма завершена.")