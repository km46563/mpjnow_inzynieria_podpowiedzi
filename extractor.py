import json 
import os 
import csv
import re


# Funkcja zapisująca dane pacjenta w pliku .csv 
def extract_data(folder, output):

    data = []

    for filename in os.listdir(folder):
        if filename.endswith('.json'):
            path = os.path.join(folder, filename)
            with open(path, 'r') as file:
                try:
                    patient_data = json.load(file)
                    name = "Nieznane"       # Zmienna na imię i nazwisko pacjenta 

                    # Listy na symptomy i diagnozy
                    symptoms = []
                    diagnoses = []

                    if 'entry' in patient_data:
                        for entry in patient_data['entry']:
                            resource = entry.get('resource', {})

                            # Dane pacjenta
                            if resource.get('resourceType') == 'Patient':
                                if 'name' in resource:
                                    names = resource['name'][0]
                                    first_name = names.get('given', [""])[0]
                                    last_name = names.get('family', "Nieznane")
                                    name = f'{first_name, last_name}'

                            # Diagnozy
                            if resource.get('resourceType') == 'Condition':
                                if 'code' in resource:
                                    diagnosis = resource['code'].get('text', 'Brak diagnozy')
                                    diagnoses.append(diagnosis)

                            # Symptomy
                            if resource.get('resourceType') == 'Observation':
                                if 'code' in resource:
                                    observation_text = resource['code'].get('text', None)
                                    if observation_text:
                                        symptoms.append(observation_text)
                                if 'valueString' in resource:
                                    symptoms.append(resource['valueString'])

                    # Formatowanie list
                    symptoms = '; '.join(set(symptoms))
                    diagnoses = '; '.join(set(diagnoses))

                    data.append([name, symptoms, diagnoses])

                except json.JSONDecodeError as e:
                    print(f"Błąd dekodowania JSON w pliku {filename}: {e}")

    with open(output, 'w', newline='', encoding='utf8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(data)

    print("Zapisano dane pacjenta")


# Funkcja wczytująca dane z pliku csv do tablic
def process_csv(filepath):
    data = {}

    with (open(filepath, mode='r', encoding='utf-8') as file):
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if not row:
                continue

            # Ekstrakcja danych
            names = row[0]
            symptoms = row[1].split(', ')
            diagnoses = row[2].split(', ')

            # Ekstrakcja symptomów i diagnoz
            #symptoms_str, diagnoses_str = symptoms_diagnoses.split(",", maxsplit=1)
            #symptoms = {symptom.strip() for symptom in symptoms_str.split(";")}
            #diagnoses = {diagnosis.strip() for diagnosis in diagnoses_str.split(";")}

            # Stworzenie słownika - pojedynczy rekord zawiera wszystkie symptomy lub diagnozy pojedynczego pacjenta
            data[names] = {'symptoms': symptoms, 'diagnoses': diagnoses}
    return data


# Funkcja, która z odpowiedzi modelu tworzy listę z przewidzianymi nazwami chorób
def process_answer(answer):
    diseases = []
    pattern = r'\*\*(.*?)\*\*'  # Nazwy chorób znajdują się pomiędzy znakami ** (np. **choroba1**)
    for line in answer:
        matches = re.findall(pattern, line)
        diseases.extend(matches)
    return diseases