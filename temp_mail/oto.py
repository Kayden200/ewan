import random
import string
import time
from colorama import Fore, init
import asyncio
from temp_mail.async_temp_mail import AsyncTempMa>

init(autoreset=True)

# Facebook Sign-up URL
FB_SIGNUP_URL = "https://m.facebook.com/reg"

# List of random names and surnames
first_names = ["Hiroshi", "Matteo", "Ivan", "Pier>
               "Sofia", "Elena", "Nia", "Viktor",>
               "Klara", "Júlia", "Katya", "Farhan>

last_names = ["Nakamura", "Rossi", "Petrov", "Dub>
              "Müller", "Ibrahim", "Schmidt", "Fe>
              "Aliyev", "Huber", "Martins", "Pere>

# Generate a random password
def generate_password():
    return ''.join(random.choices(string.ascii_le>

# Generate a random birthday
def generate_birthday():
    day = random.randint(1, 28)
    month = random.randint(1, 12)
    year = random.randint(1985, 2002)
    return str(day), str(month), str(year)

# Fetch OTP from TempMail inbox
async def get_email_otp(mailbox_id, token):
    async with AsyncTempMail() as temp_mail:
        # Fetch all emails from the mailbox
        filtered_emails = await temp_mail.fetch_a>
        for email in filtered_emails:
            if "Facebook" in email.subject:
                otp = ''.join(filter(str.isdigit,>
                print(Fore.YELLOW + f"[+] OTP Rec>
                return otp
        return None
# Create Facebook account
async def create_facebook_account():
    async with AsyncTempMail() as temp_mail:
        # Step 1: Get a temporary email address a>
        response_json = await temp_mail.fetch_new>
        email = response_json["mailbox"]
        token = response_json["token"]

        print(Fore.GREEN + f"[+] Generated Email:>

        # Step 2: Generate Facebook account detai>
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        password = generate_password()
        day, month, year = generate_birthday()

        # Step 3: Create Facebook account (simula>
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

        response = session.post(FB_SIGNUP_URL, da>

        if "checkpoint" in response.url:
            print(Fore.RED + "[!] Facebook detect>
            return None

        # Step 4: Fetch OTP from TempMail inbox
        otp = await get_email_otp(response_json[">
        if otp:
            print(Fore.GREEN + f"Account Created >
            print(Fore.GREEN + f"Name: {first_nam>
            print(Fore.GREEN + f"Email: {email}")
            print(Fore.GREEN + f"Password: {passw>
            print(Fore.GREEN + f"OTP: {otp}")
            return {
                "name": f"{first_name} {last_name>
                "email": email,
                "password": password,
                "otp": otp
            }

        print(Fore.RED + "[!] Failed to retrieve >
        return None

# Main function to create multiple accounts
async def main():
    num_accounts = int(input("Enter the number of>

    with open("accounts.txt", "a") as file:
        for _ in range(num_accounts):
            account = await create_facebook_accou>
            if account:
                # Save the account details (name,>
                file.write(f"Name: {account['name>

                print(Fore.GREEN + "[+] All accounts save>

if __name__ == "__main__":
    asyncio.run(main())
        
