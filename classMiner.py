import json
from email.encoders import encode_noop


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

    def extrair_dados_processo(self):
        all_col_sm =  self.site.findAll('div', attrs={'class':'col-sm-12'})
        info1 = all_col_sm[2]
        numero_processo = all_col_sm[2].text.strip()
        data_distribuicao = all_col_sm[3].text.strip()
        classe_judicial = all_col_sm[4].text.strip()
        assunto = all_col_sm[5].text.strip()

        all_value_sm = self.site.findAll('div', attrs={'class': 'value col-sm-12'})
        jurisdicao = all_value_sm[4].text.strip()
        orgao_julgador = all_value_sm[6].text.strip()
        print('------------------------------------')
        print("numero do processo: "+numero_processo)
        print('------------------------------------')
        print("data de distribuição: "+data_distribuicao)
        print('------------------------------------')
        print("classe judicial: "+classe_judicial)
        print('------------------------------------')
        print("assunto: "+assunto)
        print('------------------------------------')
        print("jurisdicao: "+jurisdicao)
        print('------------------------------------')
        print("Orgão julgador: " + orgao_julgador)