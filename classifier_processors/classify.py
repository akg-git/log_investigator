'''This module contains functions for classifying log messages.'''

import os

from classifier_processors.processor_regex import regex_classify_log
from classifier_processors.processor_bert import bert_classify_log
from classifier_processors.processor_llm import llm_classify_log


# The classify function takes a list of log messages and returns a classified label for each log.
def classify(logs):
    labels = []
    for source, log in logs:
        label = classify_log(source,log)
        labels.append((source, log, label))
    return labels

# The classify_log function takes a single log message and returns a classified label for that log.
def classify_log(source,log):

    if source == "LegacyCRM":
        label = llm_classify_log(log)

    else: 
        regex_pattern = regex_classify_log(log)

        if regex_pattern is None:
            label = bert_classify_log(log)
        else:
            label = regex_pattern

    return label

def classify_csv_input(input_csv_file):
    import pandas as pd

    df = pd.read_csv(input_csv_file)
    csv_logs = list(zip(df['source'], df['log_message']))

    # Extract the label from the tuple
    df["target_label"] = [label for _, _, label in classify(csv_logs)]

    output_file = input_csv_file.replace(".csv", "_classified_output.csv")
    df.to_csv(output_file, index=False)
    print(f"Classified logs saved to {output_file}")

if __name__ == "__main__":

    input_csv_file = "./resources/test_split.csv"

    try:
        if not os.path.isfile(input_csv_file):
            raise FileNotFoundError(f"Input CSV file '{input_csv_file}' not found.")
        classify_csv_input(input_csv_file)
    except FileNotFoundError as fnfe:
        print(fnfe)
    except Exception as e:
        print(f"An error occurred: {e}")

    # Example
    # logs = [
    #     ("ModernCRM", "File data_20231010.csv uploaded successfully by user User123."),
    #     ("ModernCRM", "Account with ID 5351 created by User634."),
    #     ("ModernCRM", "User User685 logged out."),
    #     ("ModernCRM", "Backup started at 2025-05-14 07:06:55."),
    #     ("ModernCRM", "Backup completed successfully."),
    #     ("ModernCRM", "  Backup ended at 2025-08-08 13:06:23."),
    #     ("ModernCRM", "System updated to version 2.5.1"),
    #     ("ModernCRM", "System reboot initiated by user User789."),
    #     ("ModernCRM", "Disk cleanup completed successfully."),
    #     ("LegacyCRM","Legacy sync completed for account 4492"),
    #     ("AnalyticsEngine","Unauthorized access to data was attempted"),
    #     ("ModernHR","Shard 6 replication task ended in failure"),
    #     ("ThirdPartyAPI","Multiple bad login attempts detected on user 8538 account"),
    #     ("LegacyCRM","Lead conversion failed for prospect ID 7842 due to missing contact information."),
    #     ("LegacyCRM","API endpoint 'getCustomerDetails' is deprecated and will be removed in version 3.2. Use 'fetchCustomerInfo' instead."),
    #     ("LegacyCRM","Customer follow-up process for lead ID 5621 failed due to missing next action"),
    #     ("LegacyCRM", "Support for legacy authentication methods will be discontinued after 2025-06-01."),
    #     ("LegacyCRM", "Task assignment for TeamID 3425 could not complete due to invalid priority level.")
    # ]

    # classified_output = classify(logs)

    # for source, log, label in classified_output:
    #     print(f"Source: {source}\nLog Message: {log}\nClassified Label: {label}\n{'-'*50}")
