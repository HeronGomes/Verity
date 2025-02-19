# Teste Verity

### Sobre

Teste para posição de **Engenheiro de I.A.**
Projeto desenvolvido a critério de teste durante a segunda fase de seleção da empresa Verity.

### Objetivos

***Principal***
- Analisar padrões e técnicas de desenvolvimento.

***Secundário***
- Desenvolver uma API que execute modelos de i.a generativa, capaz de responder ao usuário em linguagem natural, questões sobre informações de uma banco de dados de compras/vendas fictício.

- Deve-se utlizar o recurso de *LangGraph*, para gerir o pipeline do processo de comunicação homem/máquina, fim-a-fim.

### Requisitos

- Python 3.10.x
- Windows 11 x64
- Processador 5Ghz+
- 16 GB RAM+
- 6 GB VRAM+
- Hdd 20 GB+

### Instalação
Para instalação dos pacotes necessários, execute (dentro do diretório do projeto):

```pip install -r requirements.txt```

Deve-se baixar e instalar o [OLLAMA](https://ollama.com/)

Após iniciar o serviço, dois modelos deverão ser carregados:

- mistral e sqlcoder

Da seguinte forma:

Uma vez no terminal do S.O execute:

```ollama pull mistral``` e depois ``` ollama pull sqlcoder ```

### Execução

A depender do S.O escolhido, deve-se executar os arquivo:

- start_server.bat para windows (homologado)
- start_server.sh para unix/like (vide caracterísricas da distribuição)

Para uma execução com python, apenas rode o arquivo run.py:
``` python run.py ```

### Limitações

- Por comodidade optou-se por não utilizar recursos de memória ou persistência de contexto durante 
as interações do usuário com o chat.
- Devido a limitação de RAM do host, optou-se por carregar modelos menores (e menos inteligentes) para a execução da tarefa, mas, nada impede a mudança para qualquer outro modelo que seja compativel (*vide documentação do modelo sobre compatibilidade com tools*).
- Não há implementação de ***guardrails*** ou recursos que garantam a boa interação do usuário com o chat ou mesmo o processo contrário.
- Erros de SQL e alucinações em querys complexas são esperados.