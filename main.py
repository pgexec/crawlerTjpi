from classCrawler import Crawler

def main():
    numero_processo = "0000989-95.2017.8.18.0078"
    crawler = Crawler(numero_processo)
    site = crawler.requisicao_site()
    site_result = crawler.redirecionamento_pag(site)
    print(site_result)

if __name__ == "__main__":
    main()