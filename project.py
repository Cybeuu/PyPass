import random
from cryptography.fernet import Fernet
from passpwnedcheck.pass_checker import PassChecker
import getpass
import sys
import csv

# list which will store the passwords with encryption
password_manager = {}

# ANSI escape codes for terminal
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"


def main():
    while True:
        choice = input(F""" {GREEN}
╔════════╦═════════════════════════════════╗
║ Option ║         Description             ║
╠════════╬═════════════════════════════════╣
║   1    ║ Create a new account            ║
║════════║═════════════════════════════════║
║   2    ║ Log in to an existing account   ║
║════════║═════════════════════════════════║
║   3    ║ Retrieve password (key required)║
║════════║═════════════════════════════════║
║   4    ║ Generate a new password         ║
║════════║═════════════════════════════════║
║   5    ║ Check if a password is leaked   ║
║════════║═════════════════════════════════║
║   6    ║ Evaluate password strength      ║
║════════║═════════════════════════════════║
║   0    ║ Exit the application            ║
╚════════╩═════════════════════════════════╝


{RESET}Enter Choice: """)
        if choice == "1":
            create_account()
        elif choice == "2":
            login()
        elif choice == "3":
            get_password()
        elif choice == "4":
            Count = int(input("How many password do you need? "))
            Length = int(input("Length of password: "))
            print(f"{GREEN}{make_passwords(Count, Length)}{RESET}")
        elif choice == "5":
            print(check_password(input("Enter Your Password: ")))
        elif choice == "6":
            password = input("Enter a password: ")
            strength = password_strength(password)
            if int(strength[0]) >= 5:
                print(f""" {BLUE}
                ╔═══════════════════════════════════════╗
                ║ The strength of the password is: {strength[0]}/8 ║
                ╚═══════════════════════════════════════╝
{RESET}""")
                print("TESTING")  # just adding an extra new line
            for comment in strength[1]:
                print(f"{comment}")
        elif choice == "0":
            sys.exit()
        else:
            print(f"{RED}Invalid choice{RESET}")


