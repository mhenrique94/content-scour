import csv
import json
from django.conf import settings

from django.db import connection
from langchain_core.documents import Document as lc_document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts.prompt import PromptTemplate
from langchain_postgres import PGVector
from langchain_groq import ChatGroq
from langchain_ai21 import AI21Embeddings
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_text_splitters import RecursiveCharacterTextSplitter

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

ai21_embedding = AI21Embeddings(
    api_key=settings.AI21_API_KEY
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
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)
    content_doc = lc_document(page_content=content, metadata={"source": document.file.name})
    split_documents = text_splitter.split_documents([content_doc])
    processed_lc_documents = [
        lc_document(page_content=chunk.page_content, metadata=chunk.metadata) for chunk in split_documents
    ]
    if IS_LOCAL:
        PGVector.from_documents(
            embedding=hf,
            documents=processed_lc_documents,
            collection_name=collection,
            connection=CONNECTION_STRING
        )
    else:
        PGVector.from_documents(
            embedding=ai21_embedding,
            documents=processed_lc_documents,
            collection_name=collection,
            connection=CONNECTION_STRING
        )

    document.processed = True
    document.save()


def delete_user_document(document, user):
    collection = f"{user.id}{user.username}_collection"
    vector_ids = _get_vector_id(document.file.name)
    _, db = _get_llm(IS_LOCAL, collection)

    db.delete(vector_ids, collection_only=True)
    document.delete()

def rag_from_query(query, user):
    collection = f"{user.id}{user.username}_collection"
    chat, db = _get_llm(IS_LOCAL, collection)

    retriever = db.as_retriever(search_kwargs={'k': 3})

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
    chat = ChatGroq(
        temperature=0,
        groq_api_key=settings.GROQ_API_KEY,
        model_name=settings.GROQ_API_MODEL
    )

    if is_local:
        db = PGVector.from_existing_index(hf, collection_name=collection, connection=CONNECTION_STRING)
    else:
        db = PGVector.from_existing_index(ai21_embedding, collection_name=collection, connection=CONNECTION_STRING)
    
    return chat, db


def _get_vector_id(document_name):
    with connection.cursor() as cursor:
        query = """
        SELECT id
        FROM langchain_pg_embedding
        WHERE cmetadata->>'source' = %s
        """
        cursor.execute(query, (document_name,))
        results = cursor.fetchall()

    return [result[0] for result in results] if results else None
