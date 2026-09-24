# Orquestrador Multiagente — Descoberta e Renda Autônoma

Coordena a descoberta de oportunidades, validação com **poder de veto**,
simulação de personas (**MatrAIx**) e registro auditável em grafo de
conhecimento (**Semantica**) — terminando sempre em **gate humano**.

> **Regra de ouro:** MatrAIx gera evidência *simulada* · Semantica preserva
> e relaciona · usuários reais confirmam ou rejeitam a hipótese.

## Rodar

```bash
python3 -m orquestrador.pipeline 001
```

Saída em `experiments/exp-001/`:

| Arquivo | Conteúdo |
|---|---|
| `relatorio.md` | veredito por ideia (✅/⛔ + justificativa) |
| `graph.jsonl` | grafo append-only (namespaces discovery/matraix/validation/production) |
| `fila-gate-humano.json` | aprovadas aguardando **sua** aprovação |

## Estado (MVP honesto)

- ✅ Descoberta interna (10 ideias seed), validação com veto, grafo JSONL,
  simulação determinística de 5 personas, gate humano
- 🔮 Descoberta externa com URL verificável, MatrAIx real (LLM), Semantica
  real (semantica-agi), produção/pagamento (Mercado Pago)

Ver `docs/DECISIONS.md` para arquitetura e rastro de decisões.
