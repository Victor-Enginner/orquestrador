"""Agente de Descoberta — MVP.

Regra 1 do documento: toda oportunidade precisa de URL + trecho citado.
Neste MVP a 'varredura' lê fontes INTERNAS (IDeias de projetos.md da raiz).
Fonte interna = confiança baixa por definição (0.3); evidência EXTERNA
verificável (URL real + trecho) é o próximo incremento — futuro.
"""

from __future__ import annotations

from pathlib import Path

from orquestrador.models import Evidencia, Ideia

RAIZ = Path(__file__).resolve().parent.parent.parent  # meu-portfolio/
FONTE_IDEIAS = RAIZ / "IDeias de projetos.md"

# Bloqueadores declarados por posição da ideia no documento (1-indexado):
# riscos legais/ToS que o validador usa como veto automático (Princípio 2).
BLOQUEADORES_PADRAO = {
    "1": "repost de conteúdo de terceiros: risco de direitos autorais/strikes",
    "5": "clonagem de voz de famosos: risco de violação de imagem",
    "6": "cortes de podcasts de terceiros: risco de direitos autorais",
}


def descobrir() -> list[Ideia]:
    """Extração determinística: título = linha anterior a cada bloco 'Como é:'."""
    if not FONTE_IDEIAS.exists():
        return []
    linhas = FONTE_IDEIAS.read_text(encoding="utf-8").splitlines()
    ideias: list[Ideia] = []

    for i, ln in enumerate(linhas):
        if not ln.strip().lower().startswith("como é:"):
            continue
        n = len(ideias) + 1
        titulo = next(
            (linhas[j].strip() for j in range(i - 1, -1, -1) if linhas[j].strip()),
            f"ideia-{n}",
        )
        titulo = titulo.lstrip("0123456789.-* ").rstrip(":* ")
        como = ln.strip()[len("Como é:"):].strip()
        por = next(
            (
                linhas[j].strip()[len("Por que é idiota e funciona:"):].strip()
                for j in range(i + 1, len(linhas))
                if linhas[j].strip().lower().startswith("por que")
            ),
            "",
        )
        bloq = [BLOQUEADORES_PADRAO[str(n)]] if str(n) in BLOQUEADORES_PADRAO else []

        ideias.append(Ideia(
            id=f"IDEIA-{n:02d}",
            titulo=titulo or f"ideia-{n}",
            problema=como[:200] or por[:200],
            publico="a enriquecer na descoberta externa (futuro)",
            ativo="ativo digital simples (PDF/serviço/planilha — ver doc)",
            faixa_preco="R$ 10-97",
            evidencias=[Evidencia(
                url=f"file://{FONTE_IDEIAS}#linha-{i + 1}",
                trecho=(como or por)[:140],
                fonte="interna",
                confianca=0.3,
            )],
            bloqueadores=bloq,
        ))
    return ideias
