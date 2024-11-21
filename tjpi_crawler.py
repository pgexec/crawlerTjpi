import requests
from bs4 import BeautifulSoup
import re

url = 'https://pje.tjpi.jus.br/1g/ConsultaPublica/DetalheProcessoConsultaPublica/listView.seam?'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Cookie": "MO=P; JSESSIONID=2FQz_X8UYjBWHloh6ZT7owY9XRHDKKQSiNHuVXUx.pje-legacy-57596c467f-m95zs; X-Oracle-BMC-LBS-Route=61b9e84409b90154f1e6a7faa036c404491b61cf27da03a11a2ff120e313e9b656c62fd8a7c42ae85fb583106f287d235bcee33acab551b4a5ce0751; OAuth_Token_Request_State=94eaeb9c-6840-4e3c-8548-665ad9a005df",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "Sec-CH-UA": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Host": "pje.tjpi.jus.br"
}

params = {
    'ca':'ca=fcc12a4f2e8dbc175ca9878197c8d4404628d90d202db7c7'
}

def fazer_requisicao(ulr,headers,params):
    try:
        response  = requests.get(url,headers=headers,params=params)
        if response.status_code == 200:
            print("Página acessada com sucesso")
            soup = BeautifulSoup(response.content,"html.parser")
            return soup
        else:
            print(f"Erro ao acessar a página: {response.status_code}")
            exit()
    except Exception as e:
        print(f"Ocorreu um erro ao fazer a requisição{e}")
        exit()

site = fazer_requisicao(url,headers,params)
print(site)
teste = site.find('div',attrs={'id':'j_id140:processoTrfViewView:j_id146'})
print(teste)