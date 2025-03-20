import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Carrega os dados das imagens a partir do diretório especificado.
    
    Parâmetros:
        data_dir (str): Caminho do diretório contendo as imagens organizadas em subdiretórios.
    
    Retorna:
        tuple: Duas listas, uma contendo as imagens e outra contendo os rótulos.
    """
    images = []  # Lista para armazenar as imagens
    labels = []  # Lista para armazenar os rótulos (categorias)
    
    # Percorre os subdiretórios dentro de data_dir
    for category in range(NUM_CATEGORIES):
        category_path = os.path.join(data_dir, str(category))
        
        # Percorre todas as imagens dentro do subdiretório da categoria
        for filename in os.listdir(category_path):
            img_path = os.path.join(category_path, filename)
            
            # Carrega a imagem usando OpenCV
            img = cv2.imread(img_path)
            
            # Redimensiona a imagem para o tamanho padrão (30x30)
            img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
            
            # Adiciona a imagem e seu rótulo às listas
            images.append(img)
            labels.append(category)
    
    return images, labels


def get_model():
    """
    Cria e retorna um modelo de rede neural para classificar sinais de trânsito.
    
    Retorna:
        tf.keras.models.Model: Modelo compilado pronto para treinamento.
    """
    model = tf.keras.models.Sequential([
        # Primeira camada convolucional
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', 
                               input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        
        # Segunda camada convolucional
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        
        # Flatten para converter a matriz em vetor
        tf.keras.layers.Flatten(),
        
        # Camada totalmente conectada
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),  # Dropout para evitar overfitting
        
        # Camada de saída com NUM_CATEGORIES neurônios (um para cada categoria)
        tf.keras.layers.Dense(NUM_CATEGORIES, activation='softmax')
    ])
    
    # Compila o modelo usando a função de perda categórica e o otimizador Adam
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model