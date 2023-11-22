import os
import logging
from huggingface_hub import hf_hub_download
import pinecone
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains.question_answering import load_qa_chain

def init():
    """
    Initialize the document search and question answering components.

    This function sets up the necessary components, including document loading,
    text splitting, embeddings, Pinecone index, LlamaCpp language model, and
    question answering chain.

    Returns:
        None
    """
    global docsearch, chain

    # Document Loading
    loader = PyPDFLoader("assets/files/Constitution.pdf")
    data = loader.load()
    
    # Text Splitting
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=150)
    text = text_splitter.split_documents(data)

    # Environment Variables
    os.environ["CUDA_VISIBLE_DEVICE"] = "0"
    PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
    PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV', 'gcp-starter')

    # Embeddings
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    # Pinecone Index
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)
    index = pinecone.Index('llamaprac')

    # Callback Manager
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    # Language Model Initialization
    model_name_or_path = "TheBloke/Llama-2-7b-Chat-GGUF"
    model_basename = "llama-2-7b-chat.Q5_0.gguf"
    model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)

    ngpu = 40
    n_batch = 256
    n_ctx = 1024
    llm = LlamaCpp(
        model_path=model_path,
        max_tokens=256,
        n_gpu_layers=ngpu,
        n_batch=n_batch,
        callback_manager=callback_manager,
        n_ctx=n_ctx,
    )

    # Question Answering Chain
    chain = load_qa_chain(llm, chain_type="stuff")

    # Pinecone Document Search Index
    docsearch = Pinecone.from_texts([t.page_content for t in text], embeddings, index_name='llamaprac')

    logging.info("Init complete")


def run(query):
    """
    Execute a question answering query.

    Args:
        query (str): The user's question.

    Returns:
        str: The response to the user's question.
    """
    logging.info("model 1: request received")
    docs = docsearch.similarity_search(query)
    response = chain.run(input_documents=docs, question=query)
    
    if isinstance(response, str):
        logging.info("Request processed")
        return response
    else:
        logging.error("chain.run() did not return a string")
        return ""
