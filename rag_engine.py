import os
import PyPDF2
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions
import ollama

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# --- Reranker Model Setup ---
# Load only ONCE for efficiency!
global_reranker_tokenizer = None
global_reranker_model = None

def setup_reranker(model_name="BAAI/bge-reranker-v2-m3"):
    global global_reranker_tokenizer, global_reranker_model
    if global_reranker_tokenizer is None or global_reranker_model is None:
        global_reranker_tokenizer = AutoTokenizer.from_pretrained(model_name)
        global_reranker_model = AutoModelForSequenceClassification.from_pretrained(model_name)
    return global_reranker_tokenizer, global_reranker_model

# --- PDF ---
def extract_text(pdf_path: str) -> str:
    text = []
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for p in reader.pages:
            page_text = p.extract_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text)

def chunk_with_overlap(text: str, chunk_size: int = 500, overlap: int = 20):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i : i + chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
    return chunks

def build_chroma_collection(chunks, name="pdf_collection"):
    client = chromadb.Client()
    try:
        col = client.get_collection(name=name)
    except chromadb.errors.NotFoundError:
        col = client.create_collection(
            name=name,
            embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
        )
    if col.count() == 0:
        col.add(
            documents=chunks,
            ids=[f"chunk_{i}" for i in range(len(chunks))]
        )
    return col

def retrieve_chunks(query: str, collection, n_results=10):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results["documents"][0]  # List of candidate chunks

# --- HF reranker ---
def rerank_with_bge(query, candidates, model_name="BAAI/bge-reranker-v2-m3"):
    tokenizer, model = setup_reranker(model_name)
    pairs = [(query, doc) for doc in candidates]
    # Batch encode
    inputs = tokenizer(
        [q for q, d in pairs],
        [d for q, d in pairs],
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=512,
    )
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits[:, 0]  # Shape: (num_candidates,)
    scores = logits.tolist()
    best_idx = scores.index(max(scores))
    return candidates[best_idx]

def ask_ollama(context: str, question: str, model="llama3:instruct"):
    prompt = f"""Context:
{context}

Question:
{question}

Answer:"""
    resp = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return resp["message"]["content"]

def rag_call(que: str):
    PDF_FILE = "Tasks.pdf"
    question = que.strip()

    text = extract_text(PDF_FILE)
    print(f"[✓] extract_text: got {len(text)} characters")

    chunks = chunk_with_overlap(text, chunk_size=500, overlap=20)
    print(f"[✓] chunk_with_overlap: produced {len(chunks)} chunks")

    collection = build_chroma_collection(chunks, name="pdf_collection")
    print(f"[✓] build_chroma_collection: stored {collection.count()} embeddings")

    candidates = retrieve_chunks(question, collection, n_results=10)
    print(f"[✓] retrieve_chunks: gathered {len(candidates)} candidates")

    best_chunk = rerank_with_bge(question, candidates, model_name="BAAI/bge-reranker-v2-m3")
    print(f"[✓] rerank_with_bge: selected chunk: \"{best_chunk[:80]}...\"")

    answer = ask_ollama(best_chunk, question, model="llama3:instruct")
    print("\n💡 Answer:\n", answer)
    print("[✓] ask_ollama success")

    return answer
