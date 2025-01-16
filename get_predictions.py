import csv

from prompting import get_disease, get_disease_one_shot, get_disease_few_shot
from extractor import process_csv, process_answer
from utils import process_predicted_diseases, extract_disorders, compare_diseases_fuzzy

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

print("----------------------------")
print("TRUE DISEASES")
true_diseases = extract_disorders(filepath)
print(true_diseases)

print("----------------------------")
print("PREDICTED DISEASES ZERO SHOT")
predicted_diseases_zero = process_predicted_diseases(output_csv_zero_shot)
print(predicted_diseases_zero)

print("----------------------------")
print("PREDICTED DISEASES ONE SHOT")
predicted_diseases_one = process_predicted_diseases(output_csv_one_shot)
print(predicted_diseases_one)

print("----------------------------")
print("PREDICTED DISEASES FEW SHOT")
predicted_diseases_few = process_predicted_diseases(output_csv_few_shot)
print(predicted_diseases_few)

print("----------------------------")
print("COMPARE DISEASES ZERO SHOT")
accuracy = compare_diseases_fuzzy(true_diseases, predicted_diseases_zero, threshold=0.6)
print(f"Fuzzy matching accuracy: {accuracy:.2%}")

print("----------------------------")
print("COMPARE DISEASES ONE SHOT")
accuracy = compare_diseases_fuzzy(true_diseases, predicted_diseases_one, threshold=0.6)
print(f"Fuzzy matching accuracy: {accuracy:.2%}")

print("----------------------------")
print("COMPARE DISEASES FEW SHOT")
accuracy = compare_diseases_fuzzy(true_diseases, predicted_diseases_few, threshold=0.6)
print(f"Fuzzy matching accuracy: {accuracy:.2%}")
