import json 
import os 
import csv 


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


folder = 'fhir'
output = 'pacjenci.csv'

extract_data(folder, output)