# create an account
def create_account():
    username = input("Create username: ")
    password = getpass.getpass("Create password: ")
    key = getpass.getpass("Enter key for password retrieval: ")

    fernet_key = Fernet.generate_key()
    cipher_suite = Fernet(fernet_key)
    encrypted_password = cipher_suite.encrypt(password.encode()).decode()
    encrypted_key = cipher_suite.encrypt(key.encode()).decode()     # encrypted password

    password_manager[username] = {
        'password': encrypted_password,
        'key': encrypted_key,
        'fernet_key': fernet_key
    }

    with open('passwords.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([username, encrypted_password, encrypted_key, fernet_key])

    print(f"✅ {GREEN} Account Created {RESET}")


# login to account
def login():
    username = input("Enter Username: ")
    password = getpass.getpass("Enter Password: ")

    if username in password_manager.keys():
        encrypted_password = password_manager[username]['password']
        key = password_manager[username]['key']
        fernet_key = password_manager[username]['fernet_key']

        cipher_suite = Fernet(fernet_key)
        decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()

        if decrypted_password == password:
            print(f"✅  {GREEN} Login Successful {RESET}")
        else:
            print(f"❌ {RED} Invalid password{RESET}")
    else:
        print(f"❌ {RED} Invalid username {RESET}")


# password generator
def make_passwords(n_password=1, password_len=8):
    chars = "0123456789abcdefghijklmnpqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-#@"
    password_list = []
    for _ in range(n_password):
        password = ''
        for _ in range(password_len):
            password += random.choice(chars)
        password_list.append(password)
    return password_list


# check if password has been leaked
def check_password(passwrd):

    pass_checker = PassChecker()

    password = f'{passwrd}'
    is_leaked, count = pass_checker.is_password_compromised(password)

    if is_leaked:
        return(f'{RED}Your password has been leaked {count} times{RESET}')
    else:
        return(f'{GREEN}Your password has not been leaked (yet){RESET}')


# get password using key
def get_password():
    username = input("Enter Username: ")
    key = getpass.getpass("Enter Key: ")
    try:
        fernet_key = password_manager[username]['fernet_key']
        cipher_suite = Fernet(fernet_key)
    except KeyError:
        print(f"❌{RED} Invalid username or key {RESET}")
    if username in password_manager.keys() and cipher_suite.decrypt(password_manager[username]['key'].encode()).decode() == key:
        encrypted_password = password_manager[username]['password']
        decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()

        print(f"{GREEN}Password for {username}: {decrypted_password}{RESET}")
    else:
        print(f"❌{RED} Invalid username or key {RESET}")


def password_strength(password):
    score = 0                            # ヽ(✿ﾟ▽ﾟ)ノ good , (っ °Д °;)っ BAD
    improvments = []
    # Check password length
    if len(password) >= 8:
        score += 1
        improvments.append(f"{GREEN}ヽ(✿ﾟ▽ﾟ)ノ Length length is/more than 8 characters{RESET}")
    else:
        improvments.append(f"{RED}(っ °Д °;)っ Length less than 8{RESET}")

    # Check for uppercase letters
    if any(char.isupper() for char in password):
        score += 1
        improvments.append(f"{GREEN}ヽ(✿ﾟ▽ﾟ)ノ Uppercase letter found{RESET}")
    else:
        improvments.append(f"{RED}(っ °Д °;)っ No uppercase letters found{RESET}")

    # Check for lowercase letters
    if any(char.islower() for char in password):
        score += 1
        improvments.append(f"{GREEN}ヽ(✿ﾟ▽ﾟ)ノ Lower case found{RESET}")
    else:
        improvments.append(f"{RED}(っ °Д °;)っ No lowercase letters found{RESET}")

    # Check for digits
    if any(char.isdigit() for char in password):
        score += 1
        improvments.append(f"{GREEN}ヽ(✿ﾟ▽ﾟ)ノ  Digits found{RESET}")
    else:
        improvments.append(f"{RED}(っ °Д °;)っ No digits found{RESET} ")

    # Check for special characters
    if any(char in "!@#$%^&*()-_=+{}[]|:;<>,.?/~`" for char in password):
        score += 1
        improvments.append(f"{GREEN}ヽ(✿ﾟ▽ﾟ)ノ No special characters {RESET}")
    else:
        improvments.append(f"{RED}(っ °Д °;)っ Spcecial characters not found{RESET}")

    # Check for repeated characters
    unique_chars = set(password)
    if len(unique_chars) == len(password):
        score += 1
        improvments.append(f"{GREEN}ヽ(✿ﾟ▽ﾟ)ノ No repeated characters {RESET}")
    else:
        improvments.append(f"{RED}(っ °Д °;)っ Repeated characters present{RESET}")

    # Check for sequential characters
    sequential_chars = "abcdefghijklmnopqrstuvwxyz0123456789" # sequential characters for lowercase and digits

    if not any(seq in password.lower() for seq in [sequential_chars[i:i+4] for i in range(len(sequential_chars) - 3)]):
        score += 1
        improvments.append(f"{GREEN}ヽ(✿ﾟ▽ﾟ)ノ No sequential characters present{RESET} ")
    else:
        improvments.append(f"{RED}(っ °Д °;)っ Sequential characters present{RESET}")


    # Check for common passwords
    common_password = [
    "123456", "password", "123456789", "12345678", "12345",
    "1234567", "1234567", "1234567890", "qwerty", "abc123",
    "111111", "123123", "admin", "letmein", "welcome",
    "monkey", "password1", "1234", "sunshine", "superman",
    "iloveyou", "princess", "12345678910", "123", "dragon",
    "123456a", "123456789a", "football", "123456789a", "baseball",
    "qwertyuiop", "123321", "654321", "123qwe", "qazwsx",
    "666666", "shadow", "123abc", "password123", "1234567890a",
    "qwerty123", "123654", "p@ssword", "passw0rd", "password!",
    "admin123", "welcome123", "123456789!", "password12", "qwerty1234",
    "password1234", "123456789a!", "1234567890!", "abcd1234", "123abc!",
    "passw0rd!", "password123!", "1234567890a!", "1234567890A", "q1w2e3r4",
    "qwertyuiop!", "iloveyou!", "princess123", "987654321", "qwerty123!",
    "1234567890A!", "qwertyuiop123", "password12345", "asdfghjkl", "qazwsxedc",
    "sunshine123", "superman123", "1234567890qw", "password!123", "admin!123",
    "welcome!123", "1234567890qwe", "1234567890!@#", "abcd1234!", "123abc!@#",
    "passw0rd!123", "password123!@#", "1234567890a!@#", "qwertyuiop!123", "iloveyou!123",
    "princess123!", "987654321!", "qwerty123!@#", "asdfghjkl!", "qazwsxedc!",
    "sunshine123!", "superman123!", "1234567890qw!", "password!1234", "admin!1234",
    "welcome!1234", "1234567890qwe!", "1234567890!@#$", "abcd1234!@", "123abc!@#$",
    "passw0rd!1234", "password123!@#$", "1234567890a!@#$", "qwertyuiop!1234", "iloveyou!1234",
    "princess123!@", "987654321!@", "qwerty123!@#$", "asdfghjkl!@", "qazwsxedc!@#$",
    "sunshine123!@", "superman123!@", "1234567890qw!@", "password!12345", "admin!12345",
    "welcome!12345", "1234567890qwe!@", "1234567890!@#$%", "abcd1234!@#", "123abc!@#$%",
    "passw0rd!12345", "password123!@#$%", "1234567890a!@#$%", "qwertyuiop!12345", "iloveyou!12345",
    "princess123!@%", "987654321!@%", "qwerty123!@#$%", "asdfghjkl!@%", "qazwsxedc!@#$%",
    "sunshine123!@%", "superman123!@%", "1234567890qw!@%", "password!123456", "admin!123456",
    "welcome!123456", "1234567890qwe!@#", "1234567890!@#$%^", "abcd1234!@#", "123abc!@#$%^",
    "passw0rd!123456", "password123!@#$%^", "1234567890a!@#$%^", "qwertyuiop!123456", "iloveyou!123456",
    "princess123!@%^", "987654321!@%^", "qwerty123!@#$%^", "asdfghjkl!@%^", "qazwsxedc!@#$%^",
    "sunshine123!@%^", "superman123!@%^", "1234567890qw!@%^", "password!1234567", "admin!1234567",
    "welcome!1234567", "1234567890qwe!@#$", "1234567890!@#$%^&", "abcd1234!@#", "123abc!@#$%^&",
    "passw0rd!1234567", "password123!@#$%^&", "1234567890a!@#$%^&", "qwertyuiop!1234567", "iloveyou!1234567",
    "princess123!@%^&", "987654321!@%^&", "qwerty123!@#$%^&", "asdfghjkl!@%^&", "qazwsxedc!@#$%^&",
    "sunshine123!@%^&", "superman123!@%^&", "1234567890qw!@%^&", "password!12345678", "admin!12345678",
    "welcome!12345678", "1234567890qwe!@#$%", "1234567890!@#$%^&*", "abcd1234!@#", "123abc!@#$%^&*",
    "passw0rd!12345678", "password123!@#$%^&*", "1234567890a!@#$%^&*", "qwertyuiop!12345678", "iloveyou!12345678",
    "princess123!@%^&*", "987654321!@%^&*", "qwerty123!@#$%^&*", "asdfghjkl!@%^&*", "qazwsxedc!@#$%^&*",
    "sunshine123!@%^&*", "superman123!@%^&*", "1234567890qw!@%^&*", "password!123456789", "admin!123456789",
    "welcome!123456789", "1234567890qwe!@#$%^&", "1234567890!@#$%^&*()", "abcd1234!@#", "123abc!@#$%^&*()",
    "passw0rd!123456789", "password123!@#$%^&*()", "1234567890a!@#$%^&*()", "qwertyuiop!123456789", "iloveyou!123456789",
    "princess123!@%^&*()", "987654321!@%^&*()", "qwerty123!@#$%^&*()", "asdfghjkl!@%^&*()", "qazwsxedc!@#$%^&*()",
    "sunshine123!@%^&*()", "superman123!@%^&*()", "1234567890qw!@%^&*()", "password!1234567890", "admin!1234567890",
    "welcome!1234567890", "1234567890qwe!@#$%^&*", "1234567890!@#$%^&*()_+", "abcd1234!@#", "123abc"]

    if password.lower() not in common_password:
        score += 1
        improvments.append(f"{GREEN}ヽ(✿ﾟ▽ﾟ)ノ Password Unique {RESET}")
    else:
        improvments.append(f"{RED}(っ °Д °;)っ Common password found! {RESET}")
    # Assign a score from 1 to 10 based on the total score
    password_strength = min(score, 8)

    return password_strength, improvments


if __name__ == "__main__":
    main()
