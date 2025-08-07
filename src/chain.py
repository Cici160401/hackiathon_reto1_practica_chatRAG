from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings

from src.config import OPENAI_API_KEY, CHROMA_PERSIST

#  Arranca el vectorstore (RAG)
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vectordb   = Chroma(
    embedding_function=embeddings,
    persist_directory=CHROMA_PERSIST,
    collection_name="licitaciones"
)
retriever = vectordb.as_retriever(search_kwargs={"k": 4})

# Definimos el LLM
llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=OPENAI_API_KEY, temperature=0.2)

# Creamos la memoria de conversación
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    # guardamos el campo 'answer'
    output_key="answer"           
)

# Construimos el chain
conv_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=False  #para ver de dónde viene la info
)
