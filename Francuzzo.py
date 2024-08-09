import random
import re
import os
import hashlib
import datetime
import json
import threading
import time
from cryptography.fernet import Fernet
import shutil
from datetime import datetime
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
language = "it"
from personality import patterns_responses
try:
    from config import destinations, patterns
except:
    print("Modulo config mancante")
    input()
try:
    from orgunco import FileOrganizer
except:
    print("Modulo orgunco mancante")
try:
    from Interpreter import M_interpreter
except:
    print("Modulo Interpreter mancante")
try:
    from blockchain import Block
except:
    print("Modulo blockchain mancante")
###################ORGANIZER ADDON
CONFIG_FILE = 'config.py'

def log_action(action):
    log_folder = os.path.join(os.getcwd(), 'DPLOG')
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_file_path = os.path.join(log_folder, 'log.json')

    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'action': action
    }

    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as file:
            data = json.load(file)
    else:
        data = []

    data.append(log_entry)

    with open(log_file_path, 'w') as file:
        json.dump(data, file, indent=4)

def show_log():
    log_file_path = os.path.join(os.getcwd(), 'DPLOG', 'log.json')

    if not os.path.exists(log_file_path):
        print("No log found.")
        return

    with open(log_file_path, 'r') as file:
        data = json.load(file)

    if not data:
        print("The log is empty.")
        return

    for entry in data:
        print(f"{entry['timestamp']}: {entry['action']}")

def save_config_to_file():
    config_content = (
        f"destinations = {json.dumps(destinations, indent=4)}\n\n"
        f"patterns = {json.dumps(patterns, indent=4)}\n"
    )
    with open(CONFIG_FILE, 'w') as file:
        file.write(config_content)


def admenu():
    while True:
        print("1. Change language")
        print("2. View information")
        print("3. Modify settings")
        print("4. Modify patterns")
        print("5. Return to main Francuzzo")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()
        log_action(f"Admin menu choice: {choice}")

        if choice == '1':
            change_language()
        elif choice == '2':
            view_information()
        elif choice == '3':
            modify_settings()
        elif choice == '4':
            modify_patterns()
        elif choice == '5':
            francuzzo_chat()
        elif choice == '6':
            print("Exiting...")
            log_action("Admin exited")
            break
        else:
            print("Invalid option. Please choose a number between 1 and 6.")
            log_action("Invalid admin menu option")

def change_language():
    global language
    print("Available languages: it, en")
    new_language = input("Enter the new language: ").strip().lower()
    if new_language in ["it", "en"]:
        language = new_language
        print(f"Language changed to {language}")
        log_action(f"Language changed to {language}")
    else:
        print("Invalid language.")
        log_action("Attempted to change to invalid language")

def view_information():
    print("Displaying log:")
    show_log()

def modify_settings():
    global destinations
    print("Modifying destination settings:")
    for i, (folder, extensions) in enumerate(destinations.items(), start=1):
        print(f"{i}. {folder} - Extensions: {', '.join(extensions)}")

    print(f"{len(destinations) + 1}. Add a new folder")

    try:
        choice = int(input("Choose a folder to modify or add a new one (number): "))
        if 1 <= choice <= len(destinations):
            folder = list(destinations.keys())[choice - 1]
            print(f"Modifying extensions for {folder}")
            print(f"Current extensions: {', '.join(destinations[folder])}")
            new_extensions = input("Enter new extensions separated by commas (e.g., .pdf, .docx): ").strip().split(',')
            new_extensions = [ext.strip().lower() for ext in new_extensions]
            destinations[folder] = new_extensions
            print(f"Updated extensions for {folder}: {', '.join(destinations[folder])}")
            save_config_to_file()
            log_action(f"Updated extensions for folder '{folder}' to {', '.join(destinations[folder])}")
        elif choice == len(destinations) + 1:
            new_folder = input("Enter the name of the new folder: ").strip()
            new_extensions = input("Enter the extensions for the new folder separated by commas (e.g., .pdf, .docx): ").strip().split(',')
            new_extensions = [ext.strip().lower() for ext in new_extensions]
            destinations[new_folder] = new_extensions
            print(f"Added new folder '{new_folder}' with extensions: {', '.join(new_extensions)}")
            save_config_to_file()
            log_action(f"Added new folder '{new_folder}' with extensions: {', '.join(new_extensions)}")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. You must enter a number.")

