from pymongo import MongoClient
import uuid
from langchain_openai import OpenAI
from langchain.chains import RetrievalQA
# from langchain.vectorstores import MongoDBAtlasVectorSearch  # Removed because module could not be resolved
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
import os


class SimilarToolchain(object):
    """description of class"""
    

    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["llm_docs"]
    collection = db["documents"]

    # Sample document
    text = """LangChain is a powerful framework for building applications with language models. It supports memory, tools, agents, and chains."""

    # Upload to MongoDB
    doc_id = str(uuid.uuid4())
    collection.insert_one({"_id": doc_id, "text": text})
    print(f"✅ Document uploaded with ID: {doc_id}")
    
    # Load document from MongoDB
    doc_data = collection.find_one({"_id": doc_id})
    doc_text = doc_data["text"]

    # Create LangChain document
    document = Document(page_content=doc_text)

    # Embed and store in memory (or use MongoDB Vector Search if configured)
    os.environ["OPENAI_API_KEY"] = "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"

    embedding = OpenAIEmbeddings()
    embedded_doc = embedding.embed_documents([document.page_content])

    # Use LLM to answer a question
    llm = OpenAI(temperature=0)
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=None)  # Replace with actual retriever if using vector search

    query = "What is LangChain used for?"
    response = llm.predict(f"Answer this based on the document: {doc_text}\n\nQuestion: {query}")
    print("🤖 Answer:", response)
