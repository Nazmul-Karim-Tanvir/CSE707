# -*- coding: utf-8 -*-
"""CSE707_finalCode_Group5_23166011

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1B60jMpZMAbJL5V6IiaPvOXjuZN-9xhvp
"""

from google.colab import drive
drive.mount('/content/drive')

import os

# Replace 'your-folder-path' with the actual path to your dataset in Google Drive
dataset_path = '/content/drive/My Drive/creditcard.csv'

import pandas as pd

# Load the dataset
df_fraud = pd.read_csv(dataset_path)

# Display the first few rows to ensure it loaded correctly
df_fraud.head()

# Filter relevant columns and preprocess
df_fraud = df_fraud[['Time', 'V1', 'V2', 'V3', 'Amount', 'Class']]
df_fraud.columns = ['Timestamp', 'Feature1', 'Feature2', 'Feature3', 'Amount', 'IsFraud']

# Sample a smaller dataset for the simulation
df_sample_fraud = df_fraud.sample(1000, random_state=42)
df_sample_fraud.reset_index(drop=True, inplace=True)

# Display the distribution to understand the imbalance
print(df_sample_fraud['IsFraud'].value_counts())

df_sample_fraud.head()

import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

class FinanceApp:
    def __init__(self):
        self.blockchain = Blockchain()

    def add_transaction(self, timestamp, feature1, feature2, feature3, amount, is_fraud):
        transaction = {
            "timestamp": timestamp,
            "feature1": feature1,
            "feature2": feature2,
            "feature3": feature3,
            "amount": amount,
            "is_fraud": is_fraud
        }
        self.blockchain.add_block(Block(len(self.blockchain.chain), "", transaction['timestamp'], transaction))
        print(f"Transaction added to the blockchain: Fraud = {is_fraud}")

    def display_chain(self):
        for block in self.blockchain.chain:
            print(f"Block {block.index}: {block.data} | Hash: {block.hash}")

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Initialize the finance app
app_fraud = FinanceApp()

# Limit the number of transactions to process (e.g., 100)
num_transactions = 100

# Add transactions to the blockchain
for i, row in df_sample_fraud.head(num_transactions).iterrows():
    app_fraud.add_transaction(row['Timestamp'], row['Feature1'], row['Feature2'], row['Feature3'], row['Amount'], row['IsFraud'])

# Display the blockchain (optional: comment out if output is too large)
# app_fraud.display_chain()

# Analyze the blockchain accuracy
y_true_fraud = [1 if block.data['is_fraud'] == 0 else 0 for block in app_fraud.blockchain.chain[1:]]  # True labels (1 if valid, 0 if tampered)
y_pred_fraud = [1 if block.hash == block.calculate_hash() else 0 for block in app_fraud.blockchain.chain[1:]]

# Calculate accuracy, precision, recall, and F1-score
accuracy_fraud = accuracy_score(y_true_fraud, y_pred_fraud)
precision_fraud = precision_score(y_true_fraud, y_pred_fraud)
recall_fraud = recall_score(y_true_fraud, y_pred_fraud)
f1_fraud = f1_score(y_true_fraud, y_pred_fraud)

# Display the results
print(f"Accuracy (Fraud Dataset): {accuracy_fraud:.2f}")
print(f"Precision (Fraud Dataset): {precision_fraud:.2f}")
print(f"Recall (Fraud Dataset): {recall_fraud:.2f}")
print(f"F1-Score (Fraud Dataset): {f1_fraud:.2f}")

import matplotlib.pyplot as plt

# Plot the metrics for the fraud dataset
metrics_fraud = ["Accuracy", "Precision", "Recall", "F1-Score"]
scores_fraud = [accuracy_fraud, precision_fraud, recall_fraud, f1_fraud]

plt.figure(figsize=(10, 6))
plt.bar(metrics_fraud, scores_fraud, color=['blue', 'green', 'red', 'purple'])
plt.ylim(0, 1)
plt.title('Blockchain Performance Metrics (Fraud Detection Data)')
plt.ylabel('Score')
plt.show()