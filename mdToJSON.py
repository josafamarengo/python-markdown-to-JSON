import markdown
import json
import requests

# Define o link do arquivo Markdown
url_arquivo = 'https://raw.githubusercontent.com/Ebazhanov/linkedin-skill-assessments-quizzes/main/html/html-quiz.md'

# Faz uma requisição HTTP para obter o conteúdo do arquivo
conteudo_arquivo = requests.get(url_arquivo).text

# Converte o conteúdo do arquivo de Markdown para HTML
conteudo_html = markdown.markdown(conteudo_arquivo)

# Seleciona apenas o conteúdo da tag <h2>
titulo = conteudo_html.split('<h2>')[1].split('</h2>')[0]

# Seleciona apenas o conteúdo das tags <h4>
questions = conteudo_html.split('<h4>')[1:]
questions = [q.replace('</h4>', '') for q in questions]

# Separa as questões das alternativas armazenando-as em um dicionário
for i, q in enumerate(questions):
    question = q.split('<ul>')[0]
    alternatives = q.split('<li>')[1:]
    alternatives = [a.replace('</li>', '') for a in alternatives]
    is_correct = [True if '[x]' in a else False for a in alternatives]
    alternatives = [a.replace('[x]', '') for a in alternatives]
    alternatives = [a.replace('[ ]', '') for a in alternatives]
    alternatives = [{'alternative': a, 'is_correct': c} for a, c in zip(alternatives, is_correct)]
    questions[i] = {
        'question': question,
        'alternatives': alternatives
    }

# Cria um dicionário para armazenar as questões
conteudo_json = {
    'title': titulo,
    'questions': questions
}

nome_arquivo = titulo + '.json'
with open(nome_arquivo, 'w') as f:
    json.dump(conteudo_json, f)