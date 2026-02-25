from dotenv import load_dotenv
import asyncio
import edge_tts
import os
import random
import requests
import subprocess

load_dotenv()

async def edgeVoice(llm_result):
    VOICE_POOL = ["Andrew", "Ava", "Brian", "Christopher", "Emma", "Eric", "Guy", "Jenny", "Michelle", "Roger", "Steffan"]
    # pick a random number between 0 and the length of the voice pool - 1
    random_voice_index = random.randrange(len(VOICE_POOL))
    random_voice = VOICE_POOL[random_voice_index]
    tts = edge_tts.Communicate(
        llm_result,
        voice=f"en-US-{random_voice}Neural",  # pick any supported voice
        rate="+0%",
        volume="+0%"
    )
    try:
        await tts.save(f"./audio_files/{random_voice}.mp3")
    except Exception as e:
        print(f"Error saving audio: {e}")
    try:
        subprocess.run(["afplay", f"./audio_files/{random_voice}.mp3"])
    except Exception as e:
        print(f"Error playing audio: {e}")

def processBasicLLMRequest(user_message: str):
    api_key=os.getenv("API_KEY_LOCAL")
    base_url=os.getenv("BASE_URL_LOCAL")
    complete_url=f"{base_url}/v1/chat/completions"
    llm_model=os.getenv("LLM_MODEL_LOCAL")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": llm_model,
        "messages": [
            {"role": "system", "content": "Please respond as if you are a human user in an IRC channel where others might have responded to the user's question. Respond with a short 1 sentence response. Do not include any emojis or special characters. Do not include any formatting. Just respond with a simple sentence."},
            {"role": "user", "content": user_message}
        ]
    }
    assistant_reply = ""

    response = requests.post(complete_url, headers=headers, json=payload)
    if response.status_code == 200:
        response_data = response.json()
        assistant_reply = response_data['choices'][0]['message']['content']
        print("Response Code:", response.status_code)
    else:
        assistant_reply = f"Error: {response.status_code} - {response.text}"

    return assistant_reply


if __name__ == "__main__":
    user_message = "What is a good snack chip choice?"
    llm_result = processBasicLLMRequest(user_message)
    asyncio.run(edgeVoice(llm_result))