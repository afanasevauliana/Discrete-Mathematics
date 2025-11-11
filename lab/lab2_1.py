import numpy as np
from collections import deque, defaultdict
import matplotlib.pyplot as plt
import networkx as nx

class Graph:
    def __init__(self, vertices, edges, name="Graph"):
        self.vertices = vertices
        self.edges = edges
        self.name = name
        self.n = len(vertices)
        self.adj_list = self._build_adj_list()
        self.adj_matrix = self._build_adj_matrix()
    
    def _build_adj_list(self):
        adj_list = {v: [] for v in self.vertices}
        for u, v in self.edges:
            adj_list[u].append(v)
            adj_list[v].append(u)
        return adj_list
    
    def _build_adj_matrix(self):
        matrix = np.zeros((self.n, self.n), dtype=int)
        vertex_to_index = {v: i for i, v in enumerate(sorted(self.vertices))}
        
        for u, v in self.edges:
            i, j = vertex_to_index[u], vertex_to_index[v]
            matrix[i][j] = 1
            matrix[j][i] = 1
        return matrix
    
    def get_degrees(self):
        degrees = {}
        for v in self.vertices:
            degrees[v] = len(self.adj_list[v])
        return degrees
    
    def get_degree_sequence(self):
        degrees = self.get_degrees()
        return sorted(degrees.values(), reverse=True)
    
    def is_connected(self):
        if not self.vertices:
            return True
        
        visited = set()
        stack = [self.vertices[0]]
        
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                stack.extend(self.adj_list[vertex])
        
        return len(visited) == len(self.vertices)
    
    def get_connected_components(self):
        visited = set()
        components = []
        
        for vertex in self.vertices:
            if vertex not in visited:
                component = []
                stack = [vertex]
                
                while stack:
                    v = stack.pop()
                    if v not in visited:
                        visited.add(v)
                        component.append(v)
                        stack.extend(self.adj_list[v])
                
                components.append(component)
        
        return components
    
    def get_diameter(self):
        if not self.is_connected():
            return float('inf')
        
        diameter = 0
        for start in self.vertices:
            distances = {}
            queue = deque([start])
            distances[start] = 0
            
            while queue:
                current = queue.popleft()
                for neighbor in self.adj_list[current]:
                    if neighbor not in distances:
                        distances[neighbor] = distances[current] + 1
                        queue.append(neighbor)
            
            diameter = max(diameter, max(distances.values()))
        
        return diameter
    
    def get_graph_invariants(self):
        degrees = self.get_degrees()
        degree_sequence = self.get_degree_sequence()
        components = self.get_connected_components()
        
        return {
            'num_vertices': len(self.vertices),
            'num_edges': len(self.edges),
            'degree_sequence': degree_sequence,
            'max_degree': max(degrees.values()),
            'min_degree': min(degrees.values()),
            'is_connected': self.is_connected(),
            'num_components': len(components),
            'diameter': self.get_diameter(),
            'degrees': degrees
        }

    def draw(self, save_path=None):
        """Визуализация графа"""
        G = nx.Graph()
        G.add_nodes_from(self.vertices)
        G.add_edges_from(self.edges)
        
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', 
                node_size=800, font_size=12, font_weight='bold', 
                edge_color='gray', linewidths=1, alpha=0.7)
        plt.title(f'Граф {self.name}')
        plt.axis('off')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Граф сохранен как {save_path}")
        plt.show()

    def display_info(self):
        """Отображение информации о графе"""
        print(f"\n{self.name}:")
        print(f"Вершины: {sorted(self.vertices)}")
        print(f"Рёбра: {sorted(self.edges)}")
        print("Матрица смежности:")
        print(self.adj_matrix)
        print(f"Степени вершин: {self.get_degrees()}")

    # ОПЕРАЦИИ НАД ГРАФАМИ
    def remove_edge(self, edge):
        """Удаление ребра"""
        new_edges = [e for e in self.edges if e != edge and (e[1], e[0]) != edge]
        return Graph(self.vertices, new_edges, f"{self.name} без ребра {edge}")
    
    def remove_vertex(self, vertex):
        """Удаление вершины"""
        new_vertices = [v for v in self.vertices if v != vertex]
        new_edges = [e for e in self.edges if e[0] != vertex and e[1] != vertex]
        return Graph(new_vertices, new_edges, f"{self.name} без вершины {vertex}")
    
    def identify_vertices(self, u, v):
        """Отождествление вершин"""
        new_vertex = min(u, v)
        remaining_vertex = max(u, v)
        
        new_vertices = [vertex for vertex in self.vertices if vertex != remaining_vertex]
        if new_vertex not in new_vertices:
            new_vertices.append(new_vertex)
        
        new_edges = []
        for edge in self.edges:
            a, b = edge
            if a == remaining_vertex:
                a = new_vertex
            if b == remaining_vertex:
                b = new_vertex
            if a != b:
                new_edge = (min(a, b), max(a, b))
                if new_edge not in new_edges:
                    new_edges.append(new_edge)
        
        return Graph(new_vertices, new_edges, f"{self.name} с отождествлением {u} и {v}")
    
    def contract_edge(self, edge):
        """Стягивание ребра"""
        return self.identify_vertices(edge[0], edge[1])
    
    def complement(self):
        """Дополнение графа"""
        all_possible_edges = []
        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):
                all_possible_edges.append((self.vertices[i], self.vertices[j]))
        
        complement_edges = [e for e in all_possible_edges if e not in self.edges and (e[1], e[0]) not in self.edges]
        return Graph(self.vertices, complement_edges, f"Дополнение {self.name}")
    
    def union(self, other):
        """Объединение графов"""
        union_vertices = list(set(self.vertices + other.vertices))
        union_edges = list(set(self.edges + other.edges))
        return Graph(union_vertices, union_edges, f"Объединение {self.name} и {other.name}")
    
    def join(self, other):
        """Соединение графов"""
        join_vertices = list(set(self.vertices + other.vertices))
        join_edges = self.edges + other.edges
        
        for u in self.vertices:
            for v in other.vertices:
                join_edges.append((u, v))
        
        join_edges = list(set(join_edges))
        return Graph(join_vertices, join_edges, f"Соединение {self.name} и {other.name}")
    
    def intersection(self, other):
        """Пересечение графов"""
        intersection_vertices = list(set(self.vertices) & set(other.vertices))
        intersection_edges = []
        
        for edge in self.edges:
            if edge in other.edges or (edge[1], edge[0]) in other.edges:
                intersection_edges.append(edge)
        
        return Graph(intersection_vertices, intersection_edges, f"Пересечение {self.name} и {other.name}")
    
    def ring_sum(self, other):
        """Кольцевая сумма (симметрическая разность)"""
        ring_vertices = list(set(self.vertices + other.vertices))
        
        edges1 = set(self.edges)
        edges2 = set(other.edges)
        
        edges1_sym = edges1 | set((v, u) for (u, v) in edges1)
        edges2_sym = edges2 | set((v, u) for (u, v) in edges2)
        
        ring_edges = list((edges1_sym ^ edges2_sym) & set(self.edges + other.edges))
        return Graph(ring_vertices, ring_edges, f"Кольцевая сумма {self.name} и {other.name}")

