
import re
from functools import total_ordering

import requests
from bs4 import BeautifulSoup
from datetime import datetime


class Crawler:

    def __init__(self, numero_processo):
        self.view_state = ""
        self.data_atual = datetime.now().strftime("%m/%Y")
        self.session = requests.Session()
        self.numero_processo = numero_processo
        self.url_consulta = "https://pje.tjpi.jus.br/1g/ConsultaPublica/listView.seam"
        self.url_base = "https://pje.tjpi.jus.br"
        self.url_post = "https://pje.tjpi.jus.br/1g/ConsultaPublica/DetalheProcessoConsultaPublica/listView.seam"

        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7",
            "connection": "keep-alive",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://pje.tjpi.jus.br",
            "referer": "https://pje.tjpi.jus.br/1g/ConsultaPublica/listView.seam",
            "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        }
        self.get_cookies()
        self.get_viewstate()

        self.data = {
            "AJAXREQUEST": "_viewRoot",
            "fPP:numProcesso-inputNumeroProcessoDecoration:numProcesso-inputNumeroProcesso": self.numero_processo,
            "mascaraProcessoReferenciaRadio": "on",
            "fPP:j_id156:processoReferenciaInput": "",
            "fPP:dnp:nomeParte": "",
            "fPP:j_id174:nomeAdv": "",
            "fPP:j_id183:classeJudicial": "",
            "fPP:j_id183:sgbClasseJudicial_selection": "",
            "tipoMascaraDocumento": "on",
            "fPP:dpDec:documentoParte": "",
            "fPP:Decoration:numeroOAB": "",
            "fPP:Decoration:j_id217": "",
            "fPP:Decoration:estadoComboOAB": "org.jboss.seam.ui.NoSelectionConverter.noSelectionValue",
            "fPP:dataAutuacaoDecoration:dataAutuacaoInicioInputDate": "",
            "fPP:dataAutuacaoDecoration:dataAutuacaoInicioInputCurrentDate": self.data_atual,
            "fPP:dataAutuacaoDecoration:dataAutuacaoFimInputDate": "",
            "fPP:dataAutuacaoDecoration:dataAutuacaoFimInputCurrentDate": self.data_atual,
            "fPP": "fPP",
            "autoScroll": "",
            "javax.faces.ViewState": self.view_state,  # Capturado dinamicamente
            "fPP:j_id238": "fPP:j_id238",
            "AJAX:EVENTS_COUNT": "1",
        }

    def get_cookies(self):
        try:
            # Faz a requisição inicial para capturar cookies
            response = self.session.get(self.url_consulta, headers=self.headers)
            if response.status_code == 200:
                print("Cookies Capturados:", self.session.cookies.get_dict())
            else:
                print(f"Erro ao capturar cookies: {response.status_code}")
        except Exception as e:
            print(f"Erro ao capturar cookies: {e}")

    def get_viewstate(self):
        try:
            res = self.session.get(self.url_consulta, headers=self.headers)
            if res.status_code == 200:
                soup = BeautifulSoup(res.content, "html.parser")
                view_state_tag = soup.find('input', attrs={'id': 'javax.faces.ViewState'}).get('value')
                if view_state_tag:
                    self.view_state = view_state_tag
                    print('view_state localizado com sucesso!')
                else:
                    print('Erro: ViewState não encontrado na página.')
            else:
                print(f'Erro ao acessar a página:{res.status_code}')
        except Exception as e:
            print(f"Erro ao capturar o ViewState:{e}")

    def requisicao_site_base(self):

        try:
            res = self.session.post(self.url_consulta, headers=self.headers, data=self.data)
            if res.status_code == 200:
                html = BeautifulSoup(res.content, 'html.parser')
                return html.prettify()
            else:
                print(f'Erro na requisição POST:{res.status_code}')
        except Exception as e:
            print(f'Erro ao fazer a requisição POST:{e}')



    def montar_link(self, html):
        pattern = r"openPopUp\('.*?','(/1.*?)'\)"
        match = re.search(pattern, html)
        if match:
            url_extraced = match.group(1)
            return self.url_base + url_extraced
        else:
            print("URL de redirecionamento não encontrada!")
        return None




    def requisicao_detalhes_processo(self, link_montado):
        try:
            res = requests.get(link_montado)
            html = BeautifulSoup(res.content, 'html.parser')
            return html
        except Exception as e:
            print(f"Erro ao fazer Requisição do site com os{e}")




    def requisicao_paginas(self, total_paginas):

        resultados = []

        for pagina in range(1, total_paginas + 1):
            print(f"Requisitando página {pagina}...")

            # Atualiza o número da página no payload
            payload = {
                "AJAXREQUEST": "j_id140:j_id464",
                "j_id140:j_id545:j_id546": str(pagina),
                "j_id140:j_id545": "j_id140:j_id545",
                "autoScroll": "",
                "javax.faces.ViewState": self.view_state,  # ViewState fixo
                "j_id140:j_id545:j_id547": "j_id140:j_id545:j_id547",
                "AJAX:EVENTS_COUNT": "1",
            }

            headers = {
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7",
                "connection": "keep-alive",
                "content-length": str(len(payload)),
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "cookie": "JSESSIONID=kN70Wv771oUoMQniB8ZiRIvka-TbcsfI4lz2eVYe.pje-legacy-8458d97cb8-rnfwj; X-Oracle-BMC-LBS-Route=84eb1219f25c7f0846913922b75a6937098eb18827da03a11a2ff120e313e9b656c62fd8a7c42ae83c9ff8270e88ee4455bb083221babffb8335dd2c; _ga=GA1.1.1346687483.1732403223; _ga_NREPKDGLND=GS1.1.1732403223.1.1.1732403238.45.0.0; _ga_Y465HJSLNG=GS1.1.1732403223.1.1.1732403238.45.0.0",
                "host": "pje.tjpi.jus.br",
                "origin": "https://pje.tjpi.jus.br",
                "referer": "https://pje.tjpi.jus.br/1g/ConsultaPublica/DetalheProcessoConsultaPublica/listView.seam?ca=fcc12a4f2e8dbc1733d36839d40509854628d90d202db7c7",
                "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            }

            try:
                # Faz a requisição POST
                response = self.session.post(self.url_post, headers=headers, data=payload)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")

                    # Localiza a tabela com os dados
                    tbody = soup.find("tbody", {"id": "j_id140:processoEvento:tb"})
                    if tbody:
                        linhas = tbody.find_all("tr")
                        for linha in linhas:
                            colunas = linha.find_all("td")
                            if colunas:
                                movimento = colunas[0].text.strip()
                                documento = colunas[1].text.strip() if len(colunas) > 1 else None
                                resultados.append({"movimento": movimento, "documento": documento})
                    else:
                        print(f"Nenhum dado encontrado na página {pagina}.")
                else:
                    print(f"Erro ao acessar a página {pagina}: {response.status_code}")

            except Exception as e:
                print(f"Erro ao processar a página {pagina}: {e}")

        if not resultados:
            print("Nenhum dado encontrado durante a navegação entre páginas.")
        return resultados






