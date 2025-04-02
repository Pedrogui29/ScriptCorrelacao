import requests
import json

token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjgyX3VOQkNKVENnU0VNX3Z2TjR2LSJ9.eyJodHRwczovLzRpbnRlbGxpZ2VuY2UuY29tLmJyL2VtYWlsIjoicGVkcm8uZ3VpbGhlcm1lQGdlcy5pbmF0ZWwuYnIiLCJodHRwczovLzRpbnRlbGxpZ2VuY2UuY29tLmJyL3VzZXJfbWV0YWRhdGEiOnt9LCJodHRwczovLzRpbnRlbGxpZ2VuY2UuY29tLmJyL2FwcF9tZXRhZGF0YSI6eyJyb2xlcyI6WyJpc0NsYWFTIiwiaXNGYWFTIiwiaXNGZWF0dXJlU3RvcmUiXX0sImh0dHBzOi8vNGludGVsbGlnZW5jZS5jb20uYnIvbmFtZSI6InBlZHJvLmd1aWxoZXJtZUBnZXMuaW5hdGVsLmJyIiwiaXNzIjoiaHR0cHM6Ly80aW50ZWxsaWdlbmNlLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2N2JkYWYwY2NiZGE3YzJkZDM1YTc4ZGMiLCJhdWQiOlsiNGNhc3RodWIiLCJodHRwczovLzRpbnRlbGxpZ2VuY2UuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTc0MzUzODA1MSwiZXhwIjoxNzQ2MTMwMDUxLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiYXpwIjoibVNLWnFINUtxMVdvY3hKY2xuSVVSYlZJS1VXUmpvSnoiLCJwZXJtaXNzaW9ucyI6WyJhc2s6cXVlc3Rpb25zIiwiY3JlYXRlOnByb2plY3QtY2xhYXMiLCJjcmVhdGU6cHJvamVjdHMiLCJjcmVhdGU6d29ya3NwYWNlcyIsImVkaXQ6Z3JvdXAtYWxlcnRzIiwiZWRpdDpteS1ncm91cHMiLCJyZWFkOmFjY2Vzcy1ncm91cHMiLCJyZWFkOmNsaWVudHMiLCJyZWFkOmRvbWFpbnMiLCJyZWFkOmdyb3VwLWFsZXJ0cyIsInJlYWQ6aW5kaWNhdG9ycyIsInJlYWQ6bXktZ3JvdXBzIiwicmVhZDpvYnNlcnZhdGlvbnMiLCJyZWFkOnByZWRlZmluZWQtZ3JvdXBzIiwicmVhZDpwcm9qZWN0LWNsYWFzIiwicmVhZDpwcm9qZWN0aW9ucyIsInJlYWQ6cHJvamVjdHMiLCJyZWFkOnNlcmllcyIsInJlYWQ6dXNlcnMiLCJyZWFkOndvcmtzcGFjZXMiXX0.nmBYpRjgv2WrbexOc1SwimdvkKZ9oK6_QsjgQqdPcXgETcRArf53mEG86Lk2cVFzjoOKOiMeQwty3d4ejUrMlTjYteHxQmS75CXUCfVA3He_35EM5gQeeUxPPTiq6DHRtuoQqUhoP6sJtVVXDjx5XtpBEhNCpyCDJANBfWudOkad9JfOuCXf_Vx4n9tJKwmlkedPj9_6IM3toTXlfByKzrBcyJoMj_3ouESaE6tw7_ijgeespd4_fmSCwxeKqje-xA1q0TRM9buS7mQRZTk_RlWkOLYO6eL1pZMnJ1qy-049RQMocRGQVmRrgZy8veoFMY1stHUFfPYzMwjC7d6J9g'

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