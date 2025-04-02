import requests
import json
import numpy as np
from scipy.stats import pearsonr
from datetime import datetime

# Função para obter dados históricos de uma série
def get_series_data(indicator_code, series_code, token, limit=4000):
    url = f"https://apis.4intelligence.ai/api-feature-store/api/v1/indicators/{indicator_code}/series/{series_code}/observations?limit={limit}"
    headers = {'Authorization': token}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(f"Dados recebidos para {series_code}: {data}")  # Depuração
        observations = data.get('data', [])
        if observations:
            return observations
        else:
            print(f"Nenhuma observação encontrada para a série {series_code}.")
            return None
    else:
        print(f"Erro na requisição para {series_code}. Código de status: {response.status_code}")
        print(f"Resposta completa da API: {response.text}")  # Depuração adicional
        return None

# Função para sincronizar as datas das duas séries
def synchronize_data(data1, data2):
    # Extrai as datas e valores de ambas as séries
    dates1 = {entry['date']: entry['value'] for entry in data1}
    dates2 = {entry['date']: entry['value'] for entry in data2}

    # Encontra as datas comuns entre as duas séries
    common_dates = set(dates1.keys()).intersection(set(dates2.keys()))

    # Sincroniza os dados com base nas datas comuns
    synchronized_data1 = [(date, dates1[date]) for date in common_dates]
    synchronized_data2 = [(date, dates2[date]) for date in common_dates]

    # Ordena os dados por data (opcional, se necessário)
    synchronized_data1.sort(key=lambda x: datetime.strptime(x[0], "%Y-%m-%dT%H:%M:%S"))
    synchronized_data2.sort(key=lambda x: datetime.strptime(x[0], "%Y-%m-%dT%H:%M:%S"))

    return synchronized_data1, synchronized_data2

# Função para calcular a correlação entre duas séries
def calculate_correlation(data1, data2):
    # Verifica se os dados têm o formato esperado
    if not data1 or not data2:
        print("Os dados das séries estão vazios ou mal formatados.")
        return None

    # Extrai os valores das duas séries
    values1 = [entry[1] for entry in data1]
    values2 = [entry[1] for entry in data2]

    # Verifica se as séries têm o mesmo tamanho
    if len(values1) != len(values2):
        print(f"As séries têm tamanhos diferentes: {len(values1)} e {len(values2)}")
        return None

    # Converte para arrays do NumPy para facilitar o cálculo da correlação
    values1 = np.array(values1)
    values2 = np.array(values2)

    # Calcula a correlação de Pearson entre as duas séries
    corr, _ = pearsonr(values1, values2)

    return corr

# Função principal para buscar os dados e calcular a correlação
def main():
    token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjgyX3VOQkNKVENnU0VNX3Z2TjR2LSJ9.eyJodHRwczovLzRpbnRlbGxpZ2VuY2UuY29tLmJyL2VtYWlsIjoicGVkcm8uZ3VpbGhlcm1lQGdlcy5pbmF0ZWwuYnIiLCJodHRwczovLzRpbnRlbGxpZ2VuY2UuY29tLmJyL3VzZXJfbWV0YWRhdGEiOnt9LCJodHRwczovLzRpbnRlbGxpZ2VuY2UuY29tLmJyL2FwcF9tZXRhZGF0YSI6eyJyb2xlcyI6WyJpc0NsYWFTIiwiaXNGYWFTIiwiaXNGZWF0dXJlU3RvcmUiXX0sImh0dHBzOi8vNGludGVsbGlnZW5jZS5jb20uYnIvbmFtZSI6InBlZHJvLmd1aWxoZXJtZUBnZXMuaW5hdGVsLmJyIiwiaXNzIjoiaHR0cHM6Ly80aW50ZWxsaWdlbmNlLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2N2JkYWYwY2NiZGE3YzJkZDM1YTc4ZGMiLCJhdWQiOlsiNGNhc3RodWIiLCJodHRwczovLzRpbnRlbGxpZ2VuY2UuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTc0MzUzODA1MSwiZXhwIjoxNzQ2MTMwMDUxLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiYXpwIjoibVNLWnFINUtxMVdvY3hKY2xuSVVSYlZJS1VXUmpvSnoiLCJwZXJtaXNzaW9ucyI6WyJhc2s6cXVlc3Rpb25zIiwiY3JlYXRlOnByb2plY3QtY2xhYXMiLCJjcmVhdGU6cHJvamVjdHMiLCJjcmVhdGU6d29ya3NwYWNlcyIsImVkaXQ6Z3JvdXAtYWxlcnRzIiwiZWRpdDpteS1ncm91cHMiLCJyZWFkOmFjY2Vzcy1ncm91cHMiLCJyZWFkOmNsaWVudHMiLCJyZWFkOmRvbWFpbnMiLCJyZWFkOmdyb3VwLWFsZXJ0cyIsInJlYWQ6aW5kaWNhdG9ycyIsInJlYWQ6bXktZ3JvdXBzIiwicmVhZDpvYnNlcnZhdGlvbnMiLCJyZWFkOnByZWRlZmluZWQtZ3JvdXBzIiwicmVhZDpwcm9qZWN0LWNsYWFzIiwicmVhZDpwcm9qZWN0aW9ucyIsInJlYWQ6cHJvamVjdHMiLCJyZWFkOnNlcmllcyIsInJlYWQ6dXNlcnMiLCJyZWFkOndvcmtzcGFjZXMiXX0.nmBYpRjgv2WrbexOc1SwimdvkKZ9oK6_QsjgQqdPcXgETcRArf53mEG86Lk2cVFzjoOKOiMeQwty3d4ejUrMlTjYteHxQmS75CXUCfVA3He_35EM5gQeeUxPPTiq6DHRtuoQqUhoP6sJtVVXDjx5XtpBEhNCpyCDJANBfWudOkad9JfOuCXf_Vx4n9tJKwmlkedPj9_6IM3toTXlfByKzrBcyJoMj_3ouESaE6tw7_ijgeespd4_fmSCwxeKqje-xA1q0TRM9buS7mQRZTk_RlWkOLYO6eL1pZMnJ1qy-049RQMocRGQVmRrgZy8veoFMY1stHUFfPYzMwjC7d6J9g'

    # Defina os códigos dos indicadores e das séries que você deseja usar
    indicator_code = "BRPRC0046"  # Exemplo de código de indicador
    series_code_1 = "BRPRC0046000OOML"  # Código da primeira série
    series_code_2 = "BRPRC0046000OOMM"  # Código da segunda série

    # Obtemos os dados históricos das duas séries
    data1 = get_series_data(indicator_code, series_code_1, token)
    data2 = get_series_data(indicator_code, series_code_2, token)

    if data1 and data2:
        # Sincroniza as datas e os valores das duas séries
        synchronized_data1, synchronized_data2 = synchronize_data(data1, data2)

        # Calculando a correlação entre as duas séries
        correlation = calculate_correlation(synchronized_data1, synchronized_data2)
        if correlation is not None:
            print(f"A correlação entre as séries {series_code_1} e {series_code_2} é: {correlation:.4f}")
        else:
            print("Não foi possível calcular a correlação.")
    else:
        print("Erro ao obter os dados para as séries fornecidas.")

if __name__ == "__main__":
    main()