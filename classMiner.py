import json
import re


class Miner:
    def __init__(self, site,schema_json_path):
        self.site = site
        self.dados_processo = {}
        try:
            with open(schema_json_path,"r",encoding="utf-8") as schema_file:
                self.json_schema = json.load(schema_file)
        except Exception as e:
            self.json_schema = None
            print(f"Erro ao carregar o JSON Schema:{e}")



    def montagem_dados_processo(self):
        all_col_sm =  self.site.findAll('div', attrs={'class':'col-sm-12'})
        self.dados_processo["Numero_processo"] = re.sub(r'\s+', ' ',  all_col_sm[2].text).strip()
        self.dados_processo["Data_distribuicao"] =  re.sub(r'\s+', ' ',  all_col_sm[3].text).strip()
        self.dados_processo["Classe_judicial"] =  re.sub(r'\s+', ' ',  all_col_sm[4].text).strip()
        self.dados_processo["Assunto"] = re.sub(r'\s+', ' ',  all_col_sm[5].text).strip()
        all_value_sm = self.site.findAll('div', attrs={'class': 'value col-sm-12'})
        self.dados_processo["Jurisdicao"] = re.sub(r'\s+', ' ', all_value_sm[4].text).strip()
        self.dados_processo["Orgao_julgador"] = re.sub(r'\s+', ' ', all_value_sm[6].text).strip()

    def extrair_polo_ativo(self):
        polo_ativo = []
        tbody = self.site.find('tbody', attrs={"id": "j_id140:processoPartesPoloAtivoResumidoList:tb"})
        if tbody is not None:
            linhas = tbody.find_all('tr')
            for linha in linhas:
                colunas = linha.find_all('td')
                if len(colunas) == 2:
                    # Limpa os textos das colunas
                    participantes = re.sub(r'\s+', ' ', colunas[0].text).strip()
                    situacao = re.sub(r'\s+', ' ', colunas[1].text).strip()

                    if not participantes:
                        participantes = "Não informado"
                    if not situacao:
                        situacao = "Não informado"

                    polo_ativo.append({
                        "Movimento": participantes,
                        "Documento": situacao
                    })

            self.dados_processo["polo_ativo"] = polo_ativo

    def extrair_polo_passivo(self):
            polo_passivo = []
            tbody = self.site.find('tbody', attrs={"id": "j_id140:processoPartesPoloPassivoResumidoList:tb"})

            if tbody is not None:
                linhas = tbody.find_all('tr')
                for linha in linhas:
                    colunas = linha.find_all('td')
                    if len(colunas) == 2:
                        participantes = re.sub(r'\s+', ' ', colunas[0].text).strip()
                        situacao = re.sub(r'\s+', ' ', colunas[1].text).strip()

                        if not participantes:
                            participantes = "Não informado"
                        if not situacao:
                            situacao = "Não informado"

                        polo_passivo.append({
                            "participantes": participantes,
                            "situacao": situacao
                        })
                self.dados_processo["polo_passivo"] = polo_passivo

    def extrair_movimentacoes_processo(self):
        movimentacoes_processo = []
        tbody = self.site.find('tbody', attrs={"id":   "j_id140:processoEvento:tb"})

        if tbody is not None:
            linhas = tbody.find_all('tr')
            for linha in linhas:
                colunas = linha.find_all('td')
                if len(colunas) == 2:
                    movimento = re.sub(r'\s+', ' ', colunas[0].text).strip()
                    documento = re.sub(r'\s+', ' ', colunas[1].text).strip()

                    if not movimento:
                        participantes = "Não informado"
                    if not documento:
                        situacao = "Não informado"

                    movimentacoes_processo.append({
                        "Movimento": movimento,
                        "Documento": documento
                    })
            self.dados_processo["movimentações_do_processo"] = movimentacoes_processo

    def extrair_documentos_juntados(self,id):


        pattern = r"openPopUp\('[^']*',\s*'([^']*)'"
        elemento = self.site.find('a', attrs={'id':id})

        if elemento and elemento.has_attr('onclick'):
            onclick_value = elemento['onclick']


            match = re.search(pattern, onclick_value)
            if match:
                url = match.group(1)
                print("URL extraído:", url)
                return url
            else:
                value_href = elemento['href']
        else:
            print("Elemento ou atributo 'onclick' não encontrado.")