def check_isomorphism(G1, G2):
    print("=" * 60)
    print("ЗАДАНИЕ 1: ПРОВЕРКА ИЗОМОРФИЗМА ГРАФОВ")
    print("=" * 60)
    
    # Визуализация исходных графов
    print("\nВИЗУАЛИЗАЦИЯ ГРАФОВ:")
    G1.draw()
    G2.draw()
    
    print(f"G1: {G1.vertices} вершин, {G1.edges} рёбер")
    print(f"G2: {G2.vertices} вершин, {G2.edges} рёбер")
    print()
    
    inv1 = G1.get_graph_invariants()
    inv2 = G2.get_graph_invariants()
    
    print("ИНВАРИАНТЫ G1:")
    for key, value in inv1.items():
        print(f"  {key}: {value}")
    
    print("\nИНВАРИАНТЫ G2:")
    for key, value in inv2.items():
        print(f"  {key}: {value}")
    
    print("\nСРАВНЕНИЕ ИНВАРИАНТОВ:")
    isomorphic = True
    
    comparisons = [
        ('Число вершин', inv1['num_vertices'], inv2['num_vertices']),
        ('Число рёбер', inv1['num_edges'], inv2['num_edges']),
        ('Упорядоченный список степеней', inv1['degree_sequence'], inv2['degree_sequence']),
        ('Максимальная степень', inv1['max_degree'], inv2['max_degree']),
        ('Минимальная степень', inv1['min_degree'], inv2['min_degree']),
        ('Связность', inv1['is_connected'], inv2['is_connected']),
        ('Количество компонент связности', inv1['num_components'], inv2['num_components']),
        ('Диаметр', inv1['diameter'], inv2['diameter'])
    ]
    
    for name, val1, val2 in comparisons:
        match = val1 == val2
        isomorphic = isomorphic and match
        status = "✓ СОВПАДАЕТ" if match else "✗ НЕ СОВПАДАЕТ"
        print(f"  {name}: {val1} vs {val2} - {status}")
    
    print(f"\nРЕЗУЛЬТАТ: ГРАФЫ {'ИЗОМОРФНЫ' if isomorphic else 'НЕ ИЗОМОРФНЫ'}")
    
    return isomorphic