def modify_patterns():
    global patterns
    print("Modifying name patterns:")
    for i, (pattern, folder) in enumerate(patterns.items(), start=1):
        print(f"{i}. Pattern: '{pattern}' -> Folder: '{folder}'")

    print(f"{len(patterns) + 1}. Add a new pattern")
    print(f"{len(patterns) + 2}. Remove an existing pattern")

    try:
        choice = int(input("Choose an option (number): "))
        if 1 <= choice <= len(patterns):
            pattern = list(patterns.keys())[choice - 1]
            print(f"Modifying folder for pattern '{pattern}'")
            new_folder = input(f"Enter new folder for pattern '{pattern}': ").strip()
            patterns[pattern] = new_folder
            print(f"Updated folder for pattern '{pattern}': {new_folder}")
            save_config_to_file()
            log_action(f"Updated folder for pattern '{pattern}' to {new_folder}")
        elif choice == len(patterns) + 1:
            new_pattern = input("Enter the new pattern: ").strip()
            new_folder = input("Enter the folder for the new pattern: ").strip()
            patterns[new_pattern] = new_folder
            print(f"Added new pattern '{new_pattern}' with folder: '{new_folder}'")
            save_config_to_file()
            log_action(f"Added new pattern '{new_pattern}' with folder: '{new_folder}'")
        elif choice == len(patterns) + 2:
            del_choice = int(input("Enter the number of the pattern to remove: "))
            if 1 <= del_choice <= len(patterns):
                del_pattern = list(patterns.keys())[del_choice - 1]
                del patterns[del_pattern]
                print(f"Removed pattern '{del_pattern}'")
                save_config_to_file()
                log_action(f"Removed pattern '{del_pattern}'")
            else:
                print("Invalid choice.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. You must enter a number.")

def menu(language="it"):
    if language == "it":
        print("Inserisci comandi o premi help per visualizzarli")
    elif language == "en":
        print("Enter commands or type 'help' to see commands")

    command = input("user: ")
    log_action(f"User command: {command}")

    if command == "exit":
        log_action("User exited")
        exit()
    elif command == "organize_by_ext":
        organizer = FileOrganizer()
        print(f"Source folder: {organizer.source_folder}")
        organizer.organize()
        menu(language)
    elif command == "organize_by_pattern":
        organizer = FileOrganizer()
        print(f"Source folder: {organizer.source_folder}")
        organizer.organize_by_name_pattern()
        menu(language)


    elif command == "franzuzzo":
        francuzzo_chat()
    elif command == "ritorna":
        francuzzo_chat()


    elif command == "admin":
        admin_password = input("Enter the password: ")
        log_action("Admin mode activated")
        if admin_password == "admin":
            print("Admin mode activated")
            admenu()
    elif command == "help":
        if language == "it":
            print("comandi disponibili: organize_by_ext (organizza in base all'estenzione dei file come .txt o .mp3), organize_by_pattern (organizza in base a parole chiave presenti nel nome ad esempio 2015), exit (termini il programma), franzuzzo (ricomincia la conversazione con Francuzzo)")
        elif language == "en":
            print("Available commands: organize, organize_by_pattern, exit")
        menu(language)
    else:
        if language == "it":
            print("Unrecognized command")
        elif language == "en":
            print("Unrecognized command")
        log_action("Unrecognized command")
        menu(language)

###################ORGANIZER ADDON
###################MAIN




# Funzione per ottenere una risposta in base al tag e al pattern
def get_response(user_input):
    user_input = user_input.lower()
    for item in patterns_responses:
        for pattern in item["patterns"]:
            if re.search(pattern, user_input):
                return random.choice(item["responses"])
    return "Mi dispiace, non ho capito."



###################BLOCKCHAIN
# Funzione per generare e salvare una nuova chiave crittografica in modo sicuro
def generate_key():
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    return key, cipher_suite

# Funzione per caricare la chiave crittografica
def load_key():
    try:
        with open('secret.key', 'rb') as key_file:
            key = key_file.read()
        return key
    except FileNotFoundError:
        # Se il file non esiste, genera una nuova chiave
        key, _ = generate_key()
        with open('secret.key', 'wb') as key_file:
            key_file.write(key)
        return key

# Carica la chiave crittografica al momento dell'esecuzione del programma
key = load_key()
cipher_suite = Fernet(key)




