import csv
from django.conf import settings

from langchain_core.documents import Document as lc_document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts.prompt import PromptTemplate
from langchain_postgres import PGVector
from langchain_groq import ChatGroq
from langchain.chains.retrieval_qa.base import RetrievalQA

embedding_model_id = 'sentence-transformers/all-MiniLM-L6-v2'
embedding_model_kwargs = {'device': 'cpu'}
embedding_encode_kwargs = {'normalize_embeddings': False}

CONNECTION_STRING = (
    f"postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}?sslmode=allow"
)
COLLECTION_NAME = 'langchain_collection'
IS_LOCAL = settings.LOCAL_LLM

hf = HuggingFaceEmbeddings(
            model_name=embedding_model_id,
            model_kwargs=embedding_model_kwargs,
            encode_kwargs=embedding_encode_kwargs
        )

def process_user_document(document, user):
    file = document.file.file
    collection = f"{user.id}{user.username}_collection"
    if document.file_type == ".csv":
        data = csv.DictReader(file)
        content = ""
        for line in data:
          content += f"{line}\n"
    else:
        content = file.read().decode('utf-8')
    
    processed_lc_document = lc_document(page_content=content, metadata={"source": document.file.name})

    if IS_LOCAL:
        PGVector.from_documents(
            embedding=hf,
            documents=[processed_lc_document],
            collection_name=collection,
            connection=CONNECTION_STRING
        )
    else:
        # logica da ai21 vai aqui, lembrando que o vetor tem um campo no model Document
        print("não implementado")

    document.processed = True
    document.save()


def similarity_search(query, user):
    collection = f"{user.id}{user.username}_collection"
    chat, retriever = _get_llm(IS_LOCAL, collection)

    prompt = set_custom_prompt()

    qa = RetrievalQA.from_chain_type(llm=chat,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )

    response = qa.invoke({"query": query})
    
    return response


def set_custom_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """

    template = """Use the following pieces of information to answer the user's question.\n
    If you don't know the answer, just say that you don't know, don't try to make up an answer.\n\n
    Context: {context}\n
    Question: {question}\n\n
    Only return the helpful answer below and nothing else.
    """

    prompt = PromptTemplate(template=template,
                            input_variables=['context', 'question'])
    return prompt


def _get_llm(is_local, collection):
    if is_local:
        db = PGVector.from_existing_index(hf, collection_name=collection, connection=CONNECTION_STRING)
        retriever = db.as_retriever(search_kwargs={'k': 3})
        chat = ChatGroq(
            temperature=0,
            groq_api_key=settings.GROQ_API_KEY,
            model_name=settings.GROQ_API_MODEL
        )
        return chat, retriever
    
    # chat, retriever = process_embedding_from_base64(base64_file)
    # return chat, retriever


