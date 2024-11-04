# Importando Bibliotecas
import requests # biblioteca utilizada para fazer requisições HTTP e se comunicar com os sites
from bs4 import BeautifulSoup # biblioteca utilizada para extrair e manipular dados de HTML e XML
import pandas as pd # biblioteca utilizada para manipulação dos dados
import re # biblioteca usada para trabalhar com expressões regulares

# URL a ser coleta as informações
url = 'https://jucemg.mg.gov.br/pagina/140/leiloeiros-ordem-alfabetica'

# modificando o User-Agent para simular um acesso humano, a fim de evitar bloqueio pelo site
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Enviar requisição GET para o site
response = requests.get(url, headers=headers)

# Analisa o conteúdo HTML da resposta e cria uma estrutura navegável
soup = BeautifulSoup(response.text, 'html.parser')

# Encontrar o conteúdo dentro da tag 'article'
html = soup.find('article')

# Lista de siglas de estados
lista_siglas = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 
                'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 
                'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 
                'SP', 'TO']

# Inicializando listas para armazenar os dados
nomes = []
matriculas = []
estados = []
telefones = []
emails = []

# percorre cada tag 'p' contendo as informações de cada leiloeiro
for leiloeiro in html.find_all('p'):
    # Separar leiloeiros se houver mais de um (identificado por uma nova linha ou outro critério)
    leiloeiros_info = leiloeiro.text.split('\n\n')  # Separar por quebras de linha

    for info in leiloeiros_info:
       
        # Extrair o nome do leiloeiro
        nome = info.split('\n')[0].strip()
        nomes.append(nome)

        # Extrair a matrícula
        matricula_info = info.find("Matrícula:")
        if matricula_info != -1:
            matricula = info[matricula_info:].split(':')[1].strip().split('\r')[0]
            matriculas.append(matricula)
        else:
            matriculas.append(None)

        # Extrair o estado
        endereco_info = info.find("Prepost")
        if endereco_info != -1:
            endereco = info[endereco_info:].split('\n')[1].split('\r')[0]
        
        for sigla in lista_siglas:
        
            if re.search(rf"[\s\-]{sigla}(?:[\s\-]|$)", endereco):
                sigla,
                None
        estados.append(sigla)

        # Extrair os telefones
        telefone_info = info.find("Telefone")
        if telefone_info != -1:
            telefone = info[telefone_info:].split(':')[-1].split('\n')[0].strip().replace(' / ', ', ')
            telefones.append(telefone)
        else:
            telefones.append(None)
        
        # Extrair os e-mails
        email_links = re.findall(r'[\w\.-]+@[\w\.-]+', info)
        email = ', '.join(email_links) if email_links else None
        emails.append(email)

# Criar um DataFrame com os dados extraídos
df = pd.DataFrame({
    'Nome': nomes,
    'Matrícula': matriculas,
    'Estado': estados,
    'telefone' : telefones,
    'Email' : emails
})

# Armazena os dados em um arquivo Excel
df.to_excel('./Dados/Leiloeiros_MG.xlsx', index=False)




