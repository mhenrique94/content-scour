# import os
# import base64
from django.conf import settings

# from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_text_splitters import MarkdownTextSplitter
from langchain_core.prompts.prompt import PromptTemplate
from langchain_postgres import PGVector
from langchain_groq import ChatGroq
from langchain.chains.retrieval_qa.base import RetrievalQA

embedding_model_id = 'sentence-transformers/all-MiniLM-L6-v2'
embedding_model_kwargs = {'device': 'cpu'}
embedding_encode_kwargs = {'normalize_embeddings': False}

CONNECTION_STRING = (
    f"postgresql+psycopg://{settings.DB_VECTOR_USER}:{settings.DB_VECTOR_PASSWORD}"
    f"@localhost:{settings.DB_VECTOR_PORT}/postgres?sslmode=allow"
)

COLLECTION_NAME = 'langchain_collection'

IS_LOCAL = settings.LOCAL_LLM
# def process_embedding_from_docs() :
#     text_splitter = MarkdownTextSplitter(chunk_size = 1000, chunk_overlap = 20)

#     files = os.listdir('./docs')

#     for file in files:
#         file_path = f"./docs/{file}"
#         document = Document(page_content=file_path, metadata={"source": file_path})
#         texts = text_splitter.split_documents([document])

#         db = PGVector.from_documents(
#             embedding=hf,
#             documents=texts,
#             collection_name=COLLECTION_NAME,
#             connection=CONNECTION_STRING
#         )

#         return db


# def process_embedding_from_base64(base64_file):
#     file_bytes = base64.b64decode(base64_file)


def similarity_search(query):
    
    chat, retriever = _get_llm(IS_LOCAL)

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


def _get_llm(is_local):
    # collection tem que ter o id do usuário usando, então:
    # - criar sistema de login
    # - criar logica de upload de documentos do user associando doc > user_id

    # para definir o que vai processar
    # - recuperar o collection pertencente ao user da request

    if is_local:
        hf = HuggingFaceEmbeddings(
            model_name=embedding_model_id,
            model_kwargs=embedding_model_kwargs,
            encode_kwargs=embedding_encode_kwargs
        )


        db = PGVector.from_existing_index(hf, collection_name=COLLECTION_NAME, connection=CONNECTION_STRING)
        retriever = db.as_retriever(search_kwargs={'k': 3})
        chat = ChatGroq(
            temperature=0,
            groq_api_key=settings.GROQ_API_KEY,
            model_name=settings.GROQ_API_MODEL
        )
        return chat, retriever
    
    # chat, retriever = process_embedding_from_base64(base64_file)
    # return chat, retriever


