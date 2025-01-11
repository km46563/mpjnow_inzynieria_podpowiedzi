import csv

from prompting import get_disease
from extractor import process_csv, process_answer

filepath = 'pacjenci.csv'
data = process_csv(filepath)
output_csv = 'patients_data.csv'


with open(output_csv, mode='a', encoding='utf-8', newline='') as file:
    csv_writer = csv.writer(file)

    for patient, details in data.items():
        answer = get_disease(details['symptoms'])
        predicted_disease = process_answer(answer)
        print(predicted_disease)
        details['predicted_symptoms'] = predicted_disease
        csv_writer.writerow([
            patient,
            ", ".join(details['symptoms']),
            ", ".join(details['diagnoses']),
            ", ".join(details['predicted_symptoms'])
        ])
print("Data has been wrote")