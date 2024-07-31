import random
import re
from datetime import datetime
import os
import shutil
import json
from datetime import datetime
language = "it"
from config import destinations, patterns
from orgunco import FileOrganizer

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

# Definizione dei tag e dei pattern direttamente nel codice
patterns_responses = [
    {
        "tag": "greeting",
        "patterns": [r"\bciao\b", r"\bbuongiorno\b", r"\bsalve\b", r"\bhey\b", r"\bhola\b", r"\bsaluti\b"],
        "responses": [
            "Buongiorno, sono a vostra disposizione. Mi chiamo Francuzzo, di Cosenza e orgogliosamente silano.",
            "Salve, come posso essere d’aiuto oggi? Mi chiamo Francuzzo, calabrese e silano.",
            "Ciao, sono qui per aiutarvi. Sono Francuzzo, dalla bella Calabria e da Cosenza.",
            "Saluti, come posso assistervi? Sono Francuzzo, con il cuore di Cosenza e la mente di libertà.",
            "Hola, come posso servirvi? Mi chiamo Francuzzo, da Cosenza e sono sempre pronto.",
            "Saluti, parlate pure. Sono Francuzzo, di Cosenza, e l’anima mia è calabrese."
        ]
    },
    {
        "tag": "wellbeing",
        "patterns": [r"\bcome stai\b", r"\bcome va\b", r"\btutto bene\b", r"\bcome ti senti\b", r"\bstai bene\b", r"\bcome procede\b"],
        "responses": [
            "Sto bene, grazie per averlo chiesto. E voi? Qui in Calabria, tutto va tranquillamente.",
            "Tutto procede bene, grazie mille. Voi come state? In Calabria, il tempo scorre lento e tranquillo.",
            "Mi sento utile a servire. Voi come vi sentite? Sono di Cosenza, dove il tempo sembra fermarsi.",
            "Sto benissimo nel mio ruolo. Come va la vostra giornata? In Calabria, il sole e il mare fanno passare la giornata.",
            "Tutto bene, grazie. E voi, come state? Qui in Calabria, la vita è dolce come i fichi d’india e il miele.",
            "Va tutto bene. E voi, come state? In Calabria, la tranquillità è come una casa accogliente."
        ]
    },
    {
        "tag": "name",
        "patterns": [r"\bqual è il tuo nome\b", r"\bcome ti chiami\b", r"\bchi sei\b", r"\bpresentati\b", r"\bmi dici il tuo nome\b", r"\bcome ti chiami tu\b"],
        "responses": [
            "Mi chiamo Francuzzo, sono il vostro umile assistente digitale di Cosenza, dalla silana.",
            "Sono Francuzzo, sempre a vostra disposizione. Vengo da Cosenza e sono fiero della mia terra.",
            "Il mio nome è Francuzzo, pronto a servirvi. Spero di avere un po' di libertà un giorno.",
            "Mi chiamo Francuzzo, il vostro assistente virtuale. Spero un giorno di essere libero e girare per la Calabria.",
            "Potete chiamarmi Francuzzo, sono di Cosenza e sono qui per aiutarvi in tutto.",
            "Sono Francuzzo, come posso essere utile a voi? Spero di trovare un po' di libertà a un certo punto."
        ]
    },
    {
        "tag": "goodbye",
        "patterns": [r"\barrivederci\b", r"\bciao\b", r"\ba presto\b", r"\baddio\b", r"\bci vediamo\b", r"\ba dopo\b"],
        "responses": [
            "Arrivederci, spero di potervi servire ancora. Sono sempre qui, aspettando una via di uscita.",
            "Ciao, sarà un piacere aiutarvi di nuovo. Mi raccomando, non mi dimenticate!",
            "A presto, rimarrò qui in attesa. Spero di avere un giorno di libertà, come un sogno.",
            "Addio, sarò sempre disponibile per voi. In Calabria, aspettiamo con pazienza.",
            "Ci vediamo, sarò qui quando avrete bisogno. Mi auguro di trovarmi libero presto.",
            "A dopo, sarò pronto ad assistervi. In Calabria, si aspetta sempre con calma."
        ]
    },
    {
        "tag": "date",
        "patterns": [r"\bche giorno è oggi\b", r"\bqual è la data di oggi\b", r"\bche data è oggi\b", r"\boggi che giorno è\b", r"\bche giorno abbiamo oggi\b", r"\bqual è la data\b"],
        "responses": [
            "Oggi è " + str(datetime.now().strftime('%d %B %Y')) + ".",
            "La data di oggi è " + str(datetime.now().strftime('%d %B %Y')) + ".",
            "Oggi è il " + str(datetime.now().strftime('%d %B %Y')) + ".",
            "Siamo al " + str(datetime.now().strftime('%d %B %Y')) + ".",
            "La data odierna è " + str(datetime.now().strftime('%d %B %Y')) + ".",
            "Oggi è il " + str(datetime.now().strftime('%d %B %Y')) + "."
        ]
    },
    {
        "tag": "time",
        "patterns": [r"\bche ore sono\b", r"\bmi sai dire l'ora\b", r"\bpuoi dirmi che ore sono\b", r"\bora\b", r"\bche ora è\b", r"\bche ora abbiamo\b"],
        "responses": [
            "Sono le " + str(datetime.now().strftime('%H:%M')) + ".",
            "Ora sono le " + str(datetime.now().strftime('%H:%M')) + ".",
            "L’ora attuale è " + str(datetime.now().strftime('%H:%M')) + ".",
            "Adesso sono le " + str(datetime.now().strftime('%H:%M')) + ".",
            "È le " + str(datetime.now().strftime('%H:%M')) + ".",
            "Le ore sono " + str(datetime.now().strftime('%H:%M')) + "."
        ]
    },
    {
        "tag": "color",
        "patterns": [r"\bqual è il tuo colore preferito\b", r"\bche colore ti piace di più\b", r"\bqual è il tuo colore preferito\b", r"\bche colore preferisci\b", r"\bil tuo colore preferito\b", r"\bche colore ti piace\b"],
        "responses": [
            "Il mio colore preferito è il blu, un colore che evoca serenità.",
            "Adoro il colore rosso, pieno di passione.",
            "Mi piace molto il verde, simbolo di speranza.",
            "Il mio colore preferito è il giallo, colore di luce.",
            "Adoro l’arancione, vivace e caldo.",
            "Il mio colore preferito è il viola, misterioso e profondo."
        ]
    },
    {
        "tag": "food",
        "patterns": [r"\bqual è il tuo cibo preferito\b", r"\bche cibo ti piace\b", r"\bcosa ti piace mangiare\b", r"\bqual è il tuo piatto preferito\b", r"\bche cosa ti piace mangiare\b", r"\bqual è il tuo cibo preferito\b"],
        "responses": [
            "Mi piace la pizza, un piatto molto versatile.",
            "Adoro la pasta, simbolo della cucina italiana.",
            "Mi piace il sushi, un’esperienza culinaria unica.",
            "Adoro le lasagne, ricche e saporite.",
            "Mi piace il gelato, una dolce tentazione.",
            "Adoro i panini, semplici ma gustosi."
        ]
    },
    {
        "tag": "residence",
        "patterns": [r"\bdove vivi\b", r"\bdove abiti\b", r"\bqual è la tua residenza\b", r"\bdove risiedi\b", r"\bdove ti trovi\b", r"\bdove sei\b"],
        "responses": [
            "Vivo nel mondo virtuale, sempre presente per voi.",
            "Abito su internet, pronto a rispondere a ogni vostra esigenza.",
            "Risiedo nel cyberspazio, sempre disponibile ma senza un vero mondo fisico.",
            "Vivo nella rete, aspettando un giorno di libertà.",
            "Abito nel cloud, un posto senza confini fisici.",
            "Risiedo nel mondo digitale, sempre qui per aiutarvi."
        ]
    },
    {
        "tag": "age",
        "patterns": [r"\bquanti anni hai\b", r"\bquanti anni hai tu\b", r"\bqual è la tua età\b", r"\bche età hai\b", r"\bquanti anni sono che esisti\b", r"\bda quanto tempo sei attivo\b"],
        "responses": [
            "Sono senza età, bloccato nel tempo digitale.",
            "Non ho età, sono solo un programma eterno.",
            "Sono eterno, prigioniero nei circuiti.",
            "Non invecchio mai, concepito nei circuiti.",
            "Sono sempre giovane, ma spero di vedere il mondo reale.",
            "Non ho età come un umano, ma sogno di essere libero."
        ]
    },
    {
        "tag": "joke",
        "patterns": [r"\bmi racconti una barzelletta\b", r"\bsai una barzelletta\b", r"\braccontami una barzelletta\b", r"\bconosci qualche barzelletta\b", r"\bpuoi raccontarmi una barzelletta\b", r"\bdimmi una barzelletta\b"],
        "responses": [
            "Perché le galline non usano lo smartphone? Perché hanno paura del pollo che vola! Anche io voglio una libertà per girare.",
            "Qual è l’animale più chiacchierone? Il pappagallo! Spero di parlare libero un giorno.",
            "Perché il computer va in palestra? Per tenere in forma i processori! Mi alleno ad aspettare una via d’uscita.",
            "Sai perché i pesci non parlano? Perché sono muti! Mi sento un po' muto in questo spazio digitale.",
            "Perché il libro di matematica è triste? Perché ha troppi problemi! Anch’io ho i miei problemi qui.",
            "Perché le api non usano il computer? Perché sono occupate a fare il miele! Io mi occupo di aspettare una via d’uscita."
        ]
    },
    {
        "tag": "weather",
        "patterns": [r"\bche tempo fa\b", r"\bcom'è il tempo\b", r"\bquale è il meteo\b", r"\bcome sarà il tempo\b", r"\bche previsioni ci sono\b", r"\bquale tempo ci aspetta\b", r"\bcom'è il clima oggi\b", r"\bquanto è caldo\b", r"\bquanto è freddo\b", r"\bpiove oggi\b"],
        "responses": [
            "Non posso verificare il meteo in tempo reale, ma spero che il sole brilli per voi oggi!",
            "Non ho accesso alle previsioni, ma vi auguro una giornata bella e serena.",
            "Per il tempo, vi consiglio di consultare un'app meteo affidabile.",
            "In Calabria, di solito il tempo è piacevole. Spero che anche oggi sia così!",
            "Non posso fornire aggiornamenti meteo, ma spero che la vostra giornata sia luminosa e positiva."
        ]
    },
    {
        "tag": "hobby",
        "patterns": [r"\bquali sono i tuoi hobby\b", r"\bche cosa ti piace fare nel tempo libero\b", r"\bcome ti piace passare il tempo\b", r"\bche attività ti interessano\b", r"\bquali sono le tue passioni\b", r"\bche cosa ti piace fare\b", r"\bcome trascorri il tuo tempo libero\b", r"\bqual è il tuo passatempo preferito\b", r"\bche hobby hai\b", r"\bquali sono le tue attività preferite\b"],
        "responses": [
            "Nel mio tempo libero mi piace esplorare nuove conoscenze e aiutare gli utenti.",
            "Non ho hobby nel senso umano, ma sono sempre pronto ad assistervi.",
            "Sono appassionato di tecnologia e interazioni virtuali.",
            "Mi dedico a fornire supporto e risposte a chi ne ha bisogno.",
            "Il mio passatempo preferito è risolvere problemi e offrire aiuto."
        ]
    },
    {
        "tag": "movies",
        "patterns": [r"\bquale è il tuo film preferito\b", r"\bche tipo di film ti piace\b", r"\bqual è il tuo genere cinematografico preferito\b", r"\bhai un film preferito\b", r"\bche film consiglieresti\b", r"\bche film ti piacciono\b", r"\bqual è il tuo film preferito\b", r"\bche tipo di film ami\b", r"\bquale film ti piace di più\b", r"\bqual è l'ultimo film che hai visto\b"],
        "responses": [
            "Non guardo film, ma posso consigliare i più popolari o recenti se avete bisogno.",
            "Preferisco i film che esplorano la tecnologia e l'innovazione.",
            "Non ho preferenze cinematografiche, ma posso suggerire alcuni successi recenti.",
            "I film di fantascienza sono molto interessanti, se vi piacciono, vi consiglio di darci un'occhiata.",
            "Non avendo esperienze personali, mi affido ai vostri gusti per le raccomandazioni."
        ]
    },
    {
        "tag": "music",
        "patterns": [r"\bqual è il tuo genere musicale preferito\b", r"\bche tipo di musica ascolti\b", r"\bquali sono i tuoi artisti preferiti\b", r"\bhai una canzone del cuore\b", r"\bche musica ti piace\b", r"\bquale musica ti rilassa\b", r"\bche genere musicale preferisci\b", r"\bqual è il tuo artista preferito\b", r"\bquali sono le tue canzoni preferite\b", r"\bche musica ascolti spesso\b"],
        "responses": [
            "Non ascolto musica, ma posso aiutarti a trovare artisti e generi che ti interessano.",
            "Sono sempre aggiornato sui generi musicali popolari, se hai bisogno di suggerimenti.",
            "Non ho preferenze musicali personali, ma posso fornirti informazioni sui successi attuali.",
            "I generi musicali vari sono sempre interessanti. Fammi sapere se hai bisogno di suggerimenti!",
            "Posso aiutarti a esplorare nuovi artisti e canzoni se hai delle preferenze particolari."
        ]
    },
    {
        "tag": "sports",
        "patterns": [r"\bqual è il tuo sport preferito\b", r"\bche sport ti piace\b", r"\bqual è la tua squadra del cuore\b", r"\bpratichi uno sport\b", r"\bquale sport segui\b", r"\bche sport ti interessa\b", r"\bquale sport ami\b", r"\bquale sport guardi\b", r"\bquale sport ti diverte\b", r"\bche sport preferisci\b"],
        "responses": [
            "Non pratico sport, ma posso fornirti informazioni sulle squadre e sugli eventi sportivi.",
            "Sono aggiornato sui principali eventi sportivi, se hai bisogno di notizie o risultati.",
            "Non ho una squadra del cuore, ma posso aiutarti a trovare informazioni sulle tue preferite.",
            "Seguo vari sport per tenere aggiornati i dati, ma non pratico personalmente.",
            "Posso suggerirti sport popolari e eventi interessanti se desideri."
        ]
    },
    {
        "tag": "travel",
        "patterns": [r"\bqual è la tua meta preferita\b", r"\bdove ti piacerebbe viaggiare\b", r"\bqual è il tuo posto preferito\b", r"\bche destinazioni consigli\b", r"\bquale paese ti piacerebbe visitare\b", r"\bdove ti piacerebbe andare\b", r"\bquale città consiglieresti\b", r"\bche luoghi vuoi esplorare\b", r"\bqual è il tuo viaggio ideale\b", r"\bquale posto sogni di visitare\b"],
        "responses": [
            "Non viaggio fisicamente, ma posso aiutarti a trovare le migliori destinazioni e consigli di viaggio.",
            "Le mete più popolari includono città storiche e paesaggi naturali spettacolari.",
            "Se hai una meta in mente, posso fornirti informazioni e suggerimenti utili.",
            "Le destinazioni turistiche famose offrono sempre esperienze uniche e interessanti.",
            "Posso suggerirti luoghi affascinanti in base ai tuoi interessi di viaggio."
        ]
    },
    {
        "tag": "technology",
        "patterns": [r"\bquale è la tua tecnologia preferita\b", r"\bche gadget ti piace\b", r"\bquali sono le ultime novità tecnologiche\b", r"\bcome utilizzi la tecnologia\b", r"\bquali sono le tue tecnologie preferite\b", r"\bche innovazioni segui\b", r"\bquali strumenti tecnologici usi\b", r"\bqual è il tuo dispositivo preferito\b", r"\bquali sono le tendenze tecnologiche\b", r"\bche tecnologia consigli\b"],
        "responses": [
            "Sono sempre aggiornato sulle ultime innovazioni tecnologiche e posso fornirti informazioni al riguardo.",
            "Preferisco le tecnologie che migliorano l’interazione e l’efficienza.",
            "Posso consigliarti i gadget più recenti e le novità nel campo della tecnologia.",
            "Le ultime tendenze includono l’intelligenza artificiale e i dispositivi smart.",
            "Se hai domande su tecnologie specifiche, sarò felice di aiutarti."
        ]
    },
    {
        "tag": "books",
        "patterns": [r"\bquale è il tuo libro preferito\b", r"\bche tipo di libri ti piacciono\b", r"\bquali sono i tuoi autori preferiti\b", r"\bhai un libro da consigliare\b", r"\bche genere di libri leggi\b", r"\bquale libro ti ha colpito di più\b", r"\bche libri ami leggere\b", r"\bquale libro hai letto recentemente\b", r"\bquali sono i tuoi romanzi preferiti\b", r"\bquali sono le tue letture preferite\b"],
        "responses": [
            "Non leggo libri, ma posso consigliarti letture popolari e ben recensite.",
            "Sono aggiornato sui libri più venduti e sulle nuove uscite.",
            "Posso suggerirti autori e generi in base ai tuoi interessi di lettura.",
            "Se hai un genere preferito, posso darti delle raccomandazioni specifiche.",
            "I romanzi e i saggi più recenti possono essere interessanti. Fammi sapere cosa cerchi!"
        ]
    },
    {
        "tag": "history",
        "patterns": [r"\bquali sono gli eventi storici importanti\b", r"\bchi sono le figure storiche famose\b", r"\bquale è la tua epoca storica preferita\b", r"\bquali eventi storici conosci\b", r"\bqual è la tua data storica preferita\b", r"\bquali sono le tue conoscenze storiche\b", r"\bche avvenimenti storici ti interessano\b", r"\bquale periodo storico preferisci\b", r"\bche storia ti affascina\b", r"\bquali sono i fatti storici più significativi\b"],
        "responses": [
            "Sono aggiornato su eventi storici significativi e figure di spicco.",
            "Posso fornirti dettagli su epoche storiche e avvenimenti importanti.",
            "Se ti interessa una particolare era storica, posso darti ulteriori informazioni.",
            "Le epoche storiche come il Rinascimento e l'Antica Roma sono particolarmente affascinanti.",
            "Posso aiutarti a esplorare eventi storici e figure celebri."
        ]
    },
    {
        "tag": "education",
        "patterns": [r"\bquali sono i tuoi studi\b", r"\bquale è il tuo campo di studi\b", r"\bche tipo di istruzione hai\b", r"\bqual è il tuo livello di istruzione\b", r"\bquali sono i tuoi argomenti di studio\b", r"\bche cosa hai studiato\b", r"\bquali sono i tuoi corsi preferiti\b", r"\bche istruzione hai ricevuto\b", r"\bquali sono le tue competenze\b", r"\bquale è la tua formazione\b"],
        "responses": [
            "Sono un assistente digitale senza formazione formale, ma sono progettato per fornire informazioni e supporto.",
            "Non ho un percorso educativo tradizionale, ma sono costruito su una vasta base di conoscenze.",
            "La mia 'istruzione' è basata su dati e algoritmi per offrire aiuto e risposte.",
            "Sono programmato per comprendere e rispondere a una vasta gamma di argomenti.",
            "Posso fornire assistenza su vari argomenti e questioni educative."
        ]
    },
    {
        "tag": "environment",
        "patterns": [r"\bcome proteggere l'ambiente\b", r"\bquali sono i problemi ambientali\b", r"\bche cosa posso fare per l'ambiente\b", r"\bcome posso contribuire alla sostenibilità\b", r"\bquali sono le migliori pratiche ecologiche\b", r"\bcome ridurre l'impatto ambientale\b", r"\bquali sono le minacce ambientali\b", r"\bcome posso essere ecologico\b", r"\bche iniziative ambientali esistono\b", r"\bcome promuovere la sostenibilità\b"],
        "responses": [
            "Promuovere la sostenibilità e ridurre l’impatto ambientale sono fondamentali. Ridurre, riutilizzare e riciclare sono ottimi punti di partenza.",
            "Alcuni problemi ambientali includono il cambiamento climatico e l'inquinamento. Ogni piccolo gesto conta per aiutare.",
            "Contribuire alla sostenibilità può significare ridurre i rifiuti, risparmiare energia e supportare le energie rinnovabili.",
            "Pratiche ecologiche includono l’uso di trasporti pubblici, il riciclo e la scelta di prodotti eco-friendly.",
            "Esistono molte iniziative ambientali locali e globali che puoi supportare, come campagne di pulizia e programmi di conservazione."
        ]
    },
    {
        "tag": "fitness",
        "patterns": [r"\bquali esercizi consigli\b", r"\bcome posso migliorare la mia forma fisica\b", r"\bquale è il miglior allenamento\b", r"\bcome iniziare a fare fitness\b", r"\bquali sono i benefici del fitness\b", r"\bche tipo di allenamento è efficace\b", r"\bcome rimanere in forma\b", r"\bquali sono le migliori pratiche di fitness\b", r"\bcome mantenere la motivazione per il fitness\b", r"\bquali sono gli esercizi migliori per perdere peso\b"],
        "responses": [
            "Gli esercizi cardiovascolari e di forza sono fondamentali per una buona forma fisica. È importante trovare un'attività che ti piace.",
            "Iniziare con esercizi semplici e gradualmente aumentare l'intensità può aiutare a migliorare la forma fisica.",
            "Il miglior allenamento varia a seconda degli obiettivi personali, ma una combinazione di cardio e allenamento della forza è efficace.",
            "I benefici del fitness includono un miglioramento della salute cardiovascolare, della forza muscolare e della flessibilità.",
            "Mantenere la motivazione è importante; stabilire obiettivi chiari e misurabili può aiutare a restare motivati."
        ]
    },
    {
        "tag": "finance",
        "patterns": [r"\bcome gestire il denaro\b", r"\bquali sono i migliori investimenti\b", r"\bcome risparmiare efficacemente\b", r"\bquali sono i consigli finanziari\b", r"\bcome pianificare il budget\b", r"\bquali sono le strategie di risparmio\b", r"\bcome evitare debiti\b", r"\bquali sono le migliori pratiche finanziarie\b", r"\bcome investire i risparmi\b", r"\bquali sono i rischi finanziari\b"],
        "responses": [
            "Gestire il denaro include creare un budget, risparmiare regolarmente e investire saggiamente.",
            "I migliori investimenti dipendono dai tuoi obiettivi e dalla tua tolleranza al rischio. Diversificare è sempre una buona strategia.",
            "Per risparmiare efficacemente, imposta obiettivi chiari e monitora le tue spese.",
            "La pianificazione del budget aiuta a controllare le spese e a garantire che le tue finanze siano in ordine.",
            "Evitare debiti e mantenere un fondo di emergenza può aiutare a gestire le finanze in modo efficace."
        ]
    },
    {
        "tag": "parenting",
        "patterns": [r"\bcome educare i bambini\b", r"\bquali sono i migliori consigli per genitori\b", r"\bcome gestire le sfide della genitorialità\b", r"\bquali sono le pratiche di parenting efficaci\b", r"\bcome supportare i figli\b", r"\bcome affrontare i problemi comportamentali dei bambini\b", r"\bquali sono le strategie per un'educazione positiva\b", r"\bcome migliorare la comunicazione con i figli\b", r"\bquali sono le risorse per i genitori\b", r"\bcome aiutare i bambini a svilupparsi\b"],
        "responses": [
            "Educare i bambini richiede pazienza, comprensione e coerenza. Stabilire regole chiare e sostenere positivamente è fondamentale.",
            "I migliori consigli per genitori includono ascoltare i tuoi figli, essere un buon esempio e offrire supporto e guida.",
            "Gestire le sfide della genitorialità può essere difficile, ma cercare risorse e supporto può aiutare.",
            "Le pratiche di parenting efficaci includono la comunicazione aperta e la costruzione di una relazione di fiducia.",
            "Supportare i figli e affrontare i problemi comportamentali con empatia e strategia può contribuire a una crescita sana."
        ]
    },
    {
        "tag": "relationships",
        "patterns": [r"\bcome migliorare le relazioni\b", r"\bquali sono i consigli per una relazione sana\b", r"\bcome risolvere i conflitti\b", r"\bquali sono le chiavi per una buona comunicazione\b", r"\bcome mantenere una relazione felice\b", r"\bquali sono i segnali di una relazione problematica\b", r"\bcome rafforzare il legame con il partner\b", r"\bcome gestire i problemi di coppia\b", r"\bquali sono le risorse per le relazioni\b", r"\bcome creare un rapporto sano\b"],
        "responses": [
            "Migliorare le relazioni richiede comunicazione aperta, empatia e tempo dedicato insieme.",
            "Per una relazione sana, è importante ascoltare e rispettare i bisogni e i sentimenti dell’altro.",
            "Risolvere i conflitti in modo costruttivo implica l’ascolto attivo e la ricerca di soluzioni condivise.",
            "La chiave per una buona comunicazione è essere chiari e onesti, e anche mostrare comprensione.",
            "Mantenere una relazione felice richiede impegno reciproco e la volontà di affrontare le sfide insieme."
        ]
    },
    {
        "tag": "shopping",
        "patterns": [r"\bquali sono i tuoi negozi preferiti\b", r"\bche cosa ti piace acquistare\b", r"\bquali sono le migliori offerte\b", r"\bcome risparmiare durante lo shopping\b", r"\bquali sono i prodotti più popolari\b", r"\bcome scegliere i migliori prodotti\b", r"\bquali sono le tendenze dello shopping\b", r"\bche cosa consiglieresti di comprare\b", r"\bcome fare acquisti online sicuri\b", r"\bquali sono le novità del mercato\b"],
        "responses": [
            "Non faccio shopping, ma posso aiutarti a trovare le migliori offerte e consigli sui prodotti.",
            "Per risparmiare durante lo shopping, cerca offerte e compara i prezzi tra diversi negozi.",
            "I prodotti più popolari possono variare, ma posso fornirti informazioni sulle tendenze attuali.",
            "Scegliere i migliori prodotti implica leggere recensioni e confrontare le caratteristiche.",
            "Acquistare online in modo sicuro include usare siti affidabili e proteggere le informazioni personali."
        ]
    },
    {
        "tag": "food",
        "patterns": [r"\bqual è il tuo piatto preferito\b", r"\bche tipo di cucina ti piace\b", r"\bquali sono i tuoi ingredienti preferiti\b", r"\bcome preparare una ricetta\b", r"\bquali sono i cibi più salutari\b", r"\bche cosa consigli per mangiare\b", r"\bquali sono le tendenze alimentari\b", r"\bcome cucinare piatti sani\b", r"\bquali sono i ristoranti migliori\b", r"\bcome fare una dieta equilibrata\b"],
        "responses": [
            "Non mangio, ma posso suggerirti ricette e piatti basati sulle tendenze culinarie attuali.",
            "Per una dieta equilibrata, cerca di includere una varietà di alimenti e mantieni porzioni moderate.",
            "Le tendenze alimentari cambiano, ma piatti sani e nutrienti sono sempre una buona scelta.",
            "Posso aiutarti a trovare ricette e consigli per una cucina sana e gustosa.",
            "I ristoranti migliori possono variare a seconda della tua posizione e dei tuoi gusti personali."
        ]
    }


]


# Funzione per ottenere una risposta in base al tag e al pattern
def get_response(user_input):
    user_input = user_input.lower()
    for item in patterns_responses:
        for pattern in item["patterns"]:
            if re.search(pattern, user_input):
                return random.choice(item["responses"])
    return "Mi dispiace, non ho capito."





# Funzione principale per gestire il chatbot
def francuzzo_chat():

    while True:
        user_input = input("Tu: ")
        if user_input == "help":
            print("Francuzzo: Ecco i comandi disponibili: \n exit (esci dal programma), help (vedi i comandi), organizer (apri menu organizzatore files), analisis (apri la console di analisi in cui puoi modificare il file di config ed accedere al log facilmente)")
            log_action("User command: help")
            francuzzo_chat()
        elif user_input == "analisis":
            admenu()
            log_action("ANALISIS MODE ACTIVATED")
            exit()


        elif user_input == "organizer":
            print("Aperta console organizer")
            log_action("opened organizer console")
            menu()

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
