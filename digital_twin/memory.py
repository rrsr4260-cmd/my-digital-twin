from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from config import MEMORY_RESULTS

# Optional MongoDB support
MONGO_AVAILABLE = False
collection = None

try:
    from pymongo import MongoClient
    from config import MONGO_URI, DATABASE_NAME, MEMORY_COLLECTION

    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    client.server_info()  # test connection

    db = client[DATABASE_NAME]
    collection = db[MEMORY_COLLECTION]
    MONGO_AVAILABLE = True
    print("MongoDB connected successfully.")

except Exception as e:
    print("MongoDB not available. Running with local memory only.")
    print("MongoDB error:", e)

model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

dimension = 384
index = faiss.IndexFlatL2(dimension)

memory_texts = []

def load_memory():
    print("Loading memory...")

    vectors = []
    memory_texts.clear()

    if MONGO_AVAILABLE and collection is not None:
        try:
            for doc in collection.find():
                text = doc.get("text", "").strip()
                if not text:
                    continue

                memory_texts.append(text)
                vector = model.encode(text, convert_to_numpy=True)
                vectors.append(vector)

        except Exception as e:
            print("MongoDB load error:", e)

    if vectors:
        vectors = np.array(vectors).astype("float32")
        index.add(vectors)

    print("Memory loaded:", len(memory_texts))

def save_memory(text: str):
    try:
        if not text.strip():
            return

        vector = model.encode(text, convert_to_numpy=True)

        memory_texts.append(text)
        index.add(np.array([vector]).astype("float32"))

        if MONGO_AVAILABLE and collection is not None:
            try:
                collection.insert_one({"text": text})
            except Exception as e:
                print("MongoDB save error:", e)

    except Exception as e:
        print("Save memory error:", e)

def search_memory(query: str) -> str:
    try:
        if len(memory_texts) == 0:
            return ""

        vector = model.encode(query, convert_to_numpy=True)
        _, indices = index.search(np.array([vector]).astype("float32"), MEMORY_RESULTS)

        results = []
        for i in indices[0]:
            if 0 <= i < len(memory_texts):
                results.append(memory_texts[i])

        return "\n".join(results)

    except Exception as e:
        print("Search memory error:", e)
        return ""

load_memory()