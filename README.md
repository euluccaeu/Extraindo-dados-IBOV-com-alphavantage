# Extraindo-de-dados-IBOV-com-alphavantage

Este projeto em Python compara a rentabilidade de uma ação da B3 com indicadores de referência do mercado brasileiro nos últimos 30 dias. Ele utiliza APIs públicas e gratuitas para fornecer uma análise simplificada e acessível da performance de um ativo em relação ao:

- IBOVESPA (via ETF BOVA11);
- CDI (via Banco Central);
- IPCA (inflação, via Banco Central); e
- Poupança (estimada).

Funcionalidades e vantagens:
- Consulta diária de ações com Alpha Vantage
- Comparação com benchmarks econômicos reais
- Classificação da ação: acima, abaixo ou em linha com o mercado
- Saída em terminal de fácil leitura

Tecnologias utilizadas
- Python 3
- Biblioteca requests (requisições HTTP)
- APIs do Banco Central e Alpha Vantage

Exemplos de uso
Digite o ticker da ação (ex: PETR4.SA) e receber uma análise de performance comparativa com o mercado brasileiro (IBOVESPA) nos últimos 30 dias úteis.


