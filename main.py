import requests
import json

token = 'GH_SECRET'
#List of indicators
url = "https://apis.4intelligence.ai/api-feature-store/api/v1/indicators?limit=4000"

response = requests.get(url, headers={'Authorization': token})

if (response.status_code==200):
    print(response.json())

    data = []

    data.append(response.json())

    with open("indicators.json", "w") as file:  # "w" will create myjson.json if it doesn't exist, otherwise rewrite the whole file
        json.dump(data, file, indent=4)  # dump all the data into the json file with 4 space indentation


#List of series from an indicator
url_series = f"https://apis.4intelligence.ai/api-feature-store/api/v1/indicators/BRPRC0046/series?limit=4000"

response_series = requests.get(url_series, headers={'Authorization':token})


if (response.status_code==200):
    print(response_series.json())


#Get serie by code - metadata from time-series
url_serie_by_code = "https://apis.4intelligence.ai/api-feature-store/api/v1/series/BRPRC0046000OOML"

response_serie_by_code = requests.get(url_serie_by_code, headers={'Authorization': token})


if (response.status_code==200):
    print(response_serie_by_code.json())


#o limit muda de acordo com time-series, por isso é importante ou estipular um valor bem alto, ou mudar a variável de acordo com a time-serie correspondente


#Historical data from a time-series
url_historical = "https://apis.4intelligence.ai/api-feature-store/api/v1/indicators/BRPRC0046/series/BRPRC0046000OOML/observations?limit=4000"

response_historical = requests.get(url_historical, headers={'Authorization':token})

if (response.status_code==200):
    print(response_historical.json())


#Projection of a time-series
url_projection = "https://apis.4intelligence.ai/api-feature-store/api/v1/indicators/BRPRC0046/series/BRPRC0046000OOML/projections?limit=4000"


if (response.status_code==200):
    response_projection = requests.get(url_projection, headers={'Authorization':token})

    print(response_projection.json())