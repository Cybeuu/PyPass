


# PyWarden



**Video Demo**: https://youtu.be/VBjkHbTQSIg



### Description:

PyWarden is an password manager, developed as the CS50P Final Project, focused on enhancing password security through encryption. Its user-friendly interface enables easy password management while ensuring robust protection against unauthorized access. Features include secure password storage, login, password retrieval with authorized keys, and password strength assessment to guard against leaks or compromises. Please note that PyWarden is a project and not intended for actual password storage.





## Features:



- Implement password storage with encryption for enhanced security.

- Enable account login with secure password management.

- Facilitate password retrieval using an authorized key.

- Assess password strength to ensure robust protection.

- Verify if a password has been compromised or leaked.



## Libraries Required:



1. Cryptography: for data encryption such as emails and passwords.

2. passpwnedcheck 2.0.0: To check if a user's password has been leaked and how many times.



## Instructions:





### Clone the Project:



```bash

git clone  https://link-to-project

```

### Go to project directory

``` bash

cd my-project

```

### Install Dependencies

```bash

pip install  -r  requirements.txt

```

### Run the program

```bash

python project.py

```



**Note**: Always be cautious about the security of your passwords and sensitive information. Use reliable and trusted password managers for real-world applications.


## Documentation
### Functions ( excluding main )

``` python
def create_account():

username = input("Create username: ")

password = getpass.getpass("Create password: ")

key = getpass.getpass("Enter key for password retrieval: ")
```
#### Prompt the user to input a username, password, and a key. The key is used to safely store and retrieve the password. Both the password and the key are encrypted using the Fernet algorithm from the cryptography library. The encrypted details are then stored in a CSV file for future reference



```python
def login():

username = input("Enter Username: ")

password = getpass.getpass("Enter Password: ")
```
#### Allows the user to log in with their username and password. This function serves as a testing mechanism to verify the encryption and decryption process, but is kept for future use possibilities.

```python
def make_passwords(n_password=1, password_len=8):

chars = "0123456789abcdefghijklmnpqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-#@"

password_list = []
```
#### Generates random passwords using the characters provided in the 'chars' string. Note that while the generated passwords cannot be easily guessed, their randomness may not always guarantee the strongest security.

```python
def check_password(passwrd):
	pass_checker = PassChecker()
	...
```
#### Checks if the user-inputted password has been leaked or compromised. This function uses a database from an external library that is periodically updated to perform the verification.



```python
def get_password():

username = input("Enter Username: ")

key = getpass.getpass("Enter Key: ")
```

#### Enables the user to retrieve their password using their designated key.


```python
def password_strength(password):

score = 0  # ヽ(✿ﾟ▽ﾟ)ノ good , (っ °Д °;)っ BAD

improvments = []
```
#### Allows the user to input their password, and the program evaluates the strength of the password using eight different criteria. The function returns a final score and provides suggestions for password improvements.
