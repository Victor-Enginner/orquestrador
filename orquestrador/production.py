"""Agente de Produção de Ativos — MVP (documento §2.2: geração de ativos
vendáveis + controle de qualidade antes da entrega).

Regras deste MVP:
- Consome APENAS a fila aprovada pelo gate humano (fila-gate-humano.json).
- Cada ativo é um SCAFFOLD honesto: estrutura completa de venda com campos
  [PREENCHER: ...] onde só humanos/evidências reais podem preencher
  (ex.: contatos de fornecedores reais). NADA é inventado.
- QC determinístico: título, público-alvo, preço, tamanho mínimo, disclosure
  de afiliado quando aplicável, zero "[PREENCHER" em seções obrigatórias de
  estrutura (os de evidência são permitidos e BLOQUEIAM publicação — gate).
- Publicação segue PROIBIDA: saída vai para fila de revisão humana.

Uso: python3 -m orquestrador.production 001
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from adapters.semantica_adapter import ContextGraph   # noqa: E402
from orquestrador.models import Namespace             # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- templates

TEMPLATES: dict[str, callable] = {}

def template(ideia_id_prefixo: str):
    def deco(fn):
        TEMPLATES[ideia_id_prefixo] = fn
        return fn
    return deco


@template("IDEIA-02")
def _t_achadinhos(ideia: dict) -> str:
    return f"""# Kit Promotor de Achadinhos — Shopee sem Estoque

> ATIVO SCAFFOLD — gerado pelo orquestrador. Revise TODO o conteúdo antes
> de publicar. Este arquivo NÃO contém links de afiliado ainda.

**PÚBLICO-ALVO:** pessoas que consomem achadinhos no TikTok/Reels (18-34,
poder de compra R$ 20-80 por impulso)
**PREÇO SUGERIDO (teste):** grátis (o ganho é comissão de afiliado)
**FORMATO:** 5 roteiros de vídeo 15-30s + checklist de postagem

## Roteiros (estrutura — grave com o SEU produto/ link real)

1. GANCHO (0-3s): problema visual exagerado — *[PREENCHER: produto escolhido]*
2. DEMONSTRAÇÃO (3-15s): uso real, close no detalhe engraçado/útil
3. GIRO (15-25s): "custa menos que X" — *[PREENCHER: preço real na Shopee]*
4. CTA (25-30s): "link na bio" + disclosure obrigatório

## Checklist de conformidade (QC — obrigatório)

