import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from colorama import Fore, init

init(autoreset=True)

# List ng Random Names
FIRST_NAMES = ["Hiroshi", "Matteo", "Ivan", "Pierre", "Ahmed", "Fatima", "Aisha", "Yuki", "Carlos", "Dimitri", "Sofia", "Elena", "Nia"]
LAST_NAMES = ["Nakamura", "Rossi", "Petrov", "Dubois", "El-Sayed", "Oliveira", "Takahashi", "García", "Novak", "Müller"]

def get_temp_mail():
    try:
        domain = requests.get("https://api.mail.tm/domains").json()['hydra:member'][0]['domain']
        username = "".join(random.choices("abcdefghijklmnopqrstuvwxyz1234567890", k=8))
        email = f"{username}@{domain}"
        password = "TempPassword123!"
        requests.post("https://api.mail.tm/accounts", json={"address": email, "password": password})
        token = requests.post("https://api.mail.tm/token", json={"address": email, "password": password}).json()['token']
        return email, token
    except Exception as e:
        print(Fore.RED + f"[!] Mail.tm Error: {e}")
        return None, None

def setup_driver(proxy=None):
    options = webdriver.ChromeOptions()
    # Proxy format: "http://IP:PORT" or "http://user:pass@IP:PORT"
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')
    
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def run_bot():
    print(Fore.CYAN + "=== FB Account Creator (Upgraded) ===")
    
    # 1. User Input para sa Password
    user_password = input("Anong password ang gusto mong gamitin para sa lahat ng accounts? ")
    
    # 2. Proxy Input (Optional)
    use_proxy = input("Gagamit ka ba ng Proxy? (Format: IP:PORT o Enter kung wala): ")
    
    num_acc = int(input("Ilang accounts ang gagawin natin? "))

    for i in range(num_acc):
        print(Fore.YELLOW + f"\n[*] Starting Account #{i+1}...")
        
        email, token = get_temp_mail()
        if not email: continue
        
        driver = setup_driver(use_proxy if use_proxy else None)
        
        try:
            driver.get("https://m.facebook.com/reg")
            time.sleep(3)

            # Random Name Selection
            fname = random.choice(FIRST_NAMES)
            lname = random.choice(LAST_NAMES)

            print(Fore.GREEN + f"[+] Using Name: {fname} {lname}")
            print(Fore.GREEN + f"[+] Email: {email}")

            # Fill up form
            driver.find_element(By.NAME, "firstname").send_keys(fname)
            driver.find_element(By.NAME, "lastname").send_keys(lname)
            driver.find_element(By.NAME, "reg_email__").send_keys(email)
            driver.find_element(By.XPATH, f"//input[@value='{random.choice(['1', '2'])}']").click() # Random Sex
            
            # Birthday
            driver.find_element(By.NAME, "birthday_day").send_keys(str(random.randint(1, 28)))
            driver.find_element(By.NAME, "birthday_month").send_keys(random.choice(["Jan", "Feb", "Mar", "Apr", "May", "Jun"]))
            driver.find_element(By.NAME, "birthday_year").send_keys(str(random.randint(1990, 2000)))
            
            driver.find_element(By.NAME, "reg_passwd__").send_keys(user_password)
            
            time.sleep(2)
            driver.find_element(By.NAME, "submit").click()
            
            print(Fore.BLUE + "[*] Registration submitted. Waiting 40s for OTP...")
            time.sleep(40)

            # Check for OTP via Mail.tm API
            headers = {"Authorization": f"Bearer {token}"}
            msgs = requests.get("https://api.mail.tm/messages", headers=headers).json()
            
            if msgs['hydra:member']:
                otp_subject = msgs['hydra:member'][0]['subject']
                print(Fore.MAGENTA + f"[!] OTP RECEIVED: {otp_subject}")
                
                # Save to accounts.txt
                with open("accounts.txt", "a") as f:
                    f.write(f"Name: {fname} {lname} | Email: {email} | Pass: {user_password} | Subject: {otp_subject}\n")
            else:
                print(Fore.RED + "[!] No OTP found. Baka na-checkpoint ang IP.")

        except Exception as e:
            print(Fore.RED + f"[!] Error during process: {e}")
        finally:
            driver.quit()
            time.sleep(5) # Konting pahinga bago ang susunod na account

if __name__ == "__main__":
    run_bot()
