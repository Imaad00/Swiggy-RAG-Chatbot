import os
import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()

DB_FAISS_PATH = "vectorstore/db_faiss"

@st.cache_resource
def get_vectorstore():
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
    return db

def set_custom_prompt(custom_prompt_template):
    return PromptTemplate(template=custom_prompt_template, input_variables=["context", "question"])

# Minimal formatter
def get_text_preview(text, max_chars=300):
    text = text.replace("\n", " ").strip()
    if len(text) <= max_chars:
        return text
    preview = text[:max_chars]
    last_period = preview.rfind(".")
    if last_period != -1:
        return preview[:last_period+1]
    return preview + "..."

def format_source_docs_simple(source_docs):
    formatted = []
    for i, doc in enumerate(source_docs, 1):
        meta = doc.metadata
        page = meta.get('page_label') or meta.get('page') or 'N/A'
        content = get_text_preview(doc.page_content)
        formatted.append(f"{i}. Page {page} - {meta.get('source','N/A')}\n   {content}")
    return "\n".join(formatted)

def main():
    st.title("Ask SwiggyBot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        st.chat_message(message["role"]).markdown(message["content"])

    prompt = st.chat_input("Ask a Swiggy question...")

    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        CUSTOM_PROMPT_TEMPLATE = """
        Use the pieces of information provided in the context to answer the user's question.
        If the question is not relevant to the provided context, politely say that you are here to help with medical questions only.
        Context: {context}
        Question: {question}
        """

        try:
            vectorstore = get_vectorstore()
            qa_chain = RetrievalQA.from_chain_type(
                llm=ChatGroq(
                    model_name="meta-llama/llama-4-maverick-17b-128e-instruct",
                    temperature=0.0,
                    groq_api_key=os.environ["GROQ_API_KEY"]
                ),
                chain_type="stuff",
                retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
                return_source_documents=True,
                chain_type_kwargs={"prompt": set_custom_prompt(CUSTOM_PROMPT_TEMPLATE)},
            )

            response = qa_chain.invoke({"query": prompt})
            result = response["result"]
            source_docs = response["source_documents"]

            # Only show source documents if the answer is relevant (not an out-of-scope response)
            if ("I don't know" in result) or ("not relevant" in result) or ("help with swiggy annual report questions" in result):
                result_to_show = f"Answer:\n{result}"
            else:
                result_to_show = f"Answer:\n{result}\n\nSource Documents:\n{format_source_docs_simple(source_docs)}"

            st.chat_message("assistant").markdown(result_to_show)
            st.session_state.messages.append({"role": "assistant", "content": result_to_show})
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
