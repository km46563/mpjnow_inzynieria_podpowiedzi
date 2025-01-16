import csv
from difflib import SequenceMatcher

def extract_disorders(file_path):
    true_predictions = {}

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 2:
                continue
            patient_id = row[0]
            findings = row[2]

            # Wyszukiwanie chorób oznaczonych jako (disorder)
            disorders = []
            findings_list = findings.split(';')
            for finding in findings_list:
                if '(disorder)' in finding:
                    disorder_name = finding.split('(')[0].strip()  # Usuwanie "(disorder) -> same nazwy chorób
                    disorders.append(disorder_name)

            if disorders:
                true_predictions[patient_id] = disorders

    return true_predictions

# Funkcja wydobywa predicted_diseases z csvek "patients_data_x_shot.csv"
def process_predicted_diseases(filepath):
    predicted_diseases = {}

    with open(filepath, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if not row:
                continue

            patient_key = row[0]
            predicted_disease_str = row[3]

            predicted_diseases_list = predicted_disease_str.split(', ')
            predicted_diseases[patient_key] = predicted_diseases_list

    return predicted_diseases

# Funkcja porównuje true_diseases z predicted_diseases, szuka podobieństw w nazwie np. "Acute Respiratory Infection" a "Acute viral pharyngitis"
def compare_diseases_fuzzy(true_diseases, predicted_diseases, threshold=0.6):
    correct_predictions = 0
    total_predictions = 0

    for patient_key in true_diseases:
        if patient_key in predicted_diseases:
            true_list = true_diseases[patient_key]
            predicted_list = predicted_diseases[patient_key]

            for true_disease in true_list:
                for predicted_disease in predicted_list:
                    similarity = SequenceMatcher(None, true_disease.lower(), predicted_disease.lower()).ratio()
                    if similarity >= threshold:
                        correct_predictions += 1
                        break

            total_predictions += len(true_list)

    accuracy = correct_predictions / total_predictions if total_predictions else 0
    return accuracy
