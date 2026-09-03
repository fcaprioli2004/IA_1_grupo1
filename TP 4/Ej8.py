from itertools import combinations

def resolve(ci, cj):
    """
    Calcula todos los posibles resolventes entre dos cláusulas ci y cj.
    Cada cláusula se representa como un frozenset de literales (strings).
    Un literal negativo se representa con el prefijo '~'.
    """
    resolvents = []
    for lit in ci:
        neg_lit = lit[1:] if lit.startswith('~') else f"~{lit}"
        if neg_lit in cj:
            # Eliminar lit de ci y neg_lit de cj, luego unir
            new_clause = (ci - {lit}) | (cj - {neg_lit})
            resolvents.append(frozenset(new_clause))
    return resolvents

def pl_resolution(clauses):
    """
    Aplica el algoritmo de resolución proposicional.
    Retorna (True, history) si el conjunto es inconsistente (deriva cláusula vacía),
    o (False, history) si es consistente.
    """
    clauses = set(clauses)
    history = []
    
    while True:
        new_clauses = set()
        pairs = list(combinations(clauses, 2))
        
        for ci, cj in pairs:
            resolvents = resolve(ci, cj)
            for res in resolvents:
                if res not in clauses and res not in new_clauses:
                    new_clauses.add(res)
                    history.append((ci, cj, res))
                    # Si se produce la cláusula vacía, hay contradicción
                    if len(res) == 0:
                        return True, history
        
        # Si no se generan cláusulas nuevas, no hay contradicción
        if new_clauses.issubset(clauses):
            return False, history
            
        clauses |= new_clauses

# --- Representación de las cláusulas del Ejercicio 3 ---
# R1: ~b v ~c v a
# R2: ~d v ~e v b
# R3: ~g v ~e v b
# R4: ~e v c
# R5: d
# R6: e
# R7: ~a v ~g v f

base_knowledge = [
    frozenset({'~b', '~c', 'a'}),
    frozenset({'~d', '~e', 'b'}),
    frozenset({'~g', '~e', 'b'}),
    frozenset({'~e', 'c'}),
    frozenset({'d'}),
    frozenset({'e'}),
    frozenset({'~a', '~g', 'f'}),
]

# Probar consistencia de la base de conocimiento por sí sola
is_kb_inconsistent, _ = pl_resolution(base_knowledge)
print(f"¿La BC es inconsistente por sí sola? {is_kb_inconsistent}")

# Demostración por contradicción de que 'a' es True (BC U {~a})
goal_negated = frozenset({'~a'})
inconsistent, steps = pl_resolution(base_knowledge + [goal_negated])

print(f"¿BC U {{¬a}} es inconsistente?: {inconsistent}")
if inconsistent:
    print("\nPasos de resolución que derivaron la contradicción:")
    for ci, cj, res in steps:
        c1_str = " v ".join(ci) if ci else "□"
        c2_str = " v ".join(cj) if cj else "□"
        res_str = " v ".join(res) if res else "□ (CONTRADICCIÓN)"
        print(f"  Resolviendo ({c1_str}) y ({c2_str}) => ({res_str})")
        if not res:
            break