import requests
import json

OLLAMA_API_URL = 'http://localhost:11434/api/generate'

def get_disease(symptoms):
    prompt = f"""
    Analyze the following symptoms: {symptoms}. Based on these symptoms, return a list of possible diseases. Format the response **EXACTLY** like this:
    **disease1**, **disease2**, **disease3**, ...

    Do NOT include explanations or other text.

    Symptoms: {symptoms}
    """
    payload = {
        "model": "llama3.2",        # Tu można zmienić model Ollama
        "prompt": prompt,
        "temperature": 0.3,          # ~0: kreatywność, ~1: precyzja
        "max_tokens": 100,
        "stream": False
    }
    print(prompt)
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



def get_disease_one_shot(symptoms):
    """
    Generuje przewidywania chorób na podstawie objawów, wykorzystując podejście one-shot.
    """
    # Przykład do One-shot learning
    example = (
        "Patient has the following symptoms: chest pain, dizziness, excessive sweating.\n"
        "Diagnosis: myocardial infarction.\n\n"
        "Now analyze another case:"
    )

    # Tworzenie promptu z przykładem
    prompt = (
        f'{example}\n'
        f'The patient has symptoms: {symptoms}. What are the most likely diagnoses for this patient?'
        f'Answer me with the following format: "**disease1**, **disease2**, **disease3**, ..."'
    )

    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "temperature": 0.7,
        "max_tokens": 50,
        "stream": False
    }

    print(prompt)  # Debugging prompt

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()

        data = response.json()

        print("Full API response: ", data)  # Debugging response

        if 'response' in data:
            diseases = [line.strip() for line in data['response'].split('\n') if line.strip()]
        elif 'choices' in data and isinstance(data['choices'], list) and len(data['choices']) > 0:
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
        print(f"KeyError in API response: {ke}")
        return []
    


def get_disease_few_shot(symptoms):
    """
    Generuje przewidywania chorób na podstawie objawów, wykorzystując podejście few-shot.
    """
    # Przykłady do Few-shot learning
    examples = (
        "Patient has the following symptoms: chest pain, dizziness, excessive sweating.\n"
        "Diagnosis: myocardial infarction.\n\n"
        "Patient has the following symptoms: fever, cough, sore throat.\n"
        "Diagnosis: viral infection.\n\n"
        "Patient has the following symptoms: abdominal pain, vomiting, diarrhea.\n"
        "Diagnosis: food poisoning.\n\n"
        "Now analyze another case:"
    )

    # Tworzenie promptu z kilkoma przykładami
    prompt = (
        f"{examples}\n"
        f"The patient has symptoms: {symptoms}. What are the most likely diagnoses for this patient?"
        f"Answer me with the following format: '**disease1**, **disease2**, **disease3**, ...'"
    )

    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "temperature": 0.7,
        "max_tokens": 50,
        "stream": False
    }

    print(prompt)  # Debugging prompt

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()

        data = response.json()

        print("Full API response: ", data)  # Debugging response

        if 'response' in data:
            diseases = [line.strip() for line in data['response'].split('\n') if line.strip()]
        elif 'choices' in data and isinstance(data['choices'], list) and len(data['choices']) > 0:
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
        print(f"KeyError in API response: {ke}")
        return []
