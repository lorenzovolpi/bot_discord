"""
Questo codice mostra come recuperare l'ora corrente in un certo fuso orario facendo web scraping.
L'idea è quella di scaricare la pagina web e cercare gli elementi opportuni nella pagina sfruttando
dei metodi forniti dalle librerie che andremo ad utilizzare.
Le librerie che useremo sono le seguenti:

    - requests: permette di scaricare facilmente una pagina web a partire dal link passato come parametro
    - BeautifulSoup: questa libreria si occupa di generare l'html finale della pagina web che abbiamo
                     scaricato, eseguendo ad esempio il codice javascript presente nella pagina che deve
                     essere interpretato al suo caricamento; in pratica fa quello che farebbe un browser, 
                     ma è molto più leggera. Inoltre esegue anche quella che gli autori della libreria
                     chiamano "prettyfication", ovvero semplifica il codice html finale della pagina scaricata
                     per renderlo più facilmente navigabile.
                     Questa libreria si occupa anche di eseguire automaticamente il
                     parsing della pagina html ottenuta in modo da ottenere un oggetto strutturato che rappresenta
                     l'html della pacina stessa e che possiamo navigare con degli opportuni metodi.
    - lxml: questa libreria viene usata come back-end da BeautifulSoup per effettuare il parsing della pagina html.

I pacchetti che contengono queste librerie possono essere installati con:

    pip install requests bs4 lxml

"""
import sys
import requests 
from bs4 import BeautifulSoup
import lxml

# l'url dal quale scarichiamo la pagina che ci interessa
URL = "https://time.is/" 

# questo dizionario rappresenta gli headers da passare a requests per scaricare la pagina web
# utilizzando questi headers il nostro codice convince il server di essere un browser
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"}

# la funzione che ci permette di ottenere l'orario online
#  - city: una stringa che viene appesa in fondo all'url e rappresenta il nome di una città in inglese
#          con la prima lettera maiuscola dove gli spazi devono essere sostituiti da '_'
def get_clock(city:str):
    try:
        # scarichiamo la pagina web all'url indicato, ad esempio se city="Rome", l'url diventa "https://time.is/Rome"
        page = requests.get(URL + city, headers = headers)
        # creiamo l'oggetto BeautifulSoup passando lxml come back-end
        # soup è l'oggetto che rappresenta l'intero DOM e al suo interno si possono effettuare delle ricerche
        # con i metodi indicati sotto
        soup = BeautifulSoup(page.content, "lxml")

        # utilizzando il metodo find cerchiamo il tag con l'id "clock"; l'oggetto restituito conterrà tutto
        # il sottoalbero del DOM radicato nel nodo cercato
        # utilizzi più completi di find e find_all(la variante che trova tutte le occorrenze specificate nel sottoalbero
        # radicato in soup) sono ad esempio:         
        #
        #   soup.find("nome_tag", id="nome_id", _class="nome_classe")
        #   soup.find_all("nome_tag", id="nome_id", _class="nome_classe")

        clock = soup.find(id="clock")

        # dato che il nodo ottenuto sarà del tipo <time id="clock">14:35:03</time> l'unica cosa che ci
        # rimane da fare è ottenere il testo contenuto accedendo al campo string di clock. Il metodo strip()
        # è un metodo sulle stringhe di python che permette di eliminare eventuali spazi iniziali o finali
        clock_str = clock.string.strip()

        return clock_str 
    
    except Exception as e:
        print(e)
        return None
     
def main(city:str):
    print("Time in", city.replace("_", " "), ":", get_clock(city))

if __name__ == "__main__":
    main(sys.argv[1])
