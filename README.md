# 🤖 Agente RAG - Challenge ALURA ORACLE (Pegasus)

Um assistente inteligente baseado em **RAG (Retrieval-Augmented Generation)** desenvolvido para consultar e responder dúvidas com precisão sobre a documentação técnica e operacional do projeto.

---

## 📸 Demonstração da Aplicação

> *Interface desenvolvida em Streamlit para interação em tempo real com o assistente RAG.* <br>
> Link para testes: https://oracleone-challengeraitech-fabianacordeiro.streamlit.app/

---

## 🎯 Objetivo do Projeto

O objetivo deste projeto é resolver a fragmentação de conhecimento técnico, permitindo que desenvolvedores e membros da equipe consultem guias, manuais e arquiteturas internas de forma rápida, contextualizada e com rastreabilidade de fontes (nome do arquivo e página).

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.11
- **Framework de Orquestração IA:** LangChain
- **Modelo de Linguagem (LLM):** Llama 3.3 70B (via Groq API)
- **Embeddings:** `intfloat/multilingual-e5-small` (HuggingFace)
- **Vector Store:** ChromaDB (Persistente)
- **Interface Web:** Streamlit
- **Containerização:** Docker & Docker Compose
- **Deploy:** Streamlit Community Cloud

---

## 📑 Documentos Indexados

O assistente foi treinado e indexado para consultar 5 documentos base localizados no diretório `documentos/`:

1. `Arquitetura_de_Microsservicos_Mapa_de_Dominios.pdf`
2. `Guia_Oficial_de_Engenharia_Backend.pdf`
3. `Guia_Oficial_de_Engenharia_Frontend.pdf`
4. `Manual_de_Onboarding_para_Desenvolvedores.pdf`
5. `Manual_Maestro_de_Resiliencia_Resposta_a_Incidentes.pdf`

---

## ⚙️ Arquitetura e Fluxo do RAG

```text
5 PDFs (Documentos) 
   └─► Chunking (RecursiveCharacterTextSplitter - 800 chars / 100 overlap)
        └─► Embeddings (multilingual-e5-small)
             └─► Vector Store (ChromaDB Persistente)
                  └─► Tool de Busca (`pega_contexto`)
                       └─► Agente LangChain (LLM: Llama 3.3 70B Versatile)
                            └─► Resposta Precisa com Citação de Fonte/Página
```

---

## 📁 Estrutura do Repositório

```text
.
├── app.py              # Aplicação principal Streamlit com a interface de chat
├── agente_rag.ipynb    # Notebook Jupyter com experimentos e prototipação
├── documentos/         # Pasta contendo os PDFs indexados pela base de conhecimento
│   ├── Arquitetura_de_Microsservicos_Mapa_de_Dominios.pdf
│   ├── Guia_Oficial_de_Engenharia_Backend.pdf
│   ├── Guia_Oficial_de_Engenharia_Frontend.pdf
│   ├── Manual_de_Onboarding_para_Desenvolvedores.pdf
│   └── Manual_Maestro_de_Resiliencia_Resposta_a_Incidentes.pdf
├── Dockerfile          # Arquivo para build e execução da imagem Docker
├── requirements.txt    # Lista de dependências Python
└── README.md           # Documentação do projeto
```

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
- **Python 3.10+** ou **Docker** instalado.
- Chave de API da **Groq** ([Obtenha sua chave aqui](https://console.groq.com/)).

### Opção 1: Execução com Python

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
   cd SEU_REPOSITORIO
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv .venv
   # No Windows:
   .venv\Scripts\activate
   # No Linux/Mac:
   source .venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Defina a variável de ambiente:**
   - **Windows (CMD):** `set GROQ_API_KEY="sua_chave_aqui"`
   - **Windows (PowerShell):** `$env:GROQ_API_KEY="sua_chave_aqui"`
   - **Linux/Mac:** `export GROQ_API_KEY="sua_chave_aqui"`

5. **Execute o Streamlit:**
   ```bash
   streamlit run app.py
   ```

---

### Opção 2: Execução via Docker

1. **Faça o build da imagem Docker:**
   ```bash
   docker build -t rag-agent-chroma .
   ```

2. **Execute o container passando a API Key:**
   ```bash
   docker run -p 8501:8501 -e GROQ_API_KEY="sua_chave_aqui" rag-agent-chroma
   ```

3. Acesse `http://localhost:8501` no navegador.

---

## 🌐 Deploy no Streamlit Cloud

Para realizar o deploy na nuvem do Streamlit:
1. Suba o projeto para o GitHub.
2. Acesse [share.streamlit.io](https://share.streamlit.io).
3. Conecte o repositório, defina o arquivo principal como `app.py`.
4. Em **Advanced Settings > Secrets**, adicione sua chave de API:
   ```toml
   GROQ_API_KEY = "gsk_sua_chave_aqui"
   ```

---

## 🌐 Exemplos de interação com o chat
 ```toml
PERGUNTA: Como fazer commits pequenos e descritivos?
RESPOSTA: Para fazer commits pequenos e descritivos, você deve seguir o padrão Conventional Commits. Isso significa que cada commit deve
ter uma mensagem que descreva a alteração realizada, utilizando um formato específico: `tipo(escopo): descrição curta`. Os tipos de
commits incluem `feat` para novas funcionalidades, `fix` para correções de bugs, `chore` para manutenção de build ou dependências,
e `docs` para mudanças na documentação. Além disso, é importante manter os commits pequenos, focando em uma alteração de cada vez, e
utilizar branches para organizar o seu trabalho, como criar uma branch de feature para desenvolver uma nova funcionalidade. Lembre-se de
atualizar sua branch develop local, criar sua branch de feature, desenvolver e fazer commits pequenos e descritivos, e subir sua branch
para o repositório remoto.

================================================================================

PERGUNTA: Como funciona a arquitetura de microsserviços?
RESPOSTA: A arquitetura de microsserviços funciona da seguinte forma:

*   Cada microsserviço é responsável por um domínio específico de negócio e é projetado para ser escalável de forma independente.
*   Os microsserviços se comunicam entre si por meio de APIs ou mensagens, permitindo que cada serviço seja desenvolvido, testado e implantado de forma autônoma.
*   A arquitetura de microsserviços permite que as equipes de desenvolvimento tenham autonomia completa sobre o ciclo de vida do software, desde o código até o deploy em produção.
*   A escalabilidade independente dos microsserviços permite que os recursos sejam alocados de forma mais eficiente, reduzindo os custos operativos e melhorando a eficiência do sistema.
*   A arquitetura de microsserviços também permite que as equipes de desenvolvimento trabalhem de forma mais ágil e flexível, pois cada serviço pode ser desenvolvido e implantado de forma independente.

Essas são as principais características da arquitetura de microsserviços, que permitem que os sistemas sejam mais escaláveis, flexíveis e eficientes.

================================================================================
   ```

---

## 🛡️ Regras e Guardrails do Agente

- O agente consulta estritamente o conteúdo dos PDFs através do ChromaDB.
- Se a informação não estiver presente na base documental, ele responde claramente: *"Não sei a resposta com base nos documentos."*
- Evita alucinações e não usa conhecimento prévio/externo para completar lacunas.
