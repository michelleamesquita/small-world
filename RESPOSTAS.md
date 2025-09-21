# Relatório – Small-World (Watts–Strogatz)

Este relatório apresenta o resultado do experimento de pequeno-mundo. A figura abaixo mostra as grandezas normalizadas em função de `p`:

- L/L(0): comprimento médio de caminho característico normalizado
- C/C(0): coeficiente médio de aglomeração normalizado

![WS: L/L0 e C/C0 vs p](./out/ws_LC_vs_p.png)

## Observações
- Para `p` muito pequeno (regime quase-lattice), o coeficiente de aglomeração permanece próximo de 1 enquanto o comprimento de caminho ainda é alto.
- À medida que `p` cresce (inserção de poucos atalhos), L cai rapidamente enquanto C diminui lentamente: janela de pequeno-mundo.
- Em `p` próximo de 1 (regime quase-aleatório), L se aproxima do mínimo e C é baixo, como em grafos aleatórios com mesmo grau médio.

## Dados
Os dados usados para o gráfico são salvos em `./out/ws_results.csv` com as colunas:
`p, L, C, L_over_L0, C_over_C0`.
