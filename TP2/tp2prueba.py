import matplotlib.pyplot as plt
import networkx as nx
from collections import deque

ADJACENCY = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A', 'K'],
    'D': ['B', 'M'],
    'E': ['N'],
    'G': ['I', 'P'],
    'I': ['G', 'Q', 'W'],
    'W': ['I', 'K'],
    'K': ['W', 'C', 'M', 'T'],
    'M': ['K', 'D', 'N', 'F'],
    'N': ['M', 'E'],
    'P': ['G', 'Q'],
    'Q': ['P', 'I', 'R'],
    'R': ['Q', 'T'],
    'T': ['R', 'K'],
    'F': ['M']
}

def step_cost(target_node):
    return 50 if target_node == 'W' else 1

def build_search_tree_with_costs(start='I', goal='F', max_depth=13):
    tree = nx.DiGraph()
    node_id = 0
    root_name = f"{start}_{node_id}"
    
    tree.add_node(root_name, state=start, g_cost=0, is_goal=(start == goal), depth=0)
    queue = deque([(start, [start], root_name, 0, 0)])
    solutions = []

    while queue:
        curr_state, path, parent_node, depth, current_g = queue.popleft()
        
        if curr_state == goal:
            solutions.append((path, current_g, depth))
            continue
            
        if depth >= max_depth:
            continue

        for neighbor in ADJACENCY.get(curr_state, []):
            if neighbor not in path:  # Evitar ciclos en la misma rama
                node_id += 1
                child_name = f"{neighbor}_{node_id}"
                c = step_cost(neighbor)
                child_g = current_g + c
                is_goal = (neighbor == goal)
                
                tree.add_node(child_name, state=neighbor, g_cost=child_g, is_goal=is_goal, depth=depth + 1)
                tree.add_edge(parent_node, child_name, weight=c)
                queue.append((neighbor, path + [neighbor], child_name, depth + 1, child_g))
                
    return tree, solutions

def tree_layout_non_overlapping(G, root, vert_gap=1.2):
    """Calcula coordenadas evitando colisiones espaciales entre subárboles."""
    pos = {}
    current_x = [0]

    def assign_positions(node, depth):
        children = list(G.successors(node))
        if not children:
            pos[node] = (current_x[0], -depth * vert_gap)
            current_x[0] += 1.2
        else:
            for child in children:
                assign_positions(child, depth + 1)
            child_x = [pos[c][0] for c in children]
            pos[node] = (sum(child_x) / len(child_x), -depth * vert_gap)

    assign_positions(root, 0)
    return pos

# --- Ejecución para 13 pasos ---
MAX_PASOS = 13
tree, solutions = build_search_tree_with_costs(start='I', goal='F', max_depth=MAX_PASOS)
root_id = "I_0"
pos = tree_layout_non_overlapping(tree, root_id, vert_gap=1.5)

print(f"--- Soluciones encontradas hasta profundidad {MAX_PASOS} ---")
for path, cost, depth in sorted(solutions, key=lambda x: (x[1], x[2])):
    print(f"Costo g = {cost:2d} | Pasos: {depth:2d} | {' -> '.join(path)}")

# Dimensionamiento automático proporcional a la profundidad y cantidad de hojas
x_coords = [p[0] for p in pos.values()]
y_coords = [p[1] for p in pos.values()]
fig_width = max(24, (max(x_coords) - min(x_coords)) * 0.28)
fig_height = max(14, (max(y_coords) - min(y_coords)) * -0.55)

fig, ax = plt.subplots(figsize=(fig_width, fig_height))

node_labels = {
    node: f"{data['state']}\n(g={data['g_cost']})" 
    for node, data in tree.nodes(data=True)
}

colors = []
for node, data in tree.nodes(data=True):
    if data['state'] == 'I' and node == root_id:
        colors.append('#FFF176')  # Amarillo (Inicio)
    elif data['is_goal']:
        colors.append('#81C784')  # Verde (Meta F)
    elif data['state'] == 'W':
        colors.append('#FF8A80')  # Rojo suave (Paso costoso)
    else:
        colors.append('#ECEFF1')

# Dibujo de nodos y aristas con escala compacta
nx.draw_networkx_nodes(tree, pos, node_color=colors, node_size=550, edgecolors='#37474F', ax=ax)
nx.draw_networkx_labels(tree, pos, labels=node_labels, font_size=6, font_weight='bold', ax=ax)
nx.draw_networkx_edges(tree, pos, arrows=True, arrowsize=6, edge_color='#B0BEC5', width=0.8, ax=ax)

edge_labels = nx.get_edge_attributes(tree, 'weight')
nx.draw_networkx_edge_labels(tree, pos, edge_labels=edge_labels, font_size=5, font_color='#D32F2F', ax=ax)

plt.title(f"Árbol de Búsqueda (Profundidad = {MAX_PASOS} pasos)", fontsize=16, fontweight='bold')
plt.axis('off')
plt.tight_layout()

# Exportación en alta definición para poder hacer zoom sin perder nitidez
plt.savefig("arbol_busqueda_13_pasos.png", dpi=300, bbox_inches='tight')
print("\nImagen guardada como 'arbol_busqueda_13_pasos.png'")

plt.show()