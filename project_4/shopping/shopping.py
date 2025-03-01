import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")




def load_data(filename):
    evidence = []
    labels = []

    months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:

            if row[-1] == "TRUE":
                labels.append(1)
            else:
                labels.append(0)

            evidence.append([
                int(row[0]), 
                float(row[1]),
                int(row[2]), 
                float(row[3]),
                int(row[4]), 
                float(row[5]),
                float(row[6]),
                float(row[7]),
                float(row[8]),
                float(row[9]),
                months.index(row[10]),
                int(row[11]),
                int(row[12]),
                int(row[13]),
                int(row[14]),
                1 if row[15] == "Returning_Visitor" else 0,
                1 if row[16] == "TRUE" else 0
            ])

    return evidence, labels


def train_model(evidence, labels):
    
    neigh = KNeighborsClassifier(n_neighbors = 1)
    neigh.fit(evidence, labels)
    return neigh


def evaluate(labels, predictions):
    
    true_positives = 0
    actual_positives = 0
    true_negatives = 0
    actual_negatives = 0

    for index in range(len(labels)):
        if labels[index] == 1:
            actual_positives += 1
            if predictions[index] == 1:
                true_positives += 1
        else:
            actual_negatives += 1
            if predictions[index] == 0:
                true_negatives += 1

    sensitivity = true_positives / actual_positives
    specificity = true_negatives / actual_negatives

    return sensitivity, specificity
    


if __name__ == "__main__":
    main()
