import pandas as pd
import random
import json
import requests
from prompting import OLLAMA_API_URL

# funkcja do generowania prompta z quizem
def generate_quiz_prompts(csv_file: str):
    # wczytanie danych z pliku CSV
    data = pd.read_csv(csv_file)
    data.columns = ['name', 'symptoms', 'diagnoses']

    # wybór losowej osoby
    selected_row = data.sample(1).iloc[0]
    symptoms = selected_row['symptoms']
    correct_diagnosis = selected_row['diagnoses']

    # zebranie błędnych diagnoz
    other_diagnoses = data[data['diagnoses'] != correct_diagnosis]['diagnoses'].unique()
    if len(other_diagnoses) < 3:
        raise ValueError("Za mało unikalnych diagnoz w pliku, aby stworzyć warianty odpowiedzi")
    wrong_answers = random.sample(list(other_diagnoses), 3)
    options = wrong_answers + [correct_diagnosis]
    random.shuffle(options)

    # prompt
    prompt = f'Given the following symptoms: {symptoms} guess the correct diagnoses. Choose one option out of A, B, C or D. Your answer should have only this one letter. A: {options[0]}, B: {options[1]}, C: {options[2]}, D: {options[3]}'
    if correct_diagnosis == options[0]:
        correct_answer = 'A'
    elif correct_diagnosis == options[1]:
        correct_answer = 'B'
    elif correct_diagnosis == options[2]:
        correct_answer = 'C'
    else:
        correct_answer = 'D'
    return prompt, correct_answer


# funkcja łącząca się z ollamą i zadająca mu pytanie w formie quizu
def ask_quiz():
    prompt, answer = generate_quiz_prompts("pacjenci.csv")

    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "temperature": 0.7
    }
    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()

        #print("Full response text:", response.text)

        # podział odpowiedzi na linie - czasami ollama odpowiada dziwnie
        lines = response.text.splitlines()

        model_response = None
        for line in lines:
            try:
                line_data = json.loads(line)
                # szukanie linii z odpowiedzią
                if "response" in line_data and line_data["done"] == False:
                    model_response = line_data["response"].strip()
                    break
            except json.JSONDecodeError:
                print(f"Failed to parse line: {line}")
                continue

        if model_response in ["A", "B", "C", "D"]:
            is_correct = model_response == answer
            print("Model response:", model_response)
            print("Correct answer:", answer)
            return 1 if is_correct else 0
        else:
            print("Unexpected response from model:", model_response)
            return 0
    except requests.RequestException as e:
        print("Request failed:", str(e))
        return 0



score = 0
iterations = 5
for _ in range(iterations):
    score += ask_quiz()

print(f"Skuteczność modelu: {score/iterations}")
