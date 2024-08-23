import os
import re

class M_interpreter:
    # Dictionary of substitutions as a constant
    SUBSTITUTIONS = {
        'stampa': 'print',
        'se': 'if',
        'altrimenti': 'else',
        'altrimentise': 'elif',
        'definisci': 'def',
        'classe': 'class',
        'falso': 'False',
        'vero': 'True',
        'importa': 'import',
        'e': 'and',
        'stop': 'break',
        'mentre': 'while',
        'continua': 'continue',
        'perogni': 'for',
        'in': 'in',
        'ritorna': 'return',
        'prova': 'try',
        'eccetto': 'except',
        'finalmente': 'finally',
        'alza': 'raise',
        'con': 'with',
        'nonlocale': 'nonlocal',
        'globale': 'global',
        'lambda': 'lambda',
        'asincrono': 'async',
        'attendi': 'await',
        'non': 'not',
        'o': 'or',
        'è': 'is',
        'passa': 'pass',
        'aspetta': 'await',
        'asserisci': 'assert',
        'elimina': 'del',
        'nessuno': 'None'
    }

    def __init__(self, folder_name="File da interpretare"):
        self.folder_name = folder_name
        self.create_folder()

    def create_folder(self):
        """Creates the folder if it doesn't exist."""
        if not os.path.exists(self.folder_name):
            os.makedirs(self.folder_name)
            print(f"Directory '{self.folder_name}' created.")
        else:
            print(f"Directory '{self.folder_name}' already exists.")

    def replace_word(self, input_file, output_file):
        """
        Replaces Italian keywords in a file with corresponding English keywords.

        Args:
            input_file (str): The path of the input file.
            output_file (str): The path of the output file.
        """
        try:
            with open(input_file, 'r') as f_input:
                content = f_input.read()

            for italian_word, english_word in self.SUBSTITUTIONS.items():
                content = re.sub(r'\b' + re.escape(italian_word) + r'\b', english_word, content)

            with open(output_file, 'w') as f_output:
                f_output.write(content)

            print(f"Replacement completed. The resulting file has been saved as '{output_file}'.")

        except FileNotFoundError:
            print(f"Error: The file '{input_file}' was not found.")
        except Exception as e:
            print(f"Error: {e}")

    def process_files(self):
        """Processes all .M files in the directory."""
        for filename in os.listdir(self.folder_name):
            if filename.endswith('.M'):
                input_file = os.path.join(self.folder_name, filename)
                output_file = os.path.join(self.folder_name, filename.replace('.M', '_interpreted.py'))
                self.replace_word(input_file, output_file)







#Fine del codice
# ---------------------------------------------
# Copyright (c) 2024 Mario Pisano
#
# Questo programma è distribuito sotto la licenza EUPL, Versione 1.2 o – non appena 
# saranno approvate dalla Commissione Europea – versioni successive della EUPL 
# (la "Licenza");
# Puoi usare, modificare e/o ridistribuire il programma sotto i termini della 
# Licenza. 
# 
# Puoi trovare una copia della Licenza all'indirizzo:
# https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
