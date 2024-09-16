def read_file(filename):
    """Legge il contenuto da un file di testo."""
    try:
        with open(filename, 'r') as file:
            return file.read().strip()
    except IOError as e:
        print(f"Si è verificato un errore durante la lettura del file {filename}: {e}")
        return None

def write_file(filename, content):
    """Scrive il contenuto in un file di testo."""
    try:
        with open(filename, 'w') as file:
            file.write(content)
        print(f"Contenuto scritto con successo nel file {filename}")
        return True
    except IOError as e:
        print(f"Si è verificato un errore durante la scrittura nel file {filename}: {e}")
        return False

# Esempio di utilizzo
if __name__ == "__main__":
    # Esempio di scrittura
    content_to_write = "Questo è un esempio di contenuto da scrivere nel file."
    if write_file("example.txt", content_to_write):
        print("Scrittura completata.")
    
    # Esempio di lettura
    read_content = read_file("example.txt")
    if read_content is not None:
        print(f"Contenuto letto dal file: {read_content}")