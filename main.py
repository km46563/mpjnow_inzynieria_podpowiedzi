import csv

from prompting import get_disease
from extractor import process_csv, process_answer

filepath = 'pacjenci.csv'
symptoms, diagnoses = process_csv(filepath)

prediction = get_disease(symptoms[0])
predicted_disease = process_answer(prediction)

print(predicted_disease)