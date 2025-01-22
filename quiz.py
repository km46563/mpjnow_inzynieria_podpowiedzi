import pandas as pd
import random
import json
import re
import requests
from prompting import OLLAMA_API_URL


def extract_choice(response):
    """
    Extract the first occurrence of 'A', 'B', 'C', or 'D' from the model's response, even in more complex sentences.
    :param response: Full response string from the model
    :return: Extracted choice (e.g., 'A') or None if not found
    """
    # Szuka litery A, B, C, lub D w odpowiedzi, nawet w pełnych zdaniach
    match = re.search(r'\b([A-D])\b', response)
    return match.group(1) if match else None


# Funkcja do generowania prompta z quizem
def generate_quiz_prompts(csv_file: str):
    # Wczytanie danych z pliku CSV
    data = pd.read_csv(csv_file)
    data.columns = ['name', 'symptoms', 'diagnoses']

    # Wybór losowej osoby
    selected_row = data.sample(1).iloc[0]
    symptoms = selected_row['symptoms']
    correct_diagnosis = selected_row['diagnoses']

    # Zebranie błędnych diagnoz
    other_diagnoses = data[data['diagnoses'] != correct_diagnosis]['diagnoses'].unique()
    if len(other_diagnoses) < 3:
        raise ValueError("Za mało unikalnych diagnoz w pliku, aby stworzyć warianty odpowiedzi")
    wrong_answers = random.sample(list(other_diagnoses), 3)
    options = wrong_answers + [correct_diagnosis]
    random.shuffle(options)

    # Tworzenie prompta - troche go zmodyfikowalam
    prompt = (f"Given the following symptoms: {symptoms} guess the correct diagnoses. "
              f"Choose one option out of A, B, C or D. Your answer should have only this one letter. "
              f"A: {options[0]}, B: {options[1]}, C: {options[2]}, D: {options[3]}. "
              "Respond with just one letter (A, B, C, or D). If you're unsure, choose the one you think is the most likely.")

    correct_answer = ['A', 'B', 'C', 'D'][options.index(correct_diagnosis)]
    return prompt, correct_answer


# Funkcja łącząca się z modelem i zadająca pytanie w formie quizu
def ask_quiz():
    prompt, answer = generate_quiz_prompts("pacjenci.csv")
    print("\n--- Quiz ---")
    print("Prompt for the model:\n", prompt)
    print(f"Expected correct answer: {answer}")

    payload = {
        "model": "medllama2",
        "prompt": prompt,
        "temperature": 0.3
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()

        # Przetwarzanie odpowiedzi
        model_response = None
        combined_response = ""
        for line in response.text.splitlines():
            try:
                line_data = json.loads(line)
                if "response" in line_data:
                    combined_response += line_data["response"]
            except json.JSONDecodeError:
                print(f"Failed to parse line: {line}")
                continue

        # Wyciągnięcie odpowiedzi modelu
        model_choice = extract_choice(combined_response)
        print(f"Model response (combined): {combined_response}")
        print(f"Extracted choice: {model_choice}")

        # Jeśli model nie podał odpowiedzi w formie litery, spróbujmy wziąć odpowiedź z pełnej treści
        if not model_choice:
            model_choice = "A"

        # Sprawdzenie poprawności odpowiedzi
        if model_choice in ["A", "B", "C", "D"]:
            is_correct = model_choice == answer
            print(f"Correct answer: {answer}")
            print(f"Result: {'Correct' if is_correct else 'Incorrect'}")
            return 1 if is_correct else 0
        else:
            print("Unexpected response from model:", combined_response)
            return 0

    except requests.RequestException as e:
        print("Request failed:", str(e))
        return 0


# Główna pętla quizu
score = 0
iterations = 15
for _ in range(iterations):
    score += ask_quiz()

# Poprawne obliczanie skuteczności
print(f"Skuteczność modelu: {score / iterations:.2f}")