# ДАННЫЕ ДЛЯ ЗАДАНИЯ 1 (изоморфизм)
print("ЗАДАНИЕ 1: ПРОВЕРКА ИЗОМОРФИЗМА")
G1_vertices = [1, 2, 3, 4, 5, 6, 7]
G1_edges = [(1,2), (1,5), (1,7), (2,3), (2,4), (3,4), (4,5), (5,6), (5,7), (6,7)]

G2_vertices = [1, 2, 3, 4, 5, 6, 7]
G2_edges = [(1,2), (1,3), (1,4), (2,3), (3,4), (4,5), (4,7), (5,6), (5,7), (6,7)]

G1_task1 = Graph(G1_vertices, G1_edges, "G1 (задание 1)")
G2_task1 = Graph(G2_vertices, G2_edges, "G2 (задание 1)")

# Проверка изоморфизма для задания 1
is_isomorphic = check_isomorphism(G1_task1, G2_task1)

# ДАННЫЕ ДЛЯ ЗАДАНИЯ 2 (операции)
print("\n" + "=" * 60)
print("ЗАДАНИЕ 2: ОПЕРАЦИИ НАД ГРАФАМИ")
print("=" * 60)

G1_vertices = [1, 2, 3, 4, 5]
G1_edges = [(1,2), (1,3), (2,3), (2,5), (3,4), (4,5)]

G2_vertices = [1, 2, 3, 4, 5]
G2_edges = [(1,5), (2,3), (2,5), (3,4), (3,5), (4,5)]

G1 = Graph(G1_vertices, G1_edges, "G1 (задание 2)")
G2 = Graph(G2_vertices, G2_edges, "G2 (задание 2)")

# Визуализация графов для задания 2
print("\nИСХОДНЫЕ ГРАФЫ ДЛЯ ЗАДАНИЯ 2:")
G1.draw()
G2.draw()

G1.display_info()
G2.display_info()

# ЧАСТЬ 1: ОПЕРАЦИИ НАД G1
print("\n" + "=" * 50)
print("ЧАСТЬ 1: ОПЕРАЦИИ НАД G1")
print("=" * 50)

# Удаление ребра (1,2)
G1_no_edge = G1.remove_edge((1,2))
print("1. УДАЛЕНИЕ РЕБРА (1,2):")
G1_no_edge.display_info()
G1_no_edge.draw()

# Удаление вершины 3
G1_no_vertex = G1.remove_vertex(3)
print("2. УДАЛЕНИЕ ВЕРШИНЫ 3:")
G1_no_vertex.display_info()
G1_no_vertex.draw()

# Отождествление вершин 1 и 4
G1_identified = G1.identify_vertices(1, 4)
print("3. ОТОЖДЕСТВЛЕНИЕ ВЕРШИН 1 и 4:")
G1_identified.display_info()
G1_identified.draw()

# Стягивание ребра (2,5)
G1_contracted = G1.contract_edge((2,5))
print("4. СТЯГИВАНИЕ РЕБРА (2,5):")
G1_contracted.display_info()
G1_contracted.draw()

# ЧАСТЬ 2: БИНАРНЫЕ ОПЕРАЦИИ
print("\n" + "=" * 50)
print("ЧАСТЬ 2: БИНАРНЫЕ ОПЕРАЦИИ НАД G1 и G2")
print("=" * 50)

# Дополнение G1
G1_complement = G1.complement()
print("1. ДОПОЛНЕНИЕ G1:")
G1_complement.display_info()
G1_complement.draw()

# Объединение
G_union = G1.union(G2)
print("2. ОБЪЕДИНЕНИЕ G1 и G2:")
G_union.display_info()
G_union.draw()

# Соединение
G_join = G1.join(G2)
print("3. СОЕДИНЕНИЕ G1 и G2:")
G_join.display_info()
G_join.draw()

# Пересечение
G_intersection = G1.intersection(G2)
print("4. ПЕРЕСЕЧЕНИЕ G1 и G2:")
G_intersection.display_info()
G_intersection.draw()

# Кольцевая сумма
G_ring_sum = G1.ring_sum(G2)
print("5. КОЛЬЦЕВАЯ СУММА G1 и G2:")
G_ring_sum.display_info()
G_ring_sum.draw()

print("\n" + "=" * 60)
print("ЛАБОРАТОРНАЯ РАБОТА ВЫПОЛНЕНА!")
print("=" * 60)