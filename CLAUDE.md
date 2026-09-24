# CLAUDE.md — Orquestrador Multiagente

Sistema que descobre → valida → produz ativos digitais com **cadeia de
evidências** e **memória compartilhada** (grafo). Implementa
`../Agentes-orquestrator.md` + arquitetura MatrAIx + Semantica (ver
`docs/DECISIONS.md` — fonte de verdade).

## Comandos

```bash
python3 -m orquestrador.pipeline            # roda experimento 001
python3 -m orquestrador.pipeline 002        # novo experimento (dir próprio)
python3 - <<'PY'                            # consultar o grafo
import sys; sys.path.insert(0, '.')
from adapters.semantica_adapter import ContextGraph
from orquestrador.models import Namespace
for ev in ContextGraph('experiments/exp-001/graph.jsonl').consultar(Namespace.VALIDATION):
    print(ev['ts'], ev['payload']['ideia_id'], ev['payload']['aprovada'])
PY
```

Stdlib pura — sem `pip install`. Python 3.12.

## Regras inegociáveis (documento §7)

1. **Evidência obrigatória:** toda oportunidade com URL + trecho; sem isso,
   descartada (R1).
2. **Veto do validador:** rejeição com justificativa estruturada registrada
   no grafo (R2 = bloqueadores legais; R3/R4 = limiares de simulação).
3. **Gate humano:** a fila de produção (`experiments/exp-NNN/fila-gate-humano.json`)
   termina SEMPRE em aprovação humana. **Nada publica sozinho.**
4. **Traço honesto:** MatrAIx = **simulação determinística** (hash — mesmo
   input = mesmo output). NUNCA apresentar como previsão de mercado real.
5. **Namespaces do grafo:** `discovery/ validation/ matraix/ production/
   distribution/ optimization/` — não inventar outros sem atualizar o enum.

## Fronteiras de integração

- `adapters/matraix_adapter.py` — trocar pelo MatrAIx real (LLM) mantendo
  a assinatura `simular(ideia) -> SimulacaoMatrAIx` e o campo `versao_motor`.
- `adapters/semantica_adapter.py` — trocar pelo Semantica real
  (semantica-agi) mantendo `registrar(ns, tipo, payload)` / `consultar(ns, tipo)`.
- MatrAIx e Semantica vivem em **repos/venvs separados** — não juntar.

## Próximos incrementos (ordem)

1. Descoberta EXTERNA (URL real + trecho verificado, confiança ≥ 0.5)
2. MatrAIx real em venv próprio (Python ≥3.12) atrás do adapter
3. Semantica real atrás do adapter (provenance/confiança/citações)
4. Produção: geração de ativos + controle de qualidade (ainda com gate humano)
5. Falha ≥2× → pausa do agente + notificação (documento §7.5)
