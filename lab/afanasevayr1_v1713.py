import matplotlib.pyplot as plt
import numpy as np
from matplotlib_venn import venn3, venn3_circles
from matplotlib.patches import Patch

powers = {
    '000': 30,  # {1} - поидее находится вне всех множеств
    '001': 7,   # {2} - C
    '010': 5,   # {3} - только B  
    '011': 2,   # {4} - B и C
    '100': 6,   # {5} - только A
    '101': 4,   # {6} - A и C
    '110': 8,   # {7} - A и B
    '111': 2    # {8} - A, B и C
}

def calculate_set_operation(powers_dict, operation):
    if operation == 'A∪B':
        # A ∪ B = зоны: {5}, {7}, {8}, {3}, {4}
        return (powers_dict['100'] + powers_dict['110'] + powers_dict['111'] + 
                powers_dict['010'] + powers_dict['011'])
    
    elif operation == 'CΔ(A∪B)':
        # C Δ (A∪B) = (C ∪ (A∪B)) \ (C ∩ (A∪B))
        # = зоны только C + зоны только A∪B
        only_C = powers_dict['001']  # {2}
        only_AUB = (powers_dict['100'] + powers_dict['010'] + powers_dict['110'])  # {5}, {3}, {7}
        return only_C + only_AUB

def plot_venn_custom(powers_dict, title, highlight_zones=None):
    plt.figure(figsize=(10, 8))
    
    v = venn3(subsets=(1, 1, 1, 1, 1, 1, 1), 
              set_labels=('A', 'B', 'C'))
    
    # {5} = только A = 100
    # {3} = только B = 010  
    # {2} = только C = 001
    # {7} = A∩B = 110
    # {6} = A∩C = 101
    # {4} = B∩C = 011
    # {8} = A∩B∩C = 111
    
    v.get_label_by_id('100').set_text('5: ' + str(powers_dict['100']))  # {5}
    v.get_label_by_id('010').set_text('3: ' + str(powers_dict['010']))  # {3}
    v.get_label_by_id('001').set_text('2: ' + str(powers_dict['001']))  # {2}
    v.get_label_by_id('110').set_text('7: ' + str(powers_dict['110']))  # {7}
    v.get_label_by_id('101').set_text('6: ' + str(powers_dict['101']))  # {6}
    v.get_label_by_id('011').set_text('4: ' + str(powers_dict['011']))  # {4}
    v.get_label_by_id('111').set_text('8: ' + str(powers_dict['111']))  # {8}
    
    if highlight_zones:
        for zone_id, color in highlight_zones.items():
            if zone_id in ['100', '010', '001', '110', '101', '011', '111']:
                v.get_patch_by_id(zone_id).set_color(color)
            elif zone_id == '000':  # внешняя область 1
                rect = plt.Rectangle((-0.7, -0.7), 1.4, 1.4, 
                                   fill=True, color=color, alpha=0.3)
                plt.gca().add_patch(rect)
    
    plt.title(title, fontsize=14)
    plt.axis('on')
    plt.grid(True, alpha=0.3)
    plt.show()

# исходные множества
print("ШАГ 1: Исходные множества")
print("Нумерация зон согласно изображению:")
print("{1} = 30 (вне всех)")
print("{2} = 7 (только C)")  
print("{3} = 5 (только B)")
print("{4} = 2 (B∩C)")
print("{5} = 6 (только A)")
print("{6} = 4 (A∩C)")
print("{7} = 8 (A∩B)")
print("{8} = 2 (A∩B∩C)")

plot_venn_custom(powers, "Исходные множества с нумерацией зон")

# A ∪ B
print("\nШАГ 2: Множество A ∪ B")
A_union_B = calculate_set_operation(powers, 'A∪B')
print(f"Мощность A ∪ B: {A_union_B}")
print("Зоны A ∪ B: {5}, {3}, {7}, {4}, {8}")
plot_venn_custom(powers, "Множество A ∪ B (зоны {5}, {3}, {7}, {4}, {8})", 
                {'100': 'red', '010': 'red', '110': 'red', '011': 'red', '111': 'red'})

# C Δ (A∪B)
print("\nШАГ 3: Симметрическая разность C Δ (A∪B)")
C_delta_AUB = calculate_set_operation(powers, 'CΔ(A∪B)')
print(f"Мощность C Δ (A∪B): {C_delta_AUB}")
print("Зоны C Δ (A∪B): {2}, {5}, {3}, {7}")

plot_venn_custom(powers, "Симметрическая разность C Δ (A∪B) (зоны {2}, {5}, {3}, {7})", 
                {'001': 'blue', '100': 'blue', '010': 'blue', '110': 'blue'})

print("ИТОГОВЫЙ РЕЗУЛЬТАТ:")
print(f"Мощность множества C Δ (A∪B): {C_delta_AUB}")
print("Состав множества (согласно нумерации из изображения):")
print(f"- Зона {{2}} (только C): {powers['001']}")
print(f"- Зона {{5}} (только A): {powers['100']}") 
print(f"- Зона {{3}} (только B): {powers['010']}")
print(f"- Зона {{7}} (A∩B): {powers['110']}")
print(f"Сумма: {powers['001']} + {powers['100']} + {powers['010']} + {powers['110']} = {C_delta_AUB}")
print("="*60)