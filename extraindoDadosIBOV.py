import requests
from datetime import datetime, timedelta

API_KEY = 'SUA_CHAVE_ALPHA_VANTAGE'  # Insira aqui sua chave real
symbol_acao = input("Digite o código da ação (ex: PETR4.SA): ").upper()
symbol_ibov = 'BOVA11.SA'  # ETF que replica o IBOVESPA

def obter_serie_alpha(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}&outputsize=compact'
    response = requests.get(url)
    dados = response.json()
    try:
        serie = dados['Time Series (Daily)']
        return serie
    except KeyError:
        print(f"Erro ao buscar dados de {symbol}")
        return {}

def calcular_rentabilidade_30d(serie):
    datas = sorted(serie.keys(), reverse=True)
    if len(datas) < 22:
        return None
    preco_inicio = float(serie[datas[21]]['4. close'])  # Aproximadamente 30 dias úteis atrás
    preco_final = float(serie[datas[0]]['4. close'])
    return (preco_final / preco_inicio - 1) * 100

def buscar_ipca():
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json"
    r = requests.get(url)
    try:
        valor = float(r.json()[0]['valor'])
        return valor
    except:
        return None

def buscar_cdi():
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados/ultimos/21?formato=json"
    r = requests.get(url)
    try:
        valores = [float(d['valor']) for d in r.json()]
        acumulado = 1
        for v in valores:
            acumulado *= (1 + v / 100)
        return (acumulado - 1) * 100
    except:
        return None

def calcular_poupanca():
    return ((1 + 0.005) ** 1 - 1) * 100  # 0,5% ao mês

# Dados da ação
serie_acao = obter_serie_alpha(symbol_acao)
rent_acao = calcular_rentabilidade_30d(serie_acao)

# Dados do IBOV via BOVA11
serie_ibov = obter_serie_alpha(symbol_ibov)
rent_ibov = calcular_rentabilidade_30d(serie_ibov)

# Indicadores financeiros
rent_ipca = buscar_ipca()
rent_cdi = buscar_cdi()
rent_poup = calcular_poupanca()

print("\n Rentabilidade nos últimos 30 dias:\n")
if rent_acao is not None:
    print(f"Ação {symbol_acao}: {rent_acao:.2f}%")
else:
    print(f"Ação {symbol_acao}: erro ao calcular")

if rent_ibov is not None:
    print(f"IBOVESPA (via BOVA11): {rent_ibov:.2f}%")
else:
    print("IBOVESPA: erro ao calcular")

if rent_cdi is not None:
    print(f"CDI estimado: {rent_cdi:.2f}%")
else:
    print("CDI estimado: dados indisponíveis")

print(f"Poupança estimada: {rent_poup:.2f}%")

if rent_ipca is not None:
    print(f"IPCA estimado: {rent_ipca:.2f}%")
else:
    print("IPCA estimado: dados indisponíveis")


# Classificação simples
def avaliar(rent, benchmark):
    if rent is None or benchmark is None:
        return "Dados insuficientes"
    diff = rent - benchmark
    if diff > 2:
        return "ACIMA do mercado"
    elif diff < -2:
        return "ABAIXO do mercado"
    else:
        return "EM LINHA com o mercado"

print(f"\n Avaliação da ação {symbol_acao}:")
print(f"- Em relação ao IBOVESPA: {avaliar(rent_acao, rent_ibov)}")
print(f"- Em relação ao CDI: {avaliar(rent_acao, rent_cdi)}")
print(f"- Em relação à Inflação: {avaliar(rent_acao, rent_ipca)}")
