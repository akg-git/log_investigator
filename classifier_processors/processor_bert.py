'''
This module contains functions for classifying log messages using BERT expressions.
The bert_classify_log function takes a log message as input and checks it against predefined BERT models to classify the log message into several categories 
'''

import joblib
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the sentence transformer model to create embeddings for log messages
model = SentenceTransformer('all-MiniLM-L6-v2')

# Use the saved model to classify the log message #A:\AI Learning\BeginnerProjects\LogInvestigatorProject\log_investigator\models\log_classifier.joblib
bert_classifier_model = joblib.load("models/log_classifier.joblib")

def _normalize_log_message(log_message):
    """Return the actual log text expected by the embedding model."""
    if isinstance(log_message, tuple):
        if len(log_message) >= 2:
            return log_message[1]
        if len(log_message) == 1:
            return log_message[0]

    if isinstance(log_message, list):
        if len(log_message) == 1:
            return log_message[0]
        return " ".join(str(part) for part in log_message)

    return log_message


def bert_classify_log(log_message):
    log_text = _normalize_log_message(log_message)

    # Create an embedding for the log message using the sentence transformer model
    log_embedding = model.encode(log_text)
    log_embedding = np.asarray(log_embedding).reshape(1, -1)

    # #predict the probability of each class
    # probabilities = bert_classifier_model.predict_proba(log_embedding)[0]
    # print(f"Log: {log_text}\nClass Probabilities: {probabilities}\n")

    
    #perform the classification using the BERT model using loaded model
    predicted_class = bert_classifier_model.predict(log_embedding)[0]
    
    return predicted_class

if __name__ == "__main__":
    # Example log message
    logs = [
        ("ModernCRM", "File data_20231010.csv uploaded successfully by user User123."),
        ("ModernCRM", "Account with ID 5351 created by User634."),
        ("AnalyticsEngine", "User User685 logged out."),
        ("ModernCRM", "Backup started at 2025-05-14 07:06:55."),
        ("AnalyticsEngine","Unauthorized access to data was attempted"),
        ("ModernHR","Shard 6 replication task ended in failure"),
        ("ThirdPartyAPI","Multiple bad login attempts detected on user 8538 account")
    ]

    for log in logs:
        label = bert_classify_log(log)
        print(f"Log: {log}\nClassified Label: {label}\n")
