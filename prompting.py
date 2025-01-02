import requests
import json

OLLAMA_API_URL = 'http://localhost:11434/api/generate'

def get_disease(symptoms):
    prompt = f"Given the following symptoms: {', '.join(symptoms)}, identify possible diseases."
    payload = {
        "model": "llama3.2",        # Tu można zmienić model Ollama
        "prompt": prompt,
        "temperature": 0.7,          # ~0: kreatywność, ~1: precyzja
        "max_tokens": 50,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()

        data = response.json()

        print("Full API response: ", data)

        if 'response' in data:
            diseases = [line.strip() for line in data['response'].split('\n') if line.strip()]
        elif 'choices' in data and isinstance(data['choices'], list) and len(data['choices']) > 0:
            # If the API returns choices, use the first choice text
            diseases = [line.strip() for line in data['choices'][0]['text'].split('\n') if line.strip()]
        else:
            raise KeyError("Unexpected response structure from Ollama API")

        return diseases

    except requests.exceptions.RequestException as e:
        print(f"Error podczas wysyłania zapytania: {e}")
        return []
    except ValueError as ve:
        print(f"JSON decoding error: {ve}")
        return []
    except KeyError as ke:
        print(f"KeyError in aAPI response: {ke}")
        return []

symptoms = ["fever", "cough", "sore throat"]
detected_diseases = get_disease(symptoms)
print("detected diseases: ", detected_diseases)