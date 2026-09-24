# ORQUESTRADOR — DECISIONS (MVP)

> Implementa `Agentes-orquestrator.md` (v1.0) + a arquitetura combinada
> **MatrAIx + Semantica** (texto de avaliação aprovado pelo Victor).
> Regra de ouro: **MatrAIx gera evidência simulada · Semantica preserva e
> relaciona · usuários reais confirmam ou rejeitam a hipótese.**

## 1. Inventário (2026-09-24)

| Item | Estado |
|---|---|
| Pasta | criada vazia nesta sessão |
| Fontes de requirements | `../Agentes-orquestrator.md` + texto de arquitetura colado no chat + `../IDeias de projetos.md` |
| Ambientes | Python 3.12.3 (faixa comum MatrAIx ≥3.12 e Semantica 3.10–3.13) |
| Dependências externas | **nenhuma** — stdlib puro no MVP |

## 2. Arquitetura (do texto aprovado — adaptadores, não monolito)

```
meu-portfolio/
├── orquestrador/          ← ESTE repo (coordenação + adapters)
│   ├── orquestrador/      ← agentes: discovery, validation, pipeline, models
│   ├── adapters/          ← matraix_adapter · semantica_adapter (fronteiras)
│   ├── experiments/       ← exp-NNN/{graph.jsonl, relatorio.md, fila-gate-humano.json}
│   ├── schemas/           ← (futuro) JSON Schemas compartilhados
│   └── docs/
├── MatrAIx/               ← repos separados — NÃO juntar fisicamente (decisão do texto)
└── Semantica/
```

- MatrAIx/Semantica atualizáveis/substituíveis sem quebrar o pipeline.
- Environments Python separados quando os reais entrarem (evitar sobreposição
  de pydantic/httpx/rich/embeddings no mesmo venv — risco do texto-fonte).

## 3. O que é implementado vs simulação vs futuro (MVP)

| Componente | Classe |
|---|---|
| Modelos do grafo (Ideia/Evidencia/Simulacao/Veredito/RegistroDecisao) | **implementado** |
| Descoberta: extração das 10 ideias internas com evidência (url+trecho+confiança 0.3) | **implementado** (fonte INTERNA — externa é futuro) |
| Adapter Semantica: ContextGraph JSONL append-only + namespaces + consulta | **implementado (MVP honesto)** — lib real = futuro |
| Adapter MatrAIx: motor determinístico hash-based de personas | **simulação determinística** (trace reproduzível; LLM real = futuro) |
| Validação: veto determinístico (R1 evidência, R2 bloqueadores, R3/R4 limiares) | **implementado** |
| Bloqueadores de risco (ideias 1, 5, 6: direitos autorais/imagem) | **implementado** — veto automático |
| Produção/Distribuição/Pagamento (Mercado Pago) | **futuro** — fila termina em GATE HUMANO |
| Comparação previsão simulada × resultado real | **futuro** — depende de vendas reais |

## 4. Regras centrais codificadas (do documento §7)

1. Sem evidência (URL + trecho) não avança → descartada.
2. Validação tem **poder de veto**; justificativa estruturada registrada no grafo.
3. Produção termina em **gate humano** — nada publica automaticamente.
4. Falha ≥2× consecutivas do mesmo agente → pausar e notificar (a implementar
   junto com os agentes reais; anotado).
5. Pagamento só via Mercado Pago Checkout Transparente (futuro).

## 5. Riscos e limites honestos

- Personas simuladas **não substituem** entrevistas/pré-vendas/tráfego/pagamento.
- Evidência interna (confiança 0.3) é fraca por definição — a descoberta externa
  (URL real + trecho verificado) é o próximo incremento.
- O validador rejeita bloqueadores legais mas não dá aconselhamento jurídico.

## 6. Log de decisões

| Data | Decisão | Motivo |
|---|---|---|
| 2026-09-24 | MVP em Python stdlib, sem deps | Zero atrito p/ rodar; deps entram com os serviços reais em venvs separados |
| 2026-09-24 | MatrAIx = stub determinístico hash-based | Trace reproduzível (input+versão = resultado) é pré-requisito da missão; LLM entra depois sem tocar no pipeline |
| 2026-09-24 | Semantica = JSONL append-only + namespaces | Inspecionável/commitável; migra p/ a lib real mantendo a interface registrar/consultar |
| 2026-09-24 | Seed = as 10 ideias do IDeias de projetos.md | Massa de teste real do fluxo; bloqueadores legais declarados nas ideias 1/5/6 |
| 2026-09-24 | Gate humano obrigatório no fim da fila | Princípio 3 do documento; nada publica sozinho |
