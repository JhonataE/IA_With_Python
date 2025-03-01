# Importa bibliotecas necessárias
import csv  # Para ler o arquivo CSV
import sys  # Para trabalhar com argumentos de linha de comando

from sklearn.model_selection import train_test_split  # Para dividir os dados em conjuntos de treinamento e teste
from sklearn.neighbors import KNeighborsClassifier  # Para usar o classificador K-Nearest Neighbors

# Definindo o tamanho do conjunto de teste
TEST_SIZE = 0.4

# Função principal do script
def main():

    # Verifica se o número de argumentos fornecidos na linha de comando está correto
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")  # Encerra o programa se os argumentos não forem suficientes

    # Carrega os dados do arquivo CSV e divide em conjunto de treino e teste
    evidence, labels = load_data(sys.argv[1])  # Chama a função load_data para carregar os dados
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE  # Divide os dados com 40% para teste
    )

    # Treina o modelo KNN e faz as previsões
    model = train_model(X_train, y_train)  # Chama a função train_model para treinar o modelo
    predictions = model.predict(X_test)  # Faz previsões no conjunto de teste
    sensitivity, specificity = evaluate(y_test, predictions)  # Avalia as previsões com sensibilidade e especificidade

    # Exibe os resultados da avaliação
    print(f"Correct: {(y_test == predictions).sum()}")  # Exibe a quantidade de previsões corretas
    print(f"Incorrect: {(y_test != predictions).sum()}")  # Exibe a quantidade de previsões incorretas
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")  # Exibe a taxa de verdadeiro positivo (sensibilidade)
    print(f"True Negative Rate: {100 * specificity:.2f}%")  # Exibe a taxa de verdadeiro negativo (especificidade)

# Função que carrega os dados a partir de um arquivo CSV
def load_data(filename):
    evidence = []  # Lista para armazenar as evidências (dados de entrada)
    labels = []  # Lista para armazenar os rótulos (valores de saída)

    # Lista dos meses do ano, usada para converter o nome do mês em um valor numérico
    months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Abre o arquivo CSV e lê seus dados
    with open(filename, 'r') as file:
        reader = csv.reader(file)  # Cria um leitor de CSV
        next(reader)  # Pula o cabeçalho do arquivo CSV
        for row in reader:  # Para cada linha no arquivo CSV
            # A última coluna contém o valor de label (TRUE ou FALSE), converte para 1 ou 0
            if row[-1] == "TRUE":
                labels.append(1)
            else:
                labels.append(0)

            # Adiciona os dados de entrada (evidências) convertendo os valores conforme necessário
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
                1 if row[15] == "Returning_Visitor" else 0,  # Converte para 1 se for Returning_Visitor, caso contrário 0
                1 if row[16] == "TRUE" else 0  # Converte para 1 se for TRUE, caso contrário 0
            ])

    # Retorna as evidências e os rótulos
    return evidence, labels

# Função que treina o modelo KNN (K-Nearest Neighbors)
def train_model(evidence, labels):
    # Cria o modelo KNN com 1 vizinho
    neigh = KNeighborsClassifier(n_neighbors = 1)
    neigh.fit(evidence, labels)  # Treina o modelo com as evidências e os rótulos
    return neigh  # Retorna o modelo treinado

# Função que avalia as previsões do modelo
def evaluate(labels, predictions):
    # Variáveis para contar os verdadeiros positivos, verdadeiros negativos, etc.
    true_positives = 0
    actual_positives = 0
    true_negatives = 0
    actual_negatives = 0

    # Percorre todos os rótulos e previsões para contar os verdadeiros positivos e negativos
    for index in range(len(labels)):
        if labels[index] == 1:  
            actual_positives += 1  
            if predictions[index] == 1:  
                true_positives += 1 
        else:  # Se o rótulo for 0 (negativo)
            actual_negatives += 1  
            if predictions[index] == 0: 
                true_negatives += 1  

    #(taxa de verdadeiros positivos) e (taxa de verdadeiros negativos)
    sensitivity = true_positives / actual_positives
    specificity = true_negatives / actual_negatives

    # Retorna os valores de sensibilidade e especificidade
    return sensitivity, specificity

# Executa a função main se o script for chamado diretamente
if __name__ == "__main__":
    main()
