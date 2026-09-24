# Planilha Conta-Tudo (Anti-Preguiça)

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