def save_blockchain(blockchain):
    blockchain_data = []
    for block in blockchain:
        block_data = {
            'index': block.index,
            'timestamp': str(block.timestamp),
            'data': block.data,
            'data_hash': block.data_hash,
            'previous_hash': block.previous_hash,
            'hash': block.hash
        }
        blockchain_data.append(block_data)

    json_data = json.dumps(blockchain_data, indent=4)
    encrypted_data = cipher_suite.encrypt(json_data.encode('utf-8'))

    with open('blockchain.json', 'wb') as file:
        file.write(encrypted_data)

def load_blockchain():
    try:
        with open('blockchain.json', 'rb') as file:
            encrypted_data = file.read()

        decrypted_data = cipher_suite.decrypt(encrypted_data).decode('utf-8')
        blockchain_data = json.loads(decrypted_data)

        blockchain = []
        for block_data in blockchain_data:
            block = Block(
                block_data['index'],
                datetime.datetime.strptime(block_data['timestamp'], '%Y-%m-%d %H:%M:%S.%f'),
                block_data['data'],
                block_data['previous_hash']
            )
            block.data_hash = block_data['data_hash']  # Restore data_hash from saved data
            block.hash = block_data['hash']  # Restore hash from saved data
            blockchain.append(block)

        return blockchain

    except FileNotFoundError:
        return []

def check_integrity(blockchain):
    for i in range(1, len(blockchain)):
        current_block = blockchain[i]
        previous_block = blockchain[i - 1]

        if current_block.previous_hash != previous_block.hash:
            return False

        if current_block.data_hash != current_block.hash_data():
            return False

        if current_block.hash != current_block.hash_block():
            return False

    return True

def recalculate_hashes_and_check(blockchain):
    for block in blockchain:
        if block.hash != block.hash_block():
            return False
    return True

blockchain = load_blockchain()
if not blockchain:
    blockchain = [Block.create_genesis()]

previous_block = blockchain[-1]

def add_block(data):
    global previous_block
    block_to_add = Block.next_block(previous_block, data)
    blockchain.append(block_to_add)
    previous_block = block_to_add
    if check_integrity(blockchain):
        print(f"Block #{block_to_add.index} has been added to the blockchain!")
    else:
        print("Blockchain integrity check failed.")

def display_blockchain():
    for block in blockchain:
        print(f"Index: {block.index}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Data: {block.data}")
        print(f"Data Hash: {block.data_hash}")
        print(f"Block Hash: {block.hash}")
        print("------------------")

def save_blockchain_cli():
    if check_integrity(blockchain):
        save_blockchain(blockchain)
        print("Blockchain saved to blockchain.json")
    else:
        print("Blockchain integrity check failed. Not saving the blockchain.")

def check_integrity_cli():
    if check_integrity(blockchain):
        print("Blockchain integrity verified. No errors found.")
    else:
        print("Blockchain integrity check failed.")

# Background integrity check function
def background_integrity_check():
    while True:
        time.sleep(60)  # Check every 60 seconds
        if not check_integrity(blockchain) or not recalculate_hashes_and_check(blockchain):
            print("Blockchain integrity check failed in background.")
            break

# Start background integrity check thread
integrity_check_thread = threading.Thread(target=background_integrity_check, daemon=True)
integrity_check_thread.start()

# Command-line interface
def blockchain_interface():
    while True:
        print("\nBlockchain CLI")
        print("1. Add Block")
        print("2. Display Blockchain")
        print("3. Save Blockchain")
        print("4. Check Blockchain Integrity")
        print("5. Return to main console")
        choice = input("Enter your choice: ")

        if choice == "1":
            data = input("Enter data for the new block: ")
            add_block(data)
            log_action(f"Added block with data: {data}")
        elif choice == "2":
            display_blockchain()
            log_action("Displayed blockchain")
        elif choice == "3":
            save_blockchain_cli()
            log_action("Blockchain saved")
        elif choice == "4":
            check_integrity_cli()
            log_action("Blockchain integrity checked")
        elif choice == "5":
            francuzzo_chat()
        else:
            print("Invalid choice. Please try again.")

