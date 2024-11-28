import json
import re
from bs4 import BeautifulSoup

class Miner:
    def __init__(self, site, schema_json_path):
        self.site_base = "https://pje.tjpi.jus.br"
        self.site = site
        self.dados_processo = {}
        try:
            with open(schema_json_path, "r", encoding="utf-8") as schema_file:
                self.json_schema = json.load(schema_file)
        except Exception as e:
            self.json_schema = None
            print(f"Erro ao carregar o JSON Schema: {e}")

    def montagem_dados_processo(self):

        try:
            all_col_sm = self.site.find_all('div', attrs={'class': 'col-sm-12'})
            if len(all_col_sm) >= 6:
                self.dados_processo["Numero_processo"] = re.sub(r'\s+', ' ', all_col_sm[2].text).strip()
                self.dados_processo["Data_distribuicao"] = re.sub(r'\s+', ' ', all_col_sm[3].text).strip()
                self.dados_processo["Classe_judicial"] = re.sub(r'\s+', ' ', all_col_sm[4].text).strip()
                self.dados_processo["Assunto"] = re.sub(r'\s+', ' ', all_col_sm[5].text).strip()
            else:
                print('Elementos insuficientes encontrados em col-sm-12')

            all_value_sm = self.site.find_all('div', attrs={'class': 'value col-sm-12'})
            if len(all_value_sm) >= 7:
                self.dados_processo["Jurisdicao"] = re.sub(r'\s+', ' ', all_value_sm[4].text).strip()
                self.dados_processo["Orgao_julgador"] = re.sub(r'\s+', ' ', all_value_sm[6].text).strip()
            else:
                print('Elementos insuficientes encontrados em value.col-sm-12')

            self.extrair_polo_ativo()
            self.extrair_polo_passivo()
            self.extrair_movimentacoes_processo()

        except Exception as e:
            print(f'Erro ao salvar dados recebidos: {e}')


    def extrair_tabela(self, tbody_id):

        dados = []
        try:
            tbody = self.site.find('tbody', attrs={"id": tbody_id})
            if tbody:
                linhas = tbody.find_all('tr')
                for linha in linhas:
                    colunas = linha.find_all('td')
                    if len(colunas) == 2:
                        participantes = re.sub(r'\s+', ' ', colunas[0].text).strip() or "Não informado"
                        situacao = re.sub(r'\s+', ' ', colunas[1].text).strip() or "Não informado"
                        dados.append({"participantes": participantes, "situacao": situacao})
            return dados
        except Exception as e:
            print(f'Erro ao extrair dados da tabela: {e}')

    def extrair_polo_ativo(self):
        self.dados_processo["polo_ativo"] = self.extrair_tabela("j_id140:processoPartesPoloAtivoResumidoList:tb")

    def extrair_polo_passivo(self):
        self.dados_processo["polo_passivo"] = self.extrair_tabela("j_id140:processoPartesPoloPassivoResumidoList:tb")

    def extrair_movimentacoes_processo(self):
        self.dados_processo["movimentacoes_do_processo"] = self.extrair_tabela("j_id140:processoEvento:tb")

    def extrair_link_doc(self, id):
        pattern = r"openPopUp\('[^']*',\s*'([^']*)'"
        try:
            elemento = self.site.find('a', attrs={'id': id})

            if elemento and elemento.has_attr('onclick'):
                onclick_value = elemento['onclick']
                match = re.search(pattern, onclick_value)
                if match:
                    url = self.site_base + match.group(1)
                    return url
            elif elemento and elemento.has_attr('href'):
                return elemento['href']
            else:
                print("Elemento ou atributo 'onclick' não encontrado.")
            return None
        except Exception as e:
            print(f'Erro ao extrair links dos documentos juntados {e}')

    def extrair_url_documentos_juntados(self):
        try:
            documentos_juntados = []

            tbody = self.site.find('tbody', attrs={"id": "j_id140:processoDocumentoGridTab:tb"})
            if tbody:
                linhas = tbody.find_all('tr')
                for linha in linhas:
                    colunas = linha.find_all('td')
                    if len(colunas) == 2:
                        documento = {}

                        # Coluna Esquerda (Documento)
                        link_documento = colunas[0].find('a')
                        if link_documento and link_documento.has_attr('id'):
                            id_link_documento = link_documento['id']
                            url_documento = self.extrair_link_doc(id_link_documento)
                            if url_documento:
                                documento['documento'] = url_documento

                        # Coluna Direita (Certidão)
                        link_coluna_direita = colunas[1].find('a')
                        if link_coluna_direita and link_coluna_direita.has_attr('id'):
                            id_link_direito = link_coluna_direita['id']
                            url_direita = self.extrair_link_doc(id_link_direito)
                            if url_direita:
                                documento['certidao'] = url_direita
                        if documento:
                            documentos_juntados.append(documento)
            self.dados_processo['documentos_juntados'] = documentos_juntados

        except Exception as e:
            print(f"Erro ao extrair URLs de documentos juntados: {e}")
