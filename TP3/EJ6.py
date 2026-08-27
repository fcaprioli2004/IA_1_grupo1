import random

# ==========================================
# DATOS DEL PROBLEMA
# ==========================================
PRECIOS = [100, 50, 115, 25, 200, 30, 40, 100, 100, 100]
PESOS   = [300, 200, 450, 145, 664, 90, 150, 355, 401, 395]
PESO_MAXIMO = 1000  # Modificar según el límite requerido
N_ELEMENTOS = len(PRECIOS)

# HIPERPARÁMETROS DEL ALGORITMO GENÉTICO
TAM_POBLACION = 30     # N (par)
PROB_CRUCE = 0.85
PROB_MUTACION = 0.05
NUM_GENERACIONES = 60

# ==========================================
# 6.1 Y 6.2 REPRESENTACIÓN, CONTROL Y POBLACIÓN
# ==========================================
def calcular_peso_y_precio(individuo):
    peso = sum(gen * w for gen, w in zip(individuo, PESOS))
    precio = sum(gen * p for gen, p in zip(individuo, PRECIOS))
    return peso, precio

def reparar_individuo(individuo):
    """Garantiza que el individuo no exceda el peso máximo."""
    ind = individuo.copy()
    peso, _ = calcular_peso_y_precio(ind)
    
    # Si excede el peso, apaga cajas aleatoriamente hasta ser factible
    cajas_activas = [i for i, gen in enumerate(ind) if gen == 1]
    random.shuffle(cajas_activas)
    
    while peso > PESO_MAXIMO and cajas_activas:
        idx = cajas_activas.pop()
        ind[idx] = 0
        peso, _ = calcular_peso_y_precio(ind)
        
    return ind

def crear_individuo():
    ind = [random.choice([0, 1]) for _ in range(N_ELEMENTOS)]
    return reparar_individuo(ind)

def generar_poblacion(n):
    return [crear_individuo() for _ in range(n)]

# ==========================================
# 6.3 EVALUACIÓN E IDONEIDAD (RULETA)
# ==========================================
def evaluar_fitness(individuo):
    peso, precio = calcular_peso_y_precio(individuo)
    return precio if peso <= PESO_MAXIMO else 0

def seleccion_ruleta(poblacion, num_padres):
    fitness_vals = [evaluar_fitness(ind) for ind in poblacion]
    suma_fitness = sum(fitness_vals)
    
    # En caso de que todos tengan fitness 0
    if suma_fitness == 0:
        return random.choices(poblacion, k=num_padres)
    
    probabilidades = [f / suma_fitness for f in fitness_vals]
    return random.choices(poblacion, weights=probabilidades, k=num_padres)

# ==========================================
# 6.4 CRUCE, MUTACIÓN Y VERIFICACIÓN
# ==========================================
def cruzar(p1, p2):
    if random.random() < PROB_CRUCE:
        punto = random.randint(1, N_ELEMENTOS - 1)
        hijo1 = p1[:punto] + p2[punto:]
        hijo2 = p2[:punto] + p1[punto:]
    else:
        hijo1, hijo2 = p1.copy(), p2.copy()
    return hijo1, hijo2

def mutar(individuo):
    for i in range(len(individuo)):
        if random.random() < PROB_MUTACION:
            individuo[i] = 1 - individuo[i]  # Bit-flip
    return individuo

# ==========================================
# 6.5 BUCLE PRINCIPAL (DETENCIÓN Y RESULTADOS)
# ==========================================
def ejecutar_algoritmo():
    poblacion = generar_poblacion(TAM_POBLACION)
    mejor_global = None
    mejor_fitness = -1

    for gen in range(NUM_GENERACIONES):
        # Evaluar mejor de la generación actual
        for ind in poblacion:
            fit = evaluar_fitness(ind)
            if fit > mejor_fitness:
                mejor_fitness = fit
                mejor_global = ind.copy()

        # Selección de N/2 parejas (N padres en total)
        padres = seleccion_ruleta(poblacion, TAM_POBLACION)
        nueva_poblacion = []

        # Cruce y Mutación por pares
        for i in range(0, TAM_POBLACION, 2):
            h1, h2 = cruzar(padres[i], padres[i+1])
            
            # Mutar y verificar factibilidad
            h1 = reparar_individuo(mutar(h1))
            h2 = reparar_individuo(mutar(h2))
            
            nueva_poblacion.extend([h1, h2])

        poblacion = nueva_poblacion

    # Resultados finales
    peso_final, precio_final = calcular_peso_y_precio(mejor_global)
    cajas_seleccionadas = [i + 1 for i, gen in enumerate(mejor_global) if gen == 1]

    print("=== MEJOR SOLUCIÓN ENCONTRADA ===")
    print(f"Cromosoma binario: {mejor_global}")
    print(f"Cajas cargadas (j): {cajas_seleccionadas}")
    print(f"Peso total: {peso_final} / {PESO_MAXIMO}")
    print(f"Precio total: {precio_final}")

if __name__ == "__main__":
    ejecutar_algoritmo()