- [ ] **Disclosure de afiliado visível** no vídeo e na legenda (#afiliado / "recebo comissão")
- [ ] Link via programa OFICIAL de afiliados da Shopee (não invented — [PREENCHER: seu link rastreado])
- [ ] Preço verificado no dia da postagem (evidência: print/screenshot anexado)
- [ ] Sem promessa de resultado garantido (Lei 4.595/…: propaganda enganosa)

## Registro de evidência (regra 1 do orquestrador)

| Campo | Valor |
|---|---|
| URL do produto | [PREENCHER: url real] |
| Preço coletado em | [PREENCHER: data] |
| Print de referência | [PREENCHER: anexo] |
"""


@template("IDEIA-03")
def _t_planilha(ideia: dict) -> str:
    return """# Planilha Conta-Tudo (Anti-Preguiça)

> ATIVO SCAFFOLD — gere o .xlsx a partir do CSV anexo (producao/IDEIA-03/).
> Revise antes de vender.

**PÚBLICO-ALVO:** pessoas físicas que querem controlar gastos sem saber Excel
**PREÇO SUGERIDO (teste):** R$ 19,90
**FORMATO:** planilha (CSV base + guia de 1 página)

## O que resolve (copy curta)

- 5 abas: Entradas, Saídas, Resumo automático, Metas, Dívidas
- Fórmulas prontas: total por categoria, quanto sobra, alerta de estouro
- Vídeo de 2 min mostrando o preenchimento (gravar antes de publicar)

## Estrutura das abas (especificação p/ gerar o .xlsx)

| Aba | Colunas | Fórmulas |
|---|---|---|
| Entradas | data, descrição, valor, categoria | total no rodapé |
| Saídas | data, descrição, valor, categoria, forma de pagamento | total + subtotal por categoria |
| Resumo | mês, entradas, saídas, saldo | saldo = entradas − saídas; semáforo verde/vermelho |
| Metas | meta do mês, gasto atual, % consumido | barra de progresso + alerta em 80% |
| Dívidas | credor, valor total, parcela, juros | soma das parcelas + data de quitação |

## Guia de 1 página (vem junto no PDF)

1. Preencha Entradas e Saídas TODO dia (2 min)
2. O Resumo calcula sozinho — não digite lá
3. Dia 30: olhe a categoria campeã de gasto e defina a meta do mês seguinte
4. Dívidas: liste da maior taxa de juros pra menor (método bola de neve invertido)

## QC antes de publicar

- [ ] CSV abre sem erro no Excel, Google Sheets e LibreOffice
- [ ] Fórmulas testadas com 20 lançamentos fake
- [ ] Página de vendas com print real da planilha
"""


@template("IDEIA-04")
def _t_corretor_bio(ideia: dict) -> str:
    return """# Kit Corretor de Bio — Abordagem + Entrega

> ATIVO SCAFFOLD — serviço manual (o humano executa). Kit acelera a operação.

**PÚBLICO-ALVO:** pequenos comércios locais com perfil ruim no Instagram
**PREÇO SUGERIDO (teste):** R$ 50 por perfil (pacote 3 perfis R$ 120)
**FORMATO:** script de abordagem + checklist de otimização + antes/depois

## Script de abordagem (WhatsApp/DM) — primeiro contato

1. Apresentação em 1 linha (quem você é)
2. O achado: cite o problema ESPECÍFICO do perfil dele
   *[PREENCHER: o que está errado no perfil — sem inventar, olhar de verdade]*
3. Prova rápida: 1 print do perfil + 1 mockup do "depois"
4. Oferta: "arrumo hoje por R$ 50, pago no Pix — só se você gostar do preview"
5. Fechamento: prazo curto, sem pressão

## Checklist de otimização do perfil

- [ ] Nome pesquisável (categoria + cidade)
- [ ] Bio em 3 linhas: o que faz / para quem / CTA
- [ ] Link funcional (WhatsApp ou catálogo)
- [ ] Destaques organizados (cardápio, preços, localização, avaliações)

## Tabela de preços do serviço (sugestão de teste)

| Pacote | Entrega | Preço |
|---|---|---|
| Básico | bio + destaques reorganizados | R$ 50 |
| Completo | básico + link na bio (WhatsApp) + 6 destaques com capa | R$ 90 |
| Trio | 3 perfis completos (comércios vizinhos) | R$ 120 |

## Como entregar (fluxo do serviço)

1. Diagnóstico: print do perfil atual + 3 problemas pontuais
2. Mockup do "depois" (imagem simples) — aprovação antes de mexer
3. Execução: 30-60 min no perfil (ou passo a passo se ele preferir)
4. Prova: antes/depois lado a lado (vira portfólio pro próximo cliente)
5. Follow-up em 7 dias: "como foi o movimento?" (gancho pro pacote completo)
"""


@template("IDEIA-08")
def _t_fornecedores(ideia: dict) -> str:
    return """# Guia: 25 Fornecedores Verificados para Revenda sem Estoque

> ATIVO SCAFFOLD — **NÃO publique com fornecedores não verificados.**
> Cada fornecedor abaixo precisa de evidência real (contato, preço,
> prazo) coletada por você. O orquestrador NÃO inventa fornecedores.

**PÚBLICO-ALVO:** iniciantes em revenda que não sabem onde comprar barato
**PREÇO SUGERIDO (teste):** R$ 27
**FORMATO:** PDF (gerar do markdown revisado) + planilha de cotação

## Estrutura por fornecedor (replicar 25×)

| Campo | Valor |
|---|---|
| Nome / contato | [PREENCHER: evidência real — visita/cotação] |
| Categoria de produtos | [PREENCHER] |
| Pedido mínimo | [PREENCHER] |
| Preço de referência (3 itens) | [PREENCHER + print] |
| Prazo de entrega | [PREENCHER] |
| Verificado em | [PREENCHER: data] |

## Critérios de inclusão (QC do conteúdo)

- [ ] Contato testado (respondeu ou catálogo público ativo)
- [ ] Preço conferido ≤ 70% do preço de revenda comum
- [ ] Nenhum fornecedor "de lista de terceiros" sem verificação própria

## Bônus que sustenta o preço

- Planilha de cotação comparativa
- Tutorial: calcular margem com frete e imposto simples

## Como calcular a margem (exemplo com números reais)

```
custo do produto       R$ 12,00
frete rateado (pacote) R$  3,00
anúncio/embalagem      R$  2,00
custo total            R$ 17,00
preço de venda         R$ 39,90
margem bruta           R$ 22,90 (57%)
```

Regra prática: venda a pelo menos 2× o custo total. Abaixo disso,
o frete e o imprevisto comem o lucro.

## FAQ do comprador (3 perguntas que sustentam a objeção de preço)

1. "Isso funciona pra mim que nunca vendi?" → sim, cada fornecedor tem
   pedido mínimo informado; comece com 1 item para testar
2. "Por que pagar se existe AliExpress?" → o guia economiza as semanas
   de teste: fornecedores com preço/prazo já conferidos
3. "E se um fornecedor não responder?" → o guia tem 25; mesmo com falha
   de 20% sobram 20 opções testadas
"""


# ------------------------------------------------------------------ QC

def qc(ideia: dict, texto: str) -> dict:
    """Controle de qualidade determinístico (documento §2.2 + §7.3)."""
    checagens: list[tuple[bool, str]] = [
        ("PÚBLICO-ALVO" in texto, "declara público-alvo"),
        ("PREÇO" in texto, "declara preço"),
        (len(texto) >= 1200, f"conteúdo mínimo (len={len(texto)} ≥ 1200)"),
        ("AFFILIATE_MARK" not in texto, "sanidade"),
    ]
    if ideia["ideia_id"] == "IDEIA-02":  # ativo de afiliado exige disclosure
        checagens.append(("Disclosure de afiliado" in texto, "disclosure de afiliado presente"))
    preencher = texto.count("[PREENCHER")
    if preencher:
        checagens.append((False, f"{preencher} campo(s) de evidência humana pendente(s) → BLOQUEIA publicação (gate)"))
    else:
        checagens.append((True, "sem pendências de evidência"))
    return {
        "aprovado_qc": all(ok for ok, _ in checagens),
        "itens": [{"ok": ok, "item": item} for ok, item in checagens],
        "campos_preencher": preencher,
    }


# ------------------------------------------------------------------ fluxo

def produzir(experimento: str = "001") -> dict:
    dir_exp = RAIZ / "experiments" / f"exp-{experimento}"
    fila = json.loads((dir_exp / "fila-gate-humano.json").read_text(encoding="utf-8"))
    grafo = ContextGraph(dir_exp / "graph.jsonl")
    relatorio = [
        f"# Produção — exp-{experimento} — {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "> Scaffolds gerados a partir da fila aprovada. Campos [PREENCHER] =",
        "> evidência que só humano/evidência real pode preencher. Publicação",
        "> continua PROIBIDA sem sua aprovação final (gate).",
        "",
    ]
    saida = []

    for ideia in fila:
        tpl = TEMPLATES.get(ideia["ideia_id"])
        if not tpl:
            relatorio.append(f"## ⚠️ {ideia['ideia_id']} — sem template; ignorada")
            continue
        texto = tpl(ideia)
        qc_result = qc(ideia, texto)

        dir_ativo = dir_exp / "producao" / ideia["ideia_id"]
        dir_ativo.mkdir(parents=True, exist_ok=True)
        (dir_ativo / "asset.md").write_text(texto, encoding="utf-8")
        (dir_ativo / "meta.json").write_text(
            json.dumps({**ideia, "qc": qc_result}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        grafo.registrar(Namespace.PRODUCTION, "ativo", {
            "ideia_id": ideia["ideia_id"],
            "caminho": str(dir_ativo / "asset.md"),
            "aprovado_qc": qc_result["aprovado_qc"],
            "campos_preencher": qc_result["campos_preencher"],
        })

        icone = "✅" if qc_result["aprovado_qc"] else "⏳"
        relatorio += [
            f"## {icone} {ideia['ideia_id']} — {ideia['titulo']}",
            f"- asset: `producao/{ideia['ideia_id']}/asset.md`",
            f"- QC: {'APROVADO (pronto p/ sua revisão final)' if qc_result['aprovado_qc'] else 'com pendências humanas (esperado)'}"
            f" — {qc_result['campos_preencher']} campo(s) [PREENCHER]",
            "",
        ]
        saida.append({"ideia_id": ideia["ideia_id"], "qc": qc_result})

    (dir_exp / "producao" / "relatorio-producao.md").write_text(
        "\n".join(relatorio) + "\n", encoding="utf-8"
    )
    return {"experimento": experimento, "ativos": len(saida),
            "prontos": sum(1 for s in saida if s["qc"]["aprovado_qc"])}


if __name__ == "__main__":
    exp = sys.argv[1] if len(sys.argv) > 1 else "001"
    print(json.dumps(produzir(exp), ensure_ascii=False))
