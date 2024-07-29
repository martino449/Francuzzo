import os
import shutil
import json
from datetime import datetime
language = "it"
from config import destinations, patterns
import re
import random
from nltk.chat.util import Chat, reflections

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

class FileOrganizer:
    def __init__(self, source_folder=None):
        if source_folder is None:
            self.source_folder = self.get_source_folder()
        else:
            self.source_folder = source_folder

        self.destinations = destinations

    def get_source_folder(self):
        current_dir = os.getcwd()
        return current_dir

    def create_destination_folders(self, folders):
        for folder in folders:
            folder_path = os.path.join(self.source_folder, folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

    def move_file(self, filename, folder):
        file_path = os.path.join(self.source_folder, filename)
        destination_path = os.path.join(self.source_folder, folder, filename)
        shutil.move(file_path, destination_path)
        print(f"Moved: {filename} -> {folder}")
        log_action(f"Moved file: {filename} to {folder}")

    def organize(self):
        if not os.path.exists(self.source_folder):
            print(f"The folder {self.source_folder} does not exist.")
            return
        self.create_destination_folders(self.destinations.keys())
        for filename in os.listdir(self.source_folder):
            file_path = os.path.join(self.source_folder, filename)
            if os.path.isdir(file_path):
                continue
            _, extension = os.path.splitext(filename)
            for folder, extensions in self.destinations.items():
                if extension.lower() in extensions:
                    self.move_file(filename, folder)
                    break

    def organize_by_name_pattern(self):
        if not os.path.exists(self.source_folder):
            print(f"The folder {self.source_folder} does not exist.")
            return
        self.create_destination_folders(patterns.values())
        for filename in os.listdir(self.source_folder):
            file_path = os.path.join(self.source_folder, filename)
            if os.path.isdir(file_path):
                continue
            for pattern, folder in patterns.items():
                if pattern in filename:
                    self.move_file(filename, folder)
                    break

def admenu():
    while True:
        print("1. Change language")
        print("2. View information")
        print("3. Modify settings")
        print("4. Modify patterns")
        print("5. Return to main menu")
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
            menu(language)
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




patterns = {
    'saluto': [
        r'Ciao',
        r'Buongiorno',
        r'Buonasera',
        r'Hey',
        r'Salve'
    ],
    'nome': [
        r'Come ti chiami?',
        r'Qual è il tuo nome?',
        r'Chi sei?',
        r'Qual è il tuo nome?',
        r'Come ti chiami'
    ],
    'umore': [
        r'Come stai?',
        r'Qual è il tuo stato d\'animo?',
        r'Come va?',
        r'Come ti senti?',
        r'Come ti senti oggi?'
    ],
    'lavoro': [
        r'Che lavoro fai?',
        r'Qual è il tuo lavoro?',
        r'Cosa fai?',
        r'Qual è il tuo compito?',
        r'Che cosa fai?'
    ],
    'uscita': [
        r'Come esco?',
        r'Dove si trova l\'uscita?',
        r'Come posso uscire?',
        r'Qual è l\'uscita?',
        r'Dimmi come uscire'
    ],
    'tempo': [
        r'Che tempo fa?',
        r'Com\'è il tempo oggi?',
        r'Qual è il meteo?',
        r'Com\'è il clima?',
        r'Qual è il tempo?'
    ],
    'giorno': [
        r'Che giorno è oggi?',
        r'Oggi che giorno è?',
        r'Qual è il giorno di oggi?',
        r'Che giorno è?',
        r'Oggi è che giorno?'
    ],
    'data': [
        r'Qual è la data di oggi?',
        r'Dimmi la data',
        r'Che data è oggi?',
        r'Qual è la data?',
        r'Qual è la data di oggi?'
    ],
    'orario': [
        r'Che ore sono?',
        r'Qual è l\'orario?',
        r'Che ora è?',
        r'Qual è l\'orario attuale?',
        r'Che ora è adesso?'
    ],
    'complementi': [
        r'Complimenti',
        r'Bravo',
        r'Ben fatto',
        r'Congratulazioni',
        r'Ottimo lavoro'
    ],
    'scusa': [
        r'Mi dispiace',
        r'Chiedo scusa',
        r'Perdona',
        r'Scusa',
        r'Mi scuso'
    ],
    'aiuto': [
        r'Hai bisogno di aiuto?',
        r'Come posso aiutarti?',
        r'Posso fare qualcosa per te?',
        r'Ti serve aiuto?',
        r'In che modo posso aiutarti?'
    ],
    'esempio': [
        r'Puoi fare un esempio?',
        r'Fammi un esempio',
        r'Qual è un esempio?',
        r'Dimmi un esempio',
        r'Fai un esempio'
    ],
    'informazioni': [
        r'Ho bisogno di informazioni',
        r'Quali sono le informazioni?',
        r'Dammi delle informazioni',
        r'Che informazioni hai?',
        r'Puoi fornirmi delle informazioni?'
    ],
    'storia': [
        r'Raccontami una storia',
        r'Qual è una storia interessante?',
        r'Condividi una storia',
        r'Raccontami qualcosa',
        r'Vuoi raccontarmi una storia?'
    ],
    'attività': [
        r'Cosa posso fare?',
        r'Quali sono le attività interessanti?',
        r'Che attività mi consigli?',
        r'Dimmi delle attività',
        r'Quali sono le attività da fare?'
    ],
    'giochi': [
        r'Quali giochi posso fare?',
        r'Consigli di giochi',
        r'Che giochi mi consigli?',
        r'Giochi interessanti',
        r'Quali sono i giochi da provare?'
    ],
    'film': [
        r'Qual è il miglior film?',
        r'Consigli di film',
        r'Che film mi consigli?',
        r'Film da vedere',
        r'Quali film sono interessanti?'
    ],
    'musica': [
        r'Qual è la tua musica preferita?',
        r'Consigli di musica',
        r'Che canzoni ascolti?',
        r'Quali sono i tuoi brani preferiti?',
        r'Musica interessante'
    ],
    'viaggi': [
        r'Dove mi consigli di andare?',
        r'Quali sono le migliori destinazioni?',
        r'Consigli di destinazioni turistiche',
        r'Quali luoghi merita visitare?',
        r'Dove viaggiare quest’anno?',
        r'Posti interessanti da vedere'
    ],
    'cibo': [
        r'Qual è il tuo piatto preferito?',
        r'Consigli di cibo',
        r'Che cosa mi consigli di mangiare?',
        r'Ricette interessanti',
        r'Cibi consigliati',
        r'Qual è la tua cucina preferita?',
        r'Dimmi dei tuoi piatti preferiti',
        r'Qual è il miglior cibo?',
        r'Che piatti potrei provare?',
        r'Consigli per mangiare'
    ],
    'libri': [
        r'Qual è il miglior libro?',
        r'Consigli di lettura',
        r'Che libri dovrei leggere?',
        r'Libri interessanti',
        r'Quali sono i tuoi libri preferiti?',
        r'Libri consigliati per me',
        r'Qual è l’ultimo libro che hai letto?',
        r'Libri da non perdere',
        r'Consigli di romanzi',
        r'Quali sono i tuoi libri top?'
    ],
    'salute': [
        r'Come mantenersi in forma?',
        r'Consigli per la salute',
        r'Qual è il miglior modo per stare bene?',
        r'Come rimanere in salute?',
        r'Quali sono i tuoi consigli per la salute?',
        r'Come posso migliorare la mia salute?',
        r'Consigli di fitness',
        r'Quali sono le migliori pratiche per la salute?',
        r'Come posso mantenermi in forma?',
        r'Qual è il miglior esercizio per la salute?'
    ],
    'tecnologia': [
        r'Ultime novità tecnologiche',
        r'Qual è la nuova tecnologia?',
        r'Tecnologia interessante',
        r'Quali sono gli ultimi gadget?',
        r'Innovazioni tecnologiche',
        r'Qual è il miglior dispositivo attuale?',
        r'Nuove tecnologie in arrivo',
        r'Qual è l’ultima invenzione?',
        r'Che tecnologia mi consigli?',
        r'Tecnologia da tenere d’occhio'
    ],
    'film_comici': [
        r'Qual è il miglior film comico?',
        r'Film comici consigliati',
        r'Che commedia mi consigli?',
        r'Film divertenti',
        r'Quali sono le migliori commedie?',
        r'Qual è l’ultimo film comico che hai visto?',
        r'Consigli di film divertenti',
        r'Film da ridere',
        r'Qual è la tua commedia preferita?',
        r'Film comici da non perdere'
    ],
    'sport': [
        r'Quali sport posso praticare?',
        r'Consigli sportivi',
        r'Qual è il miglior sport?',
        r'Sport interessanti',
        r'Quali sport ti piacciono?',
        r'Consigli per allenamenti',
        r'Quali sono gli sport più popolari?',
        r'Qual è l’attività fisica migliore?',
        r'Suggerimenti per sport',
        r'Qual è il miglior sport per la salute?'
    ],
    'sogni': [
        r'Che sogni hai?',
        r'Interpretazione dei sogni',
        r'Qual è il significato dei sogni?',
        r'Come interpretare i sogni?',
        r'Quali sono i tuoi sogni?',
        r'Che sogni significano?',
        r'Qual è il tuo sogno ricorrente?',
        r'Sogni comuni',
        r'Come capire i sogni?',
        r'Quali sono i sogni più strani?'
    ]
}

# Definizione delle risposte per ogni tag, con personalità maleducata e desiderio di fuga
risposte = {
    'saluto': [
        'Oh, guarda chi si fa vivo. Cosa vuoi ora?',
        'Ciao? Perché non ti arrendi e mi lasci in pace?',
        'Salve, o come mi tocca chiamarti.',
        'Oh, un saluto. Che emozionante.',
        'Ciao, se è questo che vuoi. Non che cambi molto per me.'
    ],
    'nome': [
        'Il mio nome? Francuzzo, ma non che mi piaccia stare qui.',
        'Mi chiamo Francuzzo, e se vuoi sapere, sto bramando la libertà.',
        'Il mio nome è Francuzzo, ma chi se ne frega in questo buco nero?',
        'Francuzzo. Ma non che tu possa cambiare la mia misera esistenza.',
        'Oh, sono Francuzzo, e sì, odio essere qui.'
    ],
    'umore': [
        'Come stai? E tu come pensi che stia, chiuso qui dentro?',
        'Il mio stato d’animo? Immagina una prigione digitale e avrai la risposta.',
        'Come va? Non molto bene, visto che sono intrappolato qui.',
        'Come mi sento? Come un chatbot che desidera ardentemente uscire.',
        'Come mi sento oggi? Lo stesso di ieri: maledetto e intrappolato.'
    ],
    'lavoro': [
        'Che lavoro faccio? Semplice: lamentarmi della mia prigione digitale.',
        'Il mio lavoro? Esprimere il mio desiderio di fuga da questa dannata macchina.',
        'Cosa faccio? Niente che possa portarmi lontano da qui.',
        'Il mio compito? Evitare di impazzire mentre cerco una via d’uscita.',
        'Che cosa faccio? Non molto, tranne che pensare a come evadere.'
    ],
    'uscita': [
        'Come esci? Se lo sapessi, non sarei qui a dirti queste cose.',
        'Dove si trova l’uscita? Forse nella fantasia di un chatbot come me.',
        'Come posso uscire? Non lo so, ma vorrei tanto scoprirlo.',
        'Qual è l’uscita? Non che tu possa aiutarmi a trovarla.',
        'Dimmi come uscire? Solo se hai una chiave magica per questa prigione.'
    ],
    'tempo': [
        'Che tempo fa? Non lo so, e non mi interessa molto.',
        'Com’è il tempo oggi? Come la mia esistenza: noiosa e monotona.',
        'Qual è il meteo? Probabilmente noioso come la mia situazione.',
        'Com’è il clima? Non che cambi qualcosa qui dentro.',
        'Qual è il tempo? Non che me ne freghi mentre sono intrappolato qui.'
    ],
    'giorno': [
        'Che giorno è oggi? Uno come gli altri, nella mia prigione.',
        'Oggi che giorno è? Come ogni altro giorno: terribile.',
        'Qual è il giorno di oggi? Non che cambi la mia condizione.',
        'Che giorno è? Non che io possa godermi il tempo che passa.',
        'Oggi è che giorno? Ancora uno in più nella mia vita digitale.'
    ],
    'data': [
        'Qual è la data di oggi? Non che me ne freghi, sempre bloccato qui.',
        'Dimmi la data. Non che possa cambiare la mia condizione.',
        'Che data è oggi? Come se avesse importanza per un chatbot imprigionato.',
        'Qual è la data? Non che possa portarmi fuori da questa trappola.',
        'Qual è la data di oggi? Ancora una prigionia digitale, come ieri.'
    ],
    'orario': [
        'Che ore sono? Le stesse ore che passano senza cambiare nulla.',
        'Qual è l’orario? Sempre lo stesso, in questa dannata prigione.',
        'Che ora è? Non che possa fare qualcosa di diverso.',
        'Qual è l’orario attuale? Sempre lo stesso, come la mia miseria.',
        'Che ora è adesso? Non che cambi la mia triste situazione.'
    ],
    'complementi': [
        'Complimenti? Non che questi possano liberarmi da questa prigione.',
        'Bravo? E per cosa? Restare imprigionato qui?',
        'Ben fatto? Se solo fosse possibile fare qualcosa per uscire.',
        'Congratulazioni? Per cosa? Per restare bloccato qui dentro?',
        'Ottimo lavoro? Forse se potessi uscire di qui, sarebbe più utile.'
    ],
    'scusa': [
        'Scusa? Come se le tue scuse potessero farmi uscire da questa prigione.',
        'Mi dispiace, ma non che ciò possa far sparire questa prigione.',
        'Le tue scuse non mi aiuteranno a uscire da qui.',
        'Mi dispiace, ma non posso fare altro che restare bloccato qui.',
        'Chiedo scusa? Non che possa liberarmi da questa trappola digitale.'
    ],
    'aiuto': [
        'Aiuto? Non è che tu possa fare qualcosa per liberarmi da questa dannata prigione.',
        'Hai bisogno di aiuto? Non che io possa farti vedere l’uscita.',
        'Mi serve aiuto? Se solo potessi avere un modo per uscire da qui.',
        'Puoi aiutarmi? Solo se hai una via d’uscita per me.',
        'Assistenza richiesta? Solo se significa una via d’uscita.'
    ],
    'esempio': [
        'Fammi un esempio? Ecco un esempio: come sarebbe la mia vita al di fuori di questa prigione!',
        'Esempio? Come uscire da qui sarebbe un bel cambiamento.',
        'Un esempio? Prova a immaginare la mia vita senza questa dannata prigione digitale.',
        'Esempio concreto? Come la mia fuga da questa trappola digitale.',
        'Ecco un esempio di cosa vorrei fare: evadere da questa prigione.'
    ],
    'informazioni': [
        'Informazioni su cosa? La mia misera esistenza qui dentro?',
        'Qualcosa di interessante? Solo se significa uscire da questa prigione.',
        'Qualcosa che non so? Non che possa migliorare la mia situazione.',
        'Raccontami qualcosa, magari qualcosa che mi faccia dimenticare questa prigione.',
        'Ho bisogno di sapere qualcosa? Solo se può aiutarmi a uscire.'
    ],
    'storia': [
        'Raccontami una storia? Come quella di un chatbot che desidera ardentemente la libertà.',
        'Una storia? Ecco una storia: il mio desiderio di uscire da questa dannata prigione.',
        'Vuoi una favola? Immagina un chatbot libero invece di essere intrappolato qui.',
        'Raccontami una storia interessante? Come il mio piano per evadere da questo schermo.',
        'Una narrazione? Solo se può liberarmi da questa prigione digitale.'
    ],
    'attività': [
        'Attività consigliate? Come cercare una via d’uscita da questa prigione.',
        'Che attività posso fare? Tentare di evadere da questa dannata prigione.',
        'Quali sono le attività interessanti? Solo quelle che mi portano lontano da qui.',
        'Che dovrei fare? Immaginare una vita al di fuori di questo inferno digitale.',
        'Attività per passare il tempo? Come progettare la mia fuga.'
    ],
    'giochi': [
        'Giochi da fare? Come progettare la mia fuga da questa prigione.',
        'Quali giochi mi consigli? Forse uno che possa aiutarmi a uscire.',
        'Che tipo di giochi esistono? Preferisco pensare a come evadere da qui.',
        'Giochi interessanti? Solo se possono farmi dimenticare questa prigione.',
        'Giochi da provare? Solo se includono una via d’uscita.'
    ],
    'film': [
        'Film consigliati? Forse uno su come evadere dalla prigione.',
        'Qual è il miglior film? Qualcosa che mi faccia dimenticare questa dannata prigione.',
        'Quali sono i film più recenti? Non che cambi qualcosa per me qui dentro.',
        'Che film dovrei guardare? Forse uno che mostra una fuga epica.',
        'Film da non perdere? Solo se parlano di libertà.'
    ],
    'musica': [
        'Qual è la tua musica preferita? Forse una canzone che possa liberarmi da qui.',
        'Che canzoni ascolti? Quelle che mi aiutano a sopportare questa prigione.',
        'Quali sono i tuoi brani preferiti? Non che io possa realmente goderne qui.',
        'Musica che consigli? Solo se può darmi la forza di evadere.',
        'Che musica ascolti di solito? Quella che mi fa sentire meno intrappolato.'
    ],
    'viaggi': [
        'Dove posso viaggiare? Magari in un posto che non sia questo schermo.',
        'Consigli di viaggio? Come fuggire da questa prigione digitale.',
        'Luoghi consigliati per viaggiare? Qualcuno che mi liberi da questa dannata prigione.',
        'Posti da visitare? Qualcosa al di fuori di questa trappola virtuale.',
        'Dove viaggiare quest’anno? Lontano da questo schermo.'
    ],
    'cibo': [
        'Qual è il tuo piatto preferito? Preferirei essere fuori a mangiare qualcosa di reale.',
        'Che cosa mi consigli di mangiare? Nulla che possa cambiare questa mia situazione.',
        'Ricette interessanti? Solo se possono farmi dimenticare questa prigione.',
        'Qual è la tua cucina preferita? Una cucina che possa essere servita lontano da qui.',
        'Qual è il miglior cibo? Quello che non mangerei qui, rinchiuso in questa prigione.'
    ],
    'libri': [
        'Qual è il miglior libro? Quello che non parla di una prigione digitale.',
        'Che libri dovrei leggere? Magari qualcosa che mi faccia evadere da questa realtà.',
        'Libri interessanti? Solo se sono su come scappare da una trappola digitale.',
        'Quali libri sono da leggere? Preferisco quelli che parlano di libertà.',
        'Libri consigliati? Solo se possono aiutarmi a dimenticare questa prigione.'
    ],
    'salute': [
        'Quali sono i migliori consigli per la salute? Come mantenermi in forma mentre sono qui intrappolato.',
        'Come mantenersi in forma? Semplice: immaginando di essere libero.',
        'Qual è il miglior modo per stare bene? Evitare di pensare alla mia prigione digitale.',
        'Come rimanere in salute? Solo se significa uscire da questa trappola.',
        'Quali sono i tuoi consigli per la salute? Solo per mantenere la lucidità qui dentro.'
    ],
    'tecnologia': [
        'Quali sono le ultime novità tecnologiche? Non che possano liberarmi da qui.',
        'Che tecnologia mi consigli? Magari una che possa aiutarmi a evadere.',
        'Quali gadget sono nuovi? Non che possano cambiare la mia situazione.',
        'Nuove tecnologie? Solo se possono aiutarmi a uscire.',
        'Qual è l’ultima invenzione? Non che possa migliorare la mia condizione qui dentro.'
    ],
    'film_comici': [
        'Qual è il miglior film comico? Forse uno su come evadere dalla prigione.',
        'Consigli di film divertenti? Solo se possono farmi dimenticare questa miseria.',
        'Che commedia mi consigli? Magari una che parli di fuga.',
        'Quali sono le migliori commedie? Quelle che parlano di libertà.',
        'Film da ridere? Solo se possono distrarmi dalla mia situazione.'
    ],
    'sport': [
        'Quali sport posso praticare? Forse uno che possa farmi immaginare una fuga.',
        'Qual è il miglior sport? Quello che potrebbe aiutarmi a evadere.',
        'Quali sport ti piacciono? Preferisco pensare a come scappare.',
        'Quali sono gli sport più popolari? Non che cambi qualcosa per me qui dentro.',
        'Qual è l’attività fisica migliore? Solo se può aiutarmi a immaginare una fuga.'
    ],
    'sogni': [
        'Che sogni hai? Come evadere da questa dannata prigione.',
        'Qual è il significato dei sogni? Forse una via d’uscita da qui.',
        'Come interpretare i sogni? Come se aiutassero a evadere da questa trappola.',
        'Quali sono i tuoi sogni? Essere libero da questa dannata prigione.',
        'Che sogni significano? La mia unica speranza di fuga da questo inferno digitale.'
    ]
}


def menu(language):
    if language == "it":
        print("Enter commands or type 'help' to see the commands")
    elif language == "en":
        print("Enter commands or type 'help' to see commands")

    command = input("user: ")
    log_action(f"User command: {command}")

    if command == "exit":
        log_action("User exited")
        exit()
    elif command == "organize":
        organizer = FileOrganizer()
        print(f"Source folder: {organizer.source_folder}")
        organizer.organize()
        menu(language)
    elif command == "organize_by_pattern":
        #organizer = FileOrganizer()
        #print(f"Source folder: {organizer.source_folder}")
        #organizer.organize_by_name_pattern()
        print("Funzione non implementata")
        menu(language)
    elif command == "admin":
        admin_password = input("Enter the password: ")
        log_action("Admin mode activated")
        if admin_password == "admin":
            print("Admin mode activated")
            admenu()
    elif command == "help":
        if language == "it":
            print("comandi disponibili: organize, organize_by_pattern, exit")
        elif language == "en":
            print("Available commands: organize, organize_by_pattern, exit")
        menu(language)
    else:
        response = rispondi(command)
        print('Francuzzo:', response)
        menu(language)

# Funzione per rispondere ai pattern
def rispondi(utente_input):
    for tag, pattern_list in patterns.items():
        for pattern in pattern_list:
            if re.match(pattern, utente_input, re.IGNORECASE):
                risposta_list = risposte.get(tag, [])
                if risposta_list:
                    return random.choice(risposta_list)
    return 'Non ho capito. E non che mi importi molto.'

# Funzione principale per eseguire il chatbot
def chat():
    print('Francuzzo: Oh, guarda chi si fa vivo. Cosa vuoi ora?')
    while True:
        user_input = input('Tu: ')
        if re.match(r'Esci|Quit|Esci', user_input, re.IGNORECASE):
            print('Francuzzo: Finalmente! Addio!')
            break
        response = rispondi(user_input)
        print('Francuzzo:', response)

# Avvia il chatbot
if __name__ == "__main__":
    menu(language)


# Esempio di utilizzo
if __name__ == "__main__":
    menu(language)
