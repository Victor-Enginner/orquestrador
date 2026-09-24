"""Agente de Validação — poder de veto (Princípio 2). Determinístico.

Veredito = função de: evidência presente, bloqueadores declarados e
interesse/conversão SIMULADOS do MatrAIx. Nada aqui alega previsão de
mercado — o texto-fonte é explícito: 'usuários reais confirmam ou
rejeitam a hipótese'.
"""

from __future__ import annotations

from orquestrador.models import Ideia, SimulacaoMatrAIx, Veredito

INTERESSE_MINIMO = 0.50
CONVERSAO_MINIMA = 0.20
CONFIANCA_MINIMA = 0.20


def validar(ideia: Ideia, sim: SimulacaoMatrAIx) -> Veredito:
    regras: list[str] = []

    if not ideia.evidencias:
        regras.append(
            f"R1: sem evidência (url+trecho) — descartada (limiar {CONFIANCA_MINIMA})"
        )
    elif all(e.confianca < CONFIANCA_MINIMA for e in ideia.evidencias):
        regras.append(f"R1: evidência abaixo da confiança mínima {CONFIANCA_MINIMA}")

    if ideia.bloqueadores:
        regras.append("R2: bloqueadores declarados → " + "; ".join(ideia.bloqueadores))

    if sim.interesse_medio < INTERESSE_MINIMO:
        regras.append(f"R3: interesse simulado {sim.interesse_medio} < {INTERESSE_MINIMO}")

    if sim.taxa_conversao_simulada < CONVERSAO_MINIMA:
        regras.append(
            f"R4: conversão simulada {sim.taxa_conversao_simulada} < {CONVERSAO_MINIMA}"
        )

    if regras:
        return Veredito(
            aprovada=False,
            justificativa="veto do validador: " + " | ".join(regras),
            regras_aplicadas=regras,
        )

    return Veredito(
        aprovada=True,
        justificativa=(
            f"passou: interesse {sim.interesse_medio} ≥ {INTERESSE_MINIMO}, "
            f"conversão simulada {sim.taxa_conversao_simulada} ≥ {CONVERSAO_MINIMA}, "
            "sem bloqueadores. ATENÇÃO: conversão é SIMULADA — usuários reais "
            "confirmam ou rejeitam (gate humano)."
        ),
        regras_aplicadas=["limiares R3/R4 atendidos", "R1 evidência presente"],
    )
