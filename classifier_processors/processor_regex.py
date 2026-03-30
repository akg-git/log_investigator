'''
This module contains functions for classifying log messages using regular expressions.
The regex_classify_log function takes a log message as input and checks it against predefined regex patterns to classify the log message into several categories 
'''

#Regex Classification
import re

def regex_classify_log(log_message):
    # Define regex patterns for different log types
    regex_patterns = {
        'System Notification': [
            r'(File data_\d+.csv uploaded successfully by use...)',
            r'(Backup completed successfully.)',
            r'(System updated to version [\d\.]+)',
            r'(System reboot initiated by user User\d+.)',
            r'(\s*Backup (started|ended) at [\d\s\-\:]*)',
            r'(Disk cleanup completed successfully.)'
        ],
        'User Action': [
            r'(Account with ID \d+ created by User\d+.)',
            r'(\s*User\s+User\d+\s+logged\s(in|out))'
        ]
    }

    # Check log message against regex patterns and identify log type
    for label, patterns in regex_patterns.items():
        for pattern in patterns:
            if re.search(pattern, log_message, re.IGNORECASE):
                return label
    return None #'No regex pattern matched'

if __name__ == "__main__":
    # Example usage
    log_message1 = "File data_20231010.csv uploaded successfully by user User123."
    log_message2 = "Account with ID 5351 created by User634."
    log_message3 = "User User685 logged out."
    log_message4 = "Backup started at 2025-05-14 07:06:55."
    log_message5 = "Backup completed successfully."
    log_message6 = "  Backup ended at 2025-08-08 13:06:23."
    log_message7 = "System updated to version 2.5.1"
    log_message8 = "System reboot initiated by user User789."
    log_message9 = "Disk cleanup completed successfully."
    
    log_type = regex_classify_log(log_message6)
    print(f"Classified Log Type: {log_type}")