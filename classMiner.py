import re

url_base = 'https://pje.tjpi.jus.br/'
# Conteúdo HTML de exemplo
html_content = '''
<a href="javascript:void();" title="Ver Detalhes" class="btn btn-default btn-sm" onclick="openPopUp('Consulta pública','/1g/ConsultaPublica/DetalheProcessoConsultaPublica/listView.seam?ca=fcc12a4f2e8dbc17cda2a75fc573a7474628d90d202db7c7')">
<i class="fa fa-external-link"></i> <span class="sr-only">Ver detalhes do processo</span></a>
'''

# Regex para capturar apenas o conteúdo começando com '/1' dentro das aspas simples
#pattern1 = r"openPopUp\('.*?','(/1.*?)'\)"

# Usando re.search para encontrar o padrão
#match = re.search(pattern1, html_content)

# Extraindo o valor
#if match:
 #   url_extraced = match.group(1)  # Captura o grupo com o caminho
  #  print("URL específica extraída:", url_extraced)
#else:
   # print("Padrão não encontrado.")
