import csv

from prompting import get_disease, get_disease_one_shot, get_disease_few_shot
from extractor import process_csv, process_answer

filepath = 'pacjenci.csv'
data = process_csv(filepath)
output_csv_zero_shot = 'patients_data_zero_shot.csv'
output_csv_one_shot = 'patients_data_one_shot.csv'
output_csv_few_shot = 'patients_data_few_shot.csv'

# Zero-shot implementation
with open(output_csv_zero_shot, mode='a', encoding='utf-8', newline='') as file:
    csv_writer = csv.writer(file)

    for patient, details in data.items():
        answer = get_disease(details['symptoms'])
        predicted_disease = process_answer(answer)
        print(f"[Zero-shot] Predicted disease: {predicted_disease}")
        details['predicted_symptoms'] = predicted_disease
        csv_writer.writerow([
            patient,
            ", ".join(details['symptoms']),
            ", ".join(details['diagnoses']),
            ", ".join(details['predicted_symptoms'])
        ])
print("ZAKONCZONO ZERO-SHOT")

# One-shot implementation
with open(output_csv_one_shot, mode='a', encoding='utf-8', newline='') as file:
    csv_writer = csv.writer(file)

    for patient, details in data.items():
        answer = get_disease_one_shot(details['symptoms'])
        predicted_disease = process_answer(answer)
        print(f"[One-shot] Predicted disease: {predicted_disease}")
        details['predicted_symptoms'] = predicted_disease
        csv_writer.writerow([
            patient,
            ", ".join(details['symptoms']),
            ", ".join(details['diagnoses']),
            ", ".join(details['predicted_symptoms'])
        ])

print("ZAKONCZONO ONE-SHOT")


# Few-shot implementation
with open(output_csv_few_shot, mode='a', encoding='utf-8', newline='') as file:
    csv_writer = csv.writer(file)

    for patient, details in data.items():
        answer = get_disease_few_shot(details['symptoms'])
        predicted_disease = process_answer(answer)
        print(f"[Few-shot] Predicted disease: {predicted_disease}")
        details['predicted_symptoms'] = predicted_disease
        csv_writer.writerow([
            patient,
            ", ".join(details['symptoms']),
            ", ".join(details['diagnoses']),
            ", ".join(details['predicted_symptoms'])
        ])

print("ZAKONCZONO FEW-SHOT")