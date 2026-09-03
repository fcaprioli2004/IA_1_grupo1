from __future__ import annotations
from dataclasses import dataclass
from typing import FrozenSet, Set, Tuple, List
import itertools
import pandas as pd
from IPython.display import display, Markdown

# ==============================================================================
# 1. ESTRUCTURAS DE DATOS INMUTABLES
# ==============================================================================

@dataclass(frozen=True, slots=True)
class Literal:
    """Literal proposicional inmutable (ej: 'a' o '¬a')."""
    name: str
    is_negated: bool = False

    def complement(self) -> Literal:
        return Literal(self.name, not self.is_negated)

    def __repr__(self) -> str:
        return f"¬{self.name}" if self.is_negated else self.name


@dataclass(frozen=True, slots=True)
class Clause:
    """Disyunción inmutable de literales únicos."""
    literals: FrozenSet[Literal]

    @classmethod
    def from_literals(cls, *literals: Literal) -> Clause:
        return cls(frozenset(literals))

    def is_empty(self) -> bool:
        return len(self.literals) == 0

    def __len__(self) -> int:
        return len(self.literals)

    def __repr__(self) -> str:
        if self.is_empty():
            return "□ (False)"
        return " ∨ ".join(sorted(str(lit) for lit in self.literals))


@dataclass
class StepTrace:
    step: int
    parent_1: Clause
    parent_2: Clause
    resolved_on: Literal
    resolvent: Clause


# ==============================================================================
# 2. MOTOR DE RESOLUCIÓN PROPOSICIONAL (PL-Resolution)
# ==============================================================================

class PLResolutionEngine:
    @staticmethod
    def resolve(c1: Clause, c2: Clause) -> Set[Tuple[Clause, Literal]]:
        resolvents = set()
        for lit in c1.literals:
            comp = lit.complement()
            if comp in c2.literals:
                new_lits = (c1.literals - {lit}) | (c2.literals - {comp})
                
                # Descartar tautologías automáticas (P ∨ ¬P)
                names = {l.name for l in new_lits}
                is_tautology = any(
                    Literal(n, False) in new_lits and Literal(n, True) in new_lits 
                    for n in names
                )
                if not is_tautology:
                    resolvents.add((Clause(frozenset(new_lits)), lit))
        return resolvents

    @classmethod
    def prove_by_refutation(
        cls, 
        kb_clauses: Set[Clause], 
        query: Literal
    ) -> Tuple[bool, List[StepTrace]]:
        # Incorporar formalmente la hipótesis negada (~query)
        negated_query = Clause.from_literals(query.complement())
        clauses: Set[Clause] = set(kb_clauses) | {negated_query}
        trace: List[StepTrace] = []
        step_counter = 1
        resolved_pairs: Set[Tuple[Clause, Clause]] = set()

        while True:
            # Estrategia de búsqueda: priorizar cláusulas unitarias / de menor longitud
            clause_list = sorted(list(clauses), key=lambda c: len(c))
            pairs = []
            for c1, c2 in itertools.combinations(clause_list, 2):
                pair_key = (c1, c2) if id(c1) < id(c2) else (c2, c1)
                if pair_key not in resolved_pairs:
                    pairs.append((c1, c2))

            pairs.sort(key=lambda p: (len(p[0]) + len(p[1]), len(p[0]), len(p[1])))
            new_clauses_derived = set()

            for c1, c2 in pairs:
                pair_key = (c1, c2) if id(c1) < id(c2) else (c2, c1)
                resolved_pairs.add(pair_key)
                resolutions = cls.resolve(c1, c2)

                for resolvent, resolved_lit in resolutions:
                    trace.append(StepTrace(
                        step=step_counter,
                        parent_1=c1,
                        parent_2=c2,
                        resolved_on=resolved_lit,
                        resolvent=resolvent
                    ))
                    step_counter += 1

                    if resolvent.is_empty():
                        return True, trace  # Contradicción hallada: insatisfactible

                    if resolvent not in clauses:
                        new_clauses_derived.add(resolvent)

                # Si se generó una cláusula unitaria, repriorizar de inmediato
                if any(len(res[0]) == 1 for res in resolutions):
                    break

            if not new_clauses_derived or new_clauses_derived.issubset(clauses):
                return False, trace  # Punto fijo: no se deriva contradicción

            clauses.update(new_clauses_derived)


# ==============================================================================
# 3. BASE DE CONOCIMIENTO (EJERCICIO 3), EJECUCIÓN Y VISUALIZACIÓN
# ==============================================================================

# Literales del dominio
a, b, c, d, e, f, g = [Literal(var) for var in ["a", "b", "c", "d", "e", "f", "g"]]

# Transformación formal de implicaciones a FNC
kb_ejercicio_3 = {
    Clause.from_literals(b.complement(), c.complement(), a),  # R1: ¬b ∨ ¬c ∨ a
    Clause.from_literals(d.complement(), e.complement(), b),  # R2: ¬d ∨ ¬e ∨ b
    Clause.from_literals(g.complement(), e.complement(), b),  # R3: ¬g ∨ ¬e ∨ b
    Clause.from_literals(e.complement(), c),                  # R4: ¬e ∨ c
    Clause.from_literals(d),                                  # R5: d
    Clause.from_literals(e),                                  # R6: e
    Clause.from_literals(a.complement(), g.complement(), f),  # R7: ¬a ∨ ¬g ∨ f
}

meta = a  # Proposición objetivo a validar

# Ejecución de la inferencia
es_inconsistente, traza = PLResolutionEngine.prove_by_refutation(kb_ejercicio_3, meta)

# Renderizado en Jupyter
tabla = pd.DataFrame([
    {
        "Paso": t.step,
        "Cláusula 1": str(t.parent_1),
        "Cláusula 2": str(t.parent_2),
        "Literal Cancelado": str(t.resolved_on),
        "Resolvente Generado": str(t.resolvent)
    }
    for t in traza
])

display(Markdown(f"### Prueba por Refutación: $KB \\models {meta}$"))
display(Markdown(f"**Hipótesis negada incorporada:** $\\neg {meta}$"))
display(tabla)

if es_inconsistente:
    display(Markdown(
        f"**Dictamen:** Se alcanzó la cláusula vacía ($\\square$). "
        f"El conjunto $KB \\cup \\{{\\neg {meta}\\}}$ es **inconsistente** (insatisfactible); "
        f"por ende, queda formalmente demostrado que **$KB \\models {meta}$ es VERDADERO**."
    ))
else:
    display(Markdown(f"**Dictamen:** Punto fijo alcanzado. No existe inconsistencia. $KB \\not\\models {meta}$."))