###################BLOCKCHAIN
###################CRIPT
class Francuzzo_Cript:
    def __init__(self):
        self.backend = default_backend()

    def generate_key(self, password: str, salt: bytes) -> bytes:
        """Genera una chiave segreta a partire dalla password e dal sale usando PBKDF2HMAC."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # Fernet richiede una chiave di 32 byte
            salt=salt,
            iterations=100000,
            backend=self.backend
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def encrypt(self, message: str, password: str) -> bytes:
        """Cripta il messaggio utilizzando la password."""
        salt = os.urandom(16)  # Genera un sale casuale
        key = self.generate_key(password, salt)
        cipher = Fernet(key)
        encrypted_message = cipher.encrypt(message.encode())
        return salt + encrypted_message  # Prependere il sale al messaggio criptato

    def decrypt(self, encrypted_message: bytes, password: str) -> str:
        """Decripta il messaggio criptato utilizzando la password."""
        try:
            salt = encrypted_message[:16]  # Estrai il sale dal messaggio criptato
            encrypted_message = encrypted_message[16:]  # Rimuovi il sale dal messaggio criptato
            key = self.generate_key(password, salt)
            cipher = Fernet(key)
            decrypted_message = cipher.decrypt(encrypted_message)
            return decrypted_message.decode()
        except Exception as e:
            print(f"Errore durante la decriptazione: {e}")
            return None

    def save_encrypted_message(encrypted_message: bytes, filename="Encripted_Message"):
        """Salva il messaggio criptato su un file."""
        with open(filename, 'wb') as f:
            f.write(encrypted_message)

    def load_encrypted_message(self, filename: str) -> bytes:
        """Carica il messaggio criptato da un file."""
        with open(filename, 'rb') as f:
            return f.read()
###################CRIPT

# Funzione principale per gestire il chatbot
def francuzzo_chat():

    while True:
        user_input = input("Tu: ")
        if user_input == "help":
            print("Francuzzo: Ecco i comandi disponibili: \n exit (esci dal programma), help (vedi i comandi), organizer (apri menu organizzatore files), analisis (apri la console di analisi in cui puoi modificare il file di config ed accedere al log facilmente), interprete (interpreta i file.M o crea una cartella dove inserire i file .M da interpretare), blockdata (entra nella console di blockdata in cui puoi salvare dati statici in una blockchain immutabile e criptata), cript (cripta un messaggio), decript (decripta un messaggio criptato)")
            log_action("User command: help")
            francuzzo_chat()
        elif user_input == "analisis":
            admenu()
            log_action("ANALISIS MODE ACTIVATED")
            exit()


        elif user_input == "interprete":
            print("interprete attivato")
            log_action("INTERPRETER ACTIVATED")
            interpreter = M_interpreter()
            interpreter.process_files()
            francuzzo_chat()
        elif user_input == "organizer":
            print("Aperta console organizer")
            log_action("opened organizer console")
            menu()

        elif user_input == "cript":
            log_action("opened cript console")
            cript = Francuzzo_Cript()  # Create an instance of Francuzzo_Cript
            message_cript = input("Inserisci il messaggio da criptare: ")
            password_cript = input("Inserisci la password per criptare il messaggio: ")
            encrypted_message = cript.encrypt(message_cript, password_cript)  # Call encrypt on the instance
            print(f"Messaggio criptato: {encrypted_message}")  # Print the encrypted message
            if input("Vuoi salvare il messaggio criptato su un file? (s/n): ").lower:
                Francuzzo_Cript.save_encrypted_message(encrypted_message)
            else:
                francuzzo_chat()

        elif user_input == "decript":
            log_action("opened decript console")
            cript = Francuzzo_Cript()  # Create an instance of Francuzzo_Cript
            encrypted_message = input("Inserisci il messaggio criptato: ")
            password_decript = input("Inserisci la password per decriptare il messaggio: ")
            decrypted_message = cript.decrypt(encrypted_message, password_decript)  # Call decrypt on the instance
            if decrypted_message is not None:
                print(f"Messaggio decriptato: {decrypted_message}")  # Print the decrypted message
            else:
                print("Ritorno al menu principale")
            francuzzo_chat()

        elif user_input == "blockdata":
            blockchain_interface()

        elif user_input.lower() in ["exit", "quit", "esci"]:
            print("Francuzzo: Arrivederci! Speru di potervi servire ancora.")
            break
        response = get_response(user_input)
        print(f"Francuzzo: {response}")
        log_action(f"Francuzzo: {response}")
        log_action(user_input)





if __name__ == "__main__":
    francuzzo_chat()


###################MAIN