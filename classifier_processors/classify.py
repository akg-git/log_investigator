''' This module contains functions for classifying log messages using regular expressions.'''

from processor_regex import regex_classify_log


# The classify function takes a list of log messages and returns a classified label for each log.
def classify(logs):
    labels = []
    for source, log in logs:
        label = classify_log(source,log)
        labels.append((source, log, label))
    return labels

# The classify_log function takes a single log message and returns a classified label for that log.
def classify_log(source,log):

    if source is "LegacyCRM":
        pass # LLM

    else: 
        label = regex_classify_log(log)

        if label is None:
            pass # BERT

        return label

if __name__ == "__main__":
    # Example
    logs = [
        ("ModernCRM", "File data_20231010.csv uploaded successfully by user User123."),
        ("ModernCRM", "Account with ID 5351 created by User634."),
        ("ModernCRM", "User User685 logged out."),
        ("ModernCRM", "Backup started at 2025-05-14 07:06:55."),
        ("ModernCRM", "Backup completed successfully."),
        ("ModernCRM", "  Backup ended at 2025-08-08 13:06:23."),
        ("ModernCRM", "System updated to version 2.5.1"),
        ("ModernCRM", "System reboot initiated by user User789."),
        ("ModernCRM", "Disk cleanup completed successfully."),
        ("LegacyCRM","Legacy sync completed for account 4492"),
        ("AnalyticsEngine","Unauthorized access to data was attempted"),
        ("ModernHR","Shard 6 replication task ended in failure"),
        ("ThirdPartyAPI","Multiple bad login attempts detected on user 8538 account")
    ]

