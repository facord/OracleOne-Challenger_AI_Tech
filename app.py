import os
from pathlib import Path
import streamlit as st

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.tools import tool

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Agente RAG - Documentos", page_icon="🤖")
st.title("🤖 Agente RAG - Consulta de Documentos")

# --- VERIFICAÇÃO DA API KEY ---
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("Chave GROQ_API_KEY não configurada!")
    st.stop()

# --- CARREGAMENTO DO VECTOR STORE (Com Cache para performance) ---
@st.cache_resource(show_spinner="Carregando e indexando documentos...")
def inicializar_vector_store():
    documentos_dir = Path("documentos")
    
    # Loaders e Chunking
    loader = DirectoryLoader(str(documentos_dir), glob="*.pdf", loader_cls=PyPDFLoader)
    pages = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(pages)
    
    # Embeddings e Chroma
    embed_model = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-small")
    
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embed_model,
        persist_directory="./chroma_db",
        collection_name="documentos_desafio"
    )
    return vector_store

vector_store = inicializar_vector_store()
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# --- CONFIGURAÇÃO DO AGENTE ---
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

@tool
def pega_contexto(query: str) -> str:
    """Busca nos cinco PDFs os trechos mais relevantes para responder à pergunta."""
    docs = retriever.invoke(query)
    if not docs:
        return "Nenhum trecho relevante foi encontrado nos documentos."
    
    resultados = []
    for doc in docs:
        fonte = Path(doc.metadata.get("source", "arquivo desconhecido")).name
        pagina = doc.metadata.get("page")
        resultados.append(f"Fonte: {fonte}\nPágina: {pagina}\nConteúdo:\n{doc.page_content}")
    return "\n\n---\n\n".join(resultados)

system_prompt = """
Você é um assistente de perguntas e respostas sobre os documentos disponibilizados.
Regras:
1. Use a ferramenta de busca para encontrar informações nos documentos antes de responder.
2. Responda somente com informações presentes nos documentos.
3. Não use conhecimento externo para completar lacunas.
4. Se a informação não estiver nos documentos recuperados, responda: "Não sei a resposta com base nos documentos."
5. Responda de forma clara e objetiva.
"""

agente_pdf = create_agent(model=llm, tools=[pega_contexto], system_prompt=system_prompt)

# --- INTERFACE DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do usuário
if prompt := st.chat_input("Faça uma pergunta sobre os documentos..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            resposta = agente_pdf.invoke({"messages": [("user", prompt)]})
            conteudo = resposta["messages"][-1].content
            st.markdown(conteudo)
    
    st.session_state.messages.append({"role": "assistant", "content": conteudo})