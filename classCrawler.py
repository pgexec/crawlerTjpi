
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
        self.url_base = "https://pje.tjpi.jus.br/1g/ConsultaPublica/listView.seam"
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
        self.cookies = {
            "JSESSIONID": "JRrjxinpNdlQe5kML2xCUhjtRh34SBMSLG-AvvjM.pje-legacy-5f6cb998f-t4qqv",
            "X-Oracle-BMC-LBS-Route": "c92502913b1209f16af1a070630afe0312dbad2527da03a11a2ff120e313e9b656c62fd8a7c42ae85a1a70987ee9032f63ac4a97fe1f3207b4dd368b",
            "MO": "P",
            "OAuth_Token_Request_State": "61d36dd7-d72c-4d0a-aa2d-a9b6e9b5d3bc",
            "_ga": "GA1.1.1346687483.1732403223",
            "_ga_NREPKDGLND": "GS1.1.1732403223.1.1.1732403238.45.0.0",
            "_ga_Y465HJSLNG": "GS1.1.1732403223.1.1.1732403238.45.0.0",
        }

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



    def get_viewstate(self):
        try:
            res = requests.get(self.url_base,headers=self.headers,cookies=self.cookies)
            if res.status_code ==200:
                soup = BeautifulSoup(res.content,"html.parser")
                view_state = soup.find('input',attrs={'id':'javax.faces.ViewState'}).get('value')
                self.view_state = view_state
                print('view_state localizado com sucesso!')
            else:
                print(f'Erro ao acessar a página:{res.status_code}')
        except Exception as e:
            print(f"Erro ao capturar o ViewState:{e}")

    def requisicao_site(self):

        try:
            res = self.session.post(self.url_base,headers=self.headers,data=self.data,cookies=self.cookies)
            if res.status_code == 200:
                html = BeautifulSoup(res.content,'html.parser')
                return html.prettify()
            else:
                print(f'Erro na requisição POST:{res.status_code}')
        except Exception as e:
            print(f'Erro ao fazer a requisição POST:{e}')

    def redirecionamento_pag(self,html):

        pattern = r"openPopUp\('.*?','(/1.*?)'\)"
        match = re.search(pattern,html)
        if match:
            url_extraced = match.group(1)
            return self.url_base + url_extraced