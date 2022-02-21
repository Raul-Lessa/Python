import requests
import json

def request(cep):
    url = "https://viacep.com.br/ws/%s/json/" % (cep)
    try:
      return requests.get(url)
    except Exception as e:
      return requests.get(url).status_code

cep = "12227630"
try:
   result = request(cep).json()
   print("%s, %s, %s - %s" % (result["logradouro"],result["bairro"],result["localidade"],result["uf"]))
except Exception as e:
   print("Error: ")

