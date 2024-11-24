from bs4 import BeautifulSoup
from classCrawler import Crawler
from classMiner import Miner
import requests

def main():
    try:
        numero_processo = "0000989-95.2017.8.18.0078"
        crawler = Crawler(numero_processo)
        site_base = crawler.requisicao_site_base()
        if site_base is not None:
            link_montado = crawler.montar_link(site_base)
            if link_montado is not None:
                site_detalhes = crawler.requisicao_detalhes_processo(link_montado)
                miner = Miner(site_detalhes,"json_schemaPiaui.json")
                miner.extrair_dados_processo()
        else:
            print('Erro ao fazer Requisição ao site base!')



    except Exception as e:
        print(f'Erro ao buscar html do site{e}')

if __name__ == "__main__":
    main()