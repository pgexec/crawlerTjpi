from bs4 import BeautifulSoup
from classCrawler import Crawler
import requests

def main():
    try:
        numero_processo = "0000989-95.2017.8.18.0078"
        crawler = Crawler(numero_processo)
        site_consulta = crawler.requisicao_site()
        link_result = crawler.redirecionamento_pag(site_consulta)
        print(link_result)
        site = requests.get(link_result)
        siteCorreto = BeautifulSoup(site.content,'html.parser')
        print(siteCorreto)
    except Exception as e:
        print(f'Erro ao buscar html do site{e}')

if __name__ == "__main__":
    main()