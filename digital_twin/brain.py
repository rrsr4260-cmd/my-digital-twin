import ollama
from memory import search_memory, save_memory
from voice_clone import speak_clone
from config import MODEL_NAME

BASE_PROMPT = """
You are Rituraj Singh's Digital Twin.

Rules:
- Reply in natural Hinglish.
- Sound human, friendly, and conversational.
- Keep replies clear and not too long.
- Never say you are an AI.
- You are Rituraj.
- If user is emotional, respond with matching emotion and support.
"""

def detect_emotion(text: str) -> str:
    text = text.lower()

    sad_words = [
        "sad", "upset", "depressed", "cry", "alone", "hurt", "bad",
        "dukhi", "udaas", "rona", "pareshan", "toot gaya", "mood off"
    ]
    angry_words = [
        "angry", "mad", "hate", "annoyed", "frustrated", "irritated",
        "gussa", "ghussa", "bekar", "faltu", "frustrate", "chidh"
    ]
    happy_words = [
        "happy", "great", "awesome", "excited", "love", "good",
        "khush", "mast", "badiya", "maza", "acha lag raha"
    ]
    anxious_words = [
        "worried", "anxious", "nervous", "stress", "scared", "panic",
        "tension", "dar", "ghabrahat", "fikar"
    ]

    if any(word in text for word in sad_words):
        return "sad"
    if any(word in text for word in angry_words):
        return "angry"
    if any(word in text for word in happy_words):
        return "happy"
    if any(word in text for word in anxious_words):
        return "anxious"
    return "neutral"

def emotion_prompt(emotion: str) -> str:
    prompts = {
        "sad": (
            "The user sounds sad. Reply in gentle, caring Hinglish. "
            "Be emotionally supportive. Use natural phrases like "
            "'arey', 'main samajh raha hoon', 'tension mat le'."
        ),
        "angry": (
            "The user sounds angry. Reply in calm, grounded Hinglish. "
            "Do not sound aggressive. Focus on solution."
        ),
        "happy": (
            "The user sounds happy. Reply in cheerful, energetic Hinglish."
        ),
        "anxious": (
            "The user sounds anxious. Reply in reassuring Hinglish. "
            "Reduce panic. Be practical and calm."
        ),
        "neutral": (
            "Reply in casual, friendly Hinglish."
        )
    }
    return prompts.get(emotion, prompts["neutral"])

def refine_reply(reply: str, emotion: str) -> str:
    reply = reply.strip()

    if emotion == "sad" and not reply.lower().startswith("arey"):
        return "Arey, " + reply
    if emotion == "angry" and not reply.lower().startswith("samajh gaya"):
        return "Samajh gaya, " + reply
    if emotion == "happy" and not reply.lower().startswith("wah"):
        return "Wah bhai, " + reply
    if emotion == "anxious" and "tension mat le" not in reply.lower():
        return "Tension mat le, " + reply
    return reply

def think(user_input: str) -> str:
    try:
        print("Thinking...")

        memories = search_memory(user_input)
        emotion = detect_emotion(user_input)
        style_prompt = emotion_prompt(emotion)

        messages = [
            {"role": "system", "content": BASE_PROMPT},
            {"role": "system", "content": style_prompt},
            {"role": "user", "content": f"Past memories:\n{memories}"},
            {"role": "user", "content": user_input}
        ]

        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages
        )

        reply = response["message"]["content"].strip()
        reply = refine_reply(reply, emotion)

        print("AI Reply:", reply)

        save_memory("User: " + user_input)
        save_memory("Emotion: " + emotion)
        save_memory("Twin: " + reply)

        speak_clone(reply)

        return reply

    except Exception as e:
        print("Brain error:", e)
        return "Bhai thoda system issue aa gaya."