import random
import string
import requests
import asyncio
from colorama import Fore, init
import json
import time

# Initialize Colorama for colored terminal output
init(autoreset=True)

# Facebook Sign-up URL
FB_SIGNUP_URL = "https://m.facebook.com/reg"

# List of random first names and last names for account creation
first_names = ["Hiroshi", "Matteo", "Ivan", "Pierre", "Ahmed", "Fatima", "Aisha", "Yuki", "Carlos", "Dimitri", 
               "Sofia", "Elena", "Nia", "Viktor", "Lars", "Hana", "Leila", "Miguel", "Amira", "Arvid", "Mikhail", 
               "Klara", "Júlia", "Katya", "Farhan"]

last_names = ["Nakamura", "Rossi", "Petrov", "Dubois", "El-Sayed", "Oliveira", "Takahashi", "García", "Novak", 
              "Müller", "Ibrahim", "Schmidt", "Fernández", "Jovanović", "Weber", "Sato", "Wang", "Lopez", "Kovács", 
              "Aliyev", "Huber", "Martins", "Pereira", "Moretti", "Sorokin"]

# Generate a random password
def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

# Generate a random birthday
def generate_birthday():
    day = random.randint(1, 28)
    month = random.randint(1, 12)
    year = random.randint(1985, 2002)
    return str(day), str(month), str(year)

# Fetch OTP from TempMail inbox
async def get_email_otp(email, token):
    url = f"https://api.mail.tm/v1/mailbox/{email}/messages"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        emails = response.json()
        for email in emails:
            if "Facebook" in email['subject']:
                otp = ''.join(filter(str.isdigit, email['text_body']))  # Extract OTP from the email body
                if otp:
                    print(Fore.YELLOW + f"[+] OTP Received: {otp}")
                    return otp
    else:
        print(Fore.RED + "[!] Failed to fetch emails from TempMail.")
    return None

# Create Facebook account using TempMail generated email
async def create_facebook_account(token):
    # Step 1: Generate temporary email using Temp-Mail API
    url = "https://api.mail.tm/v1/email/new"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        email_data = response.json()
        email = email_data['mailbox']
        print(Fore.GREEN + f"[+] Generated Email: {email}")
        
        # Step 2: Generate random Facebook account details
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        password = generate_password()
        day, month, year = generate_birthday()

        # Step 3: Create Facebook account (simulate form submission)
        session = requests.Session()
        data = {
            "firstname": first_name,
            "lastname": last_name,
            "reg_email__": email,
            "reg_passwd__": password,
            "sex": "2",  # Male as default
            "birthday_day": day,
            "birthday_month": month,
            "birthday_year": year,
            "submit": "Sign Up"
        }

        response = session.post(FB_SIGNUP_URL, data=data)
        
        if "checkpoint" in response.url:
            print(Fore.RED + "[!] Facebook detected suspicious activity.")
            return None

        # Step 4: Retrieve OTP from TempMail inbox
        otp = await get_email_otp(email, token)
        if otp:
            print(Fore.GREEN + f"Account Created Successfully!")
            print(Fore.GREEN + f"Name: {first_name} {last_name}")
            print(Fore.GREEN + f"Email: {email}")
            print(Fore.GREEN + f"Password: {password}")
            print(Fore.GREEN + f"OTP: {otp}")
            return {
                "name": f"{first_name} {last_name}",
                "email": email,
                "password": password,
                "otp": otp
            }

        print(Fore.RED + "[!] Failed to retrieve OTP.")
        return None

# Main function to create multiple accounts
async def main():
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE3NDIwMDE2MzMsInJvbGVzIjpbIlJPTEVfVVNFUiJdLCJhZGRyZXNzIjoicnlsZUBpbmRpZ29ib29rLmNvbSIsImlkIjoiNjdkNGQyZWU2N2ZmNjk1NmUyMGE4MzI0IiwibWVyY3VyZSI6eyJzdWJzY3JpYmUiOlsiL2FjY291bnRzLzY3ZDRkMmVlNjdmZjY5NTZlMjBhODMyNCJdfX0.wT6o8TvZfcyqA1qriu6YteVtNf4tRQyj0hojBIFvlpYKD5gRk_ACcfvwIy1z-u1Qx-xIVLTl1O6ALaso7d651A"  # Replace with the Bearer token from Mail.tm
    
    num_accounts = int(input("Enter the number of accounts to create: "))
    
    with open("accounts.txt", "a") as file:
        for _ in range(num_accounts):
            account = await create_facebook_account(token)
            if account:
                # Save the account details (name, email, password, OTP) to a file
                file.write(f"Name: {account['name']} | Email: {account['email']} | Password: {account['password']} | OTP: {account['otp']}\n")
        
        print(Fore.GREEN + "[+] All accounts saved in accounts.txt")

if __name__ == "__main__":
    asyncio.run(main())
