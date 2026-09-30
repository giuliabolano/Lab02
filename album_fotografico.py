def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    #legge il file CSV specificato da file_path e costruisce la struttura dati dell'album

    try:
        with open(file_path, "r") as f: #aprire il file in modalità lettura
            righe= f.readlines()
    except FileNotFoundError: #se il file non esiste si intercetta l'errore
           return None

    album= [] #inizializzare una lista vuota
    for riga in righe[1:]: #salta la prima riga che è di intestazione
        riga=riga.strip() #per ciascuna riga rimuove gli spazi e invii a capo
        if not riga:
            continue

        parti = riga.split(",") #divide nelle sue componenti estraendo i campi
        # creazione di un dizionario foto, nel quale si salvano i dettagli di ogni foto
        foto={
            "codice": parti[0].strip(),
            "titolo": parti[1].strip(),
            "autore": parti[2].strip(),
            "mese": int(parti[3].strip()),
            "anno": int(parti[4].strip())
        }
        album.append(foto)

    return album #album completo


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    #inserisce una nuova foto sia nel file CSV sia nella struttura dati album in memoria

    #controllare che il mese sia valido sennò interrompere l'esecuzione
    if mese <1 or mese >12:
        return None

    #controllare che il codice sia univoco, se questo è già presente nell'album allora annula l'operazione
    for foto in album:
        if foto["codice"]==codice:
                return None
#scrittura su file
    try:
        with open(file_path, "a") as file: #si apre il file in modalità di aggiunta (scrittura)
            file.write(f"{codice},{titolo},{autore},{mese},{anno}\n") #scrive in fondo al file la nuova riga formattata
    except FileNotFoundError:
        return None

    #aggiornamento dell'album in memoria
    #crea il diz nuova_foto con i dati dell'immagine
    nuova_foto={
        "codice": codice,
        "titolo": titolo,
        "autore": autore,
        "mese": mese,
        "anno": anno
    }
    album.append(nuova_foto)

    return nuova_foto #restituisce nuova_foto appena inserita


def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    #cerca una foto nell'album in base al suo codice univoco

    #scorre le foto nell'album e confronta ciascuna foto col codice dato
    for foto in album:
        if foto["codice"]==codice:
            return f"{foto['codice']}, {foto['titolo']}, {foto['autore']}, {foto['mese']}. {foto['anno']}"

    return None #restituisce none se non viene trovata nessuna foto corrispondente


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    #restituisce l'elenco dei titoli delle foto scattate in un determinato anno, ordinate in ordine alfabetico

#estrae solo i titoli di tutte le foto appartenenti a quell'anno
    titoli=[]
    #scorre tutte le foto nella lista
    for foto in album:
        #se l'anno corrisponde aggiunge il titolo
        if foto["anno"]== anno:
            titoli.append(foto["titolo"])
        #se non è stata trovata nessuna foto per quell'anno
    if not titoli:
        return None

    titoli.sort() #li ordina alfabeticamente
    return titoli


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
