
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime


class Crawler:

    def __init__(self,numero_processo):
        self.view_state = ""
        self.data_atual = datetime.now().strftime("%m/%Y")
        self.session = requests.Session()
        self.numero_processo = numero_processo
        self.url_consulta = "https://pje.tjpi.jus.br/1g/ConsultaPublica/listView.seam"
        self.url_base = "https://pje.tjpi.jus.br"


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
            res = self.session.get(self.url_consulta,headers=self.headers)
            if res.status_code ==200:
                soup = BeautifulSoup(res.content,"html.parser")
                view_state_tag = soup.find('input',attrs={'id':'javax.faces.ViewState'}).get('value')
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
            res = self.session.post(self.url_consulta,headers=self.headers,data=self.data)
            if res.status_code == 200:
                html = BeautifulSoup(res.content,'html.parser')
                return html.prettify()
            else:
                print(f'Erro na requisição POST:{res.status_code}')
        except Exception as e:
            print(f'Erro ao fazer a requisição POST:{e}')

    def montar_link(self,html):
        pattern = r"openPopUp\('.*?','(/1.*?)'\)"
        match = re.search(pattern,html)
        if match:
            url_extraced = match.group(1)
            print("url construida:" + url_extraced)
            return self.url_base + url_extraced
        else:
            print("URL de redirecionamento não encontrada!")
        return None

    def requisicao_detalhes_processo(self,link_montado):
        try:
            res = requests.get(link_montado)
            html = BeautifulSoup(res.content, 'html.parser')
            return html
        except Exception as e:
            print(f"Erro ao fazer Requisição do site com os{e}")