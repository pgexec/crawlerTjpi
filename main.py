import json

from classCrawler import Crawler
from classMiner import Miner


def main():
    numero_processo = "0000989-95.2017.8.18.0078"  # Exemplo de número de processo


    try:

        crawler = Crawler(numero_processo)
        html_base = crawler.requisicao_site_base()
        if not html_base:
            print("Erro ao fazer a requisição ao site base.")
            return

        link_montado = crawler.montar_link(html_base)
        print(link_montado)

        if not link_montado:
            print("Erro ao montar o link para os detalhes do processo.")
            return

        site_detalhes = crawler.requisicao_detalhes_processo(link_montado)
        if not site_detalhes:
            print("Erro ao obter os detalhes do processo.")
            return
        resultados = crawler.requisicao_paginas(8)
        if not resultados:
            print("Nenhum dado encontrado durante a navegação entre páginas.")
        else:
            print(f"Dados coletados: {resultados}")

        miner = Miner(site_detalhes, "json_schemaPiaui.json")
        tabela_montada = miner.extrair_url_documentos(resultados)
        print(json.dumps(tabela_montada, indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"Erro durante a execução: {e}")


if __name__ == "__main__":
    main()
