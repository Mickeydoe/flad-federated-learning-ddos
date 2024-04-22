import os
import numpy as np
import h5py
import glob
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

def load_dataset(path):
    dataset = h5py.File(path, "r")
    set_x_orig = np.array(dataset["set_x"][:])  # features
    set_y_orig = np.array(dataset["set_y"][:])  # labels
    return set_x_orig, set_y_orig

def preprocess_data(X, max_len=100):
    tokenizer = Tokenizer(num_words=5000, lower=True, oov_token="<UNK>")
    tokenizer.fit_on_texts(X)
    sequences = tokenizer.texts_to_sequences(X)
    X_processed = pad_sequences(sequences, maxlen=max_len, padding='post')
    return X_processed

def load_and_preprocess_data(folder_path, set_type, seed):
    files = glob.glob(folder_path + "/*" + '-' + set_type + '.hdf5')
    set_list = []
    for file in files:
        X, Y = load_dataset(file)
        X = preprocess_data(X)
        set_list.append((X, Y))
    
    # Concatenate all the training and validation sets
    X = np.concatenate([pair[0] for pair in set_list], axis=0)
    Y = np.concatenate([pair[1] for pair in set_list], axis=0)
    
    # Shuffle the data
    np.random.seed(seed)
    indices = np.arange(X.shape[0])
    np.random.shuffle(indices)
    X = X[indices]
    Y = Y[indices]
    
    return X, Y
