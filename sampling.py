import random
import pandas as pd
from statistics import mean, stdev
import matplotlib.pyplot as plt
from prompting import get_disease, get_disease_one_shot, get_disease_few_shot

def cross_validation_sampling(input_csv, output_csv, n_samples=5, sample_size=50, approach="zero_shot"):

   
    data = pd.read_csv(input_csv)
    print("Dostępne kolumny w danych:", data.columns) 
    results = []

    for i in range(n_samples):
        # tu zacyznamy losowanie
        sample = data.sample(n=min(sample_size, len(data)), random_state=random.randint(0, 1000))
        sample_results = []

        for _, row in sample.iterrows():
            patient = row.iloc[0]  
            symptoms = " ".join(row.iloc[1:].dropna())  

            if approach == "zero_shot":
                diseases = get_disease(symptoms)
            elif approach == "one_shot":
                diseases = get_disease_one_shot(symptoms)
            elif approach == "few_shot":
                diseases = get_disease_few_shot(symptoms)
            else:
                raise ValueError("Nieznane podejście: wybierz zero_shot, one_shot lub few_shot.")

            sample_results.append(len(diseases))

        # ocena tego losowania
        avg_result = mean(sample_results)
        std_result = stdev(sample_results) if len(sample_results) > 1 else 0
        results.append({"Sample": i + 1, "Mean": avg_result, "StdDev": std_result})


    results_df = pd.DataFrame(results)
    results_df.to_csv(output_csv, index=False)
    print(f"Wyniki zapisano w pliku: {output_csv}")




def plot_results(results_csv):

    results = pd.read_csv(results_csv)

    print("Wyniki:")
    print(results)

    
    plt.errorbar(
        results["Sample"],
        results["Mean"],
        yerr=results["StdDev"],
        fmt="o",
        capsize=5,
        label="Średnia z odchyleniem standardowym"
    )
    plt.xlabel("Numer próby")
    plt.ylabel("Średnia długość odpowiedzi")
    plt.title("Losowanie próbek")
    plt.legend()
    plt.grid(True)
    plt.show()


cross_validation_sampling("pacjenci.csv", "results_sampling.csv", n_samples=10, sample_size=50, approach="zero_shot")
plot_results("results_sampling.csv")
