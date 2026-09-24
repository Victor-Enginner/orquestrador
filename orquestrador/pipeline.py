"""Pipeline MVP — descoberta → grafo (Semantica MVP) → simulação (MatrAIx)
→ validação (veto) → fila de produção terminando em GATE HUMANO.

Princípio 3: aprovação humana obrigatória antes de publicar — nada aqui
publica sozinho. Uso (a partir da raiz do repo orquestrador/):

    python3 -m orquestrador.pipeline [numero-do-experimento]
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from adapters.matraix_adapter import simular             # noqa: E402
from adapters.semantica_adapter import ContextGraph      # noqa: E402
from orquestrador.discovery import descobrir             # noqa: E402
from orquestrador.models import Namespace                # noqa: E402
from orquestrador.validation import validar              # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
EXPERIMENTOS = RAIZ / "experiments"


def rodar(experimento: str = "001") -> dict:
    dir_exp = EXPERIMENTOS / f"exp-{experimento}"
    grafo = ContextGraph(dir_exp / "graph.jsonl")
    dir_exp.mkdir(parents=True, exist_ok=True)

    relatorio: list[str] = [
        f"# Experimento {experimento} — {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "> MatrAIx = **simulação determinística** · Semantica MVP = grafo JSONL ·",
        "> produção termina em **GATE HUMANO** (nada publica sozinho).",
        "",
    ]
    fila_gate: list[dict] = []
    ideias = descobrir()

    for ideia in ideias:
        grafo.registrar(Namespace.DISCOVERY, "ideia", ideia.to_dict())

        sim = simular(ideia)
        grafo.registrar(Namespace.MATRAIX, "simulacao", {
            "ideia_id": ideia.id,
            "titulo": ideia.titulo,
            "versao_motor": sim.versao_motor,
            "interesse_medio": sim.interesse_medio,
            "conversao_simulada": sim.taxa_conversao_simulada,
            "objecoes": sim.objecoes,
        })

        ver = validar(ideia, sim)
        grafo.registrar(Namespace.VALIDATION, "decisao", {
            "ideia_id": ideia.id,
            "aprovada": ver.aprovada,
            "justificativa": ver.justificativa,
            "regras": ver.regras_aplicadas,
        })

        icone = "✅" if ver.aprovada else "⛔"
        relatorio += [
            f"## {icone} {ideia.id} — {ideia.titulo}",
            f"- interesse simulado: **{sim.interesse_medio}** · "
            f"conversão simulada: **{sim.taxa_conversao_simulada}**",
            f"- objeções: {'; '.join(sim.objecoes) if sim.objecoes else 'nenhuma forte'}",
            f"- veredito: {'APROVADA → gate humano' if ver.aprovada else 'REJEITADA'} — {ver.justificativa}",
            "",
        ]

        if ver.aprovada:
            fila_gate.append({
                "ideia_id": ideia.id,
                "titulo": ideia.titulo,
                "ativo": ideia.ativo,
                "faixa_preco": ideia.faixa_preco,
            })

    (dir_exp / "fila-gate-humano.json").write_text(
        json.dumps(fila_gate, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (dir_exp / "relatorio.md").write_text("\n".join(relatorio) + "\n", encoding="utf-8")

    grafo.registrar(Namespace.PRODUCTION, "gate_humano", {
        "fila": fila_gate,
        "nota": "PRINCÍPIO 3: aprovação humana obrigatória antes de publicar",
    })

    return {
        "experimento": experimento,
        "ideias": len(ideias),
        "aprovadas": len(fila_gate),
        "dir": str(dir_exp),
    }


if __name__ == "__main__":
    exp = sys.argv[1] if len(sys.argv) > 1 else "001"
    print(json.dumps(rodar(exp), ensure_ascii=False))
