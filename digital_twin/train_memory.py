import json
from memory import save_memory

TRAINING_FILE = "training_data.jsonl"

def train():
    count = 0

    with open(TRAINING_FILE, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)

            user = data.get("input", "").strip()
            twin = data.get("response", "").strip()

            if user:
                save_memory("User: " + user)
            if twin:
                save_memory("Twin: " + twin)

            count += 1

    print("Training completed:", count)

if __name__ == "__main__":
    train()