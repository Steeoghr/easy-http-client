
def get_html_table_data(html, table_key):
    dati = []
    element = html.find(table_key)

    if element is not None:
        print("Map table")
        dati = []
        # Trova tutte le righe della tabella
        righe = element.find_all('tr')
        for riga in righe:
            celle = riga.find_all('td')
            # Aggiungi solo celle non vuote
            dati.extend([cella.get_text(strip=True) for cella in celle if cella.get_text(strip=True)])
        return dati
    else:
        return None