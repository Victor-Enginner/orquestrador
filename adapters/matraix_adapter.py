"""Adapter MatrAIx — simulação de personas DETERMINÍSTICA (hash-based).

O texto-fonte define o papel do MatrAIx: 'simular personas heterogêneas
testando ideias, ofertas, páginas, chatbots e produtos', e a regra:
'MatrAIx gera evidência simulada'. Este adapter é um MOTOR DETERMINÍSTICO
de stub: mesmo input + versão do motor = mesmo resultado (pré-requisito
do trace reproduzível). Quando o MatrAIx real (LLM) for integrado,
substitui-se este módulo sem tocar no pipeline — é para isso que existe.
"""

from __future__ import annotations

import hashlib

from orquestrador.models import Persona, RespostaPersona, SimulacaoMatrAIx

VERSAO_MOTOR = "matraix-stub-deterministico-0.1"

PERSONAS = [
    Persona("p1", "iniciante em e-commerce", "R$ 20-50", 0.35),
    Persona("p2", "freelancer buscando renda extra", "R$ 10-30", 0.45),
    Persona("p3", "pequeno lojista", "R$ 50-200", 0.55),
    Persona("p4", "profissional de nicho (adv/contab)", "R$ 37-97", 0.60),
    Persona("p5", "caçador de promoções", "R$ 5-20", 0.25),
]


def _h(*partes: str) -> float:
    """Hash estável → float 0..1 (determinístico entre execuções e SOs)."""
    dig = hashlib.sha256("|".join(partes).encode()).hexdigest()
    return int(dig[:12], 16) / 16**12


def simular(ideia) -> SimulacaoMatrAIx:
    respostas: list[RespostaPersona] = []
    interesses: list[float] = []
    objecoes: list[str] = []
    conversoes: list[bool] = []

    for p in PERSONAS:
        i = round(
            0.35 + 0.45 * _h(VERSAO_MOTOR, ideia.id, p.id, "interesse") - 0.15 * p.ceticismo,
            3,
        )
        aceita = i >= 0.5
        respostas.append(RespostaPersona(
            p.id, "interesse",
            f"interesse {i:.2f} ({'acima' if aceita else 'abaixo'} do limiar 0.50)",
            aceita,
        ))
        interesses.append(i)

        if not aceita:
            objecoes.append(f"{p.id}: interesse abaixo do limiar")
            continue

        j = _h(VERSAO_MOTOR, ideia.id, p.id, "objecao")
        tipos = ["preço", "confiança na fonte", "esforço necessário", "nenhuma forte"]
        tipo_obj = tipos[int(j * 4) % 4]
        obj_forte = tipo_obj != "nenhuma forte" and j < p.ceticismo
        if obj_forte:
            objecoes.append(f"{p.id}: objeção de {tipo_obj}")
            respostas.append(RespostaPersona(p.id, "objecao", f"objeção de {tipo_obj}", False))
            continue
        respostas.append(RespostaPersona(p.id, "objecao", "sem objeção forte", True))

        conv = _h(VERSAO_MOTOR, ideia.id, p.id, "conversao") < i  # limitada pelo interesse
        conversoes.append(conv)
        respostas.append(RespostaPersona(
            p.id, "conversao", "converteria" if conv else "não converteria agora", conv,
        ))

    return SimulacaoMatrAIx(
        ideia_id=ideia.id,
        versao_motor=VERSAO_MOTOR,
        interesse_medio=round(sum(interesses) / len(interesses), 3),
        objecoes=sorted(set(objecoes)),
        taxa_conversao_simulada=round(sum(conversoes) / len(PERSONAS), 3),
        respostas=respostas,
    )
