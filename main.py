from classCrawler import Crawler
from classMiner import Miner


def main():
    numero_processo = "0000989-95.2017.8.18.0078"  # Exemplo de número de processo

    try:

        crawler = Crawler(numero_processo)
        site_base = crawler.requisicao_site_base()
        if not site_base:
            print("Erro ao fazer a requisição ao site base.")
            return

        link_montado = crawler.montar_link(site_base)
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

        # Executa a extração de informações com o Miner
        miner.montagem_dados_processo()
        miner.extrair_polo_ativo()
        miner.extrair_polo_passivo()
        miner.extrair_movimentacoes_processo()
        miner.extrair_url_documentos_juntados()

    except Exception as e:
        print(f"Erro durante a execução: {e}")


if __name__ == "__main__":
    main()
