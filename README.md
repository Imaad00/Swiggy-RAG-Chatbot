# 📊 Swiggy Annual Report RAG Chatbot

This project demonstrates how to build a **Retrieval-Augmented Generation (RAG) based Question Answering chatbot** using open-source tools.  
It is designed to answer questions **strictly based on the Swiggy Annual Report (FY 2023–24)**.

It leverages:

- **HuggingFace** → For text embeddings  
- **FAISS (CPU)** → For fast vector similarity search  
- **LangChain** → For RAG orchestration  
- **Streamlit** → For a simple web-based conversational interface  
- **Mistral / LLaMA (via Groq API)** → As the large language model  

The chatbot reads and understands the Swiggy Annual Report PDF and answers business-related queries while **preventing hallucinations**.

---

## 📂 Project Structure

```bash
├── Pipfile
├── Pipfile.lock
├── README.md
├── connect_memory_with_llm.py
├── create_memory_for_llm.py
├── data
│   └── Swiggy_Annual_Report_2023_24.pdf
├── swiggybot.py
├── requirements.txt
└── vectorstore
    └── db_faiss
        ├── index.faiss
        └── index.pkl
```

- `data/` → Contains the Swiggy Annual Report PDF  
- `vectorstore/` → Stores FAISS vector indexes  
- `create_memory_for_llm.py` → Builds the FAISS vector store  
- `connect_memory_with_llm.py` → Connects FAISS with the LLM  
- `swiggybot.py` → Streamlit chatbot application  

---

## 📄 Dataset

- **Document Name**: Swiggy Annual Report FY 2023–24  
- **Format**: PDF  
- **Source**: https://www.swiggy.com/about-us/

The chatbot answers questions **only using this document** and explicitly refuses if information is not present.

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
HF_TOKEN=your_huggingface_token_here
```

API keys are managed using environment variables to avoid hardcoding sensitive information.

---

## 🚀 Getting Started

### 1️⃣ Prerequisites

- Python **3.11**
- Git

Verify Python version:

```bash
python --version
```

---

### 2️⃣ Create Virtual Environment

Create a virtual environment using Python 3.11:

```bash
py -3.11 -m venv .venv
```

Activate the environment:

**Windows**
```bash
.venv\Scripts\activate
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

---

### 3️⃣ Install Dependencies

Upgrade pip and install required packages:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4️⃣ Prepare the Knowledge Base

This step performs the following actions:

- Loads the Swiggy Annual Report PDF  
- Splits the document into meaningful text chunks  
- Generates embeddings using HuggingFace models  
- Stores the embeddings in FAISS for efficient retrieval  

Run the indexing script:

```bash
python create_memory_for_llm.py
```

The FAISS index will be created at:

```text
vectorstore/db_faiss/
```

---

### 5️⃣ Run the Chatbot

Start the Streamlit application:

```bash
streamlit run swiggybot.py
```

---

## ⚙️ How It Works

1. Document ingestion and chunking  
2. Embedding generation using HuggingFace  
3. FAISS vector similarity search  
4. Retrieval-Augmented Generation using LLM  
5. Streamlit-based conversational UI  

The LLM answers **only from retrieved context**.

---

## 💬 Demo Conversation

**User:**  
Describe Swiggy’s Food Delivery business performance.

**SwiggyBot:**  
Swiggy's Food Delivery business has shown significant growth. The user base has expanded by approximately 1.1 times, and the number of restaurant partners has also grown by around 1.1 times. The Gross Order Value (GOV) has increased due to a rise in Average Order Value (AOV), driven by premium offerings and larger basket sizes. Additionally, the total number of orders has grown by 17% year-over-year (YoY), driven by an increasing user base and ordering frequency.

**Source Documents:**
- Page 6 – data\Annual-Report-FY-2023-24.pdf convenience. Innovation has been an integral part of our DNA which encourages us to ideate, experiment and iterate constantly with the focus on identifying and addressing convenience needs of our users at the core of our innovation approach.
- Page 7 – data\Annual-Report-FY-2023-24.pdf 5 dynamic experiences to our users across their entire food consumption journey. Dineout is fully integrated within Swiggy and is the leader in the dining out category in the country across 43 cities.  
- Page 9 – data\Annual-Report-FY-2023-24.pdf 7 Food Delivery: Our Food Delivery segment has continued to grow with a ~1. 1x6 expansion in user base and a ~1.1x expansion in no. of restaurant partners. The expansion in GOV is catalyzed by an increase in AOV due to increased premium offerings and larger basket sizes. 

---

✨ This project demonstrates a real-world, document-grounded RAG system suitable for enterprise financial analysis and reporting.
