import imaplib
import email
import re

# Email account credentials
IMAP_SERVER = 'imap.gmail.com'
EMAIL_ACCOUNT = input("Enter your email address: ")
EMAIL_PASSWORD = input("Enter your email password: ")

# Regular expressions for detecting suspicious URLs and email patterns
suspicious_url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
ip_url_pattern = r'http[s]?://(?:\d{1,3}\.){3}\d{1,3}'
suspicious_email_pattern = r'.*@.*\..*'

# Connect to the email server
def connect_to_email():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select("inbox")
        return mail
    except Exception as e:
        print(f"Error connecting to email: {e}")
        return None

# Fetch unread emails
def fetch_unread_emails(mail):
    status, messages = mail.search(None, '(UNSEEN)')
    if status != "OK":
        print("No new emails found!")
        return []
    return messages[0].split()

# Analyze an email for phishing signs
def analyze_email(raw_email):
    msg = email.message_from_bytes(raw_email)

    # Extract email metadata
    sender = msg["From"]
    subject = msg["Subject"]
    print(f"\nAnalyzing Email from: {sender} | Subject: {subject}")

    # Check for suspicious email addresses
    match = re.match(suspicious_email_pattern, sender)
    if match and re.search(ip_url_pattern, sender):
        print(f"Suspicious sender detected: {sender}")
    
    # Extract and analyze the email body
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                email_body = part.get_payload(decode=True).decode()
                check_phishing_signs(email_body)
    else:
        email_body = msg.get_payload(decode=True).decode()
        check_phishing_signs(email_body)

# Check for phishing signs in the email body
def check_phishing_signs(email_body):
    urls = re.findall(suspicious_url_pattern, email_body)

    if not urls:
        print("No URLs found in email.")
    else:
        for url in urls:
            # Check if URL contains an IP address
            if re.match(ip_url_pattern, url):
                print(f"Suspicious URL detected (IP-based): {url}")
            else:
                print(f"URL found: {url}")

    # Example basic phishing indicators
    phishing_indicators = ["account", "login", "password", "urgent", "verify"]
    if any(indicator in email_body.lower() for indicator in phishing_indicators):
        print("Potential phishing content detected!")

# Main function to run the email detector
def main():
    mail = connect_to_email()
    if not mail:
        return

    unread_email_ids = fetch_unread_emails(mail)
    if not unread_email_ids:
        print("No unread emails to scan!")
        return

    # Loop through unread emails and analyze them
    for email_id in unread_email_ids:
        status, raw_email = mail.fetch(email_id, '(RFC822)')
        raw_email_bytes = raw_email[0][1]
        analyze_email(raw_email_bytes)

    mail.logout()

if __name__ == "__main__":
    main()
