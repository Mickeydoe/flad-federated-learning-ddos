import argparse
from flad_training import FederatedTrain
import os
import sys

def main(argv):
    parser = argparse.ArgumentParser(description='Adaptive Federated Learning for Phishing Detection')
    
    parser.add_argument('-d', '--dataset', type=str, required=True, help='Path to the phishing dataset')
    parser.add_argument('-m', '--model', type=str, default="mlp", choices=['mlp', 'cnn'], help='Type of model to use (mlp or cnn)')
    parser.add_argument('-e', '--epochs', type=int, default=10, help='Number of training epochs')
    parser.add_argument('-b', '--batch_size', type=int, default=32, help='Batch size for training')
    parser.add_argument('-s', '--steps_per_epoch', type=int, help='Number of steps per epoch')
    parser.add_argument('-lr', '--learning_rate', type=float, default=0.01, help='Learning rate')
    parser.add_argument('-o', '--output', type=str, default='./output', help='Output directory for results')

    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    # Load and preprocess the dataset
    X_train, Y_train, X_val, Y_val = load_and_preprocess_data(args.dataset, 'train', seed=42)

    # Initialize clients
    clients = init_clients(X_train, Y_train, X_val, Y_val)

    # Start federated training
    FederatedTrain(clients, args.model, args.output, args.epochs, args.steps_per_epoch, learning_rate=args.learning_rate, batch_size=args.batch_size)

if __name__ == '__main__':
    main(sys.argv[1:])
