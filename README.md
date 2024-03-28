# EPICODE_Data-Analysis_Capstone


Per questo progetto di fine corso di Data Analysis tenuto da EPICODE, ho voluto realizzare un'analisi dell'offerta del mercato italiano degli immobili in vendita.

Per mettere alla prova le mie capacità e per approfondire determinati argomenti, ho voluto realizzare un algoritmo di scraping con Python sul sito immobiliare.it utilizzando anche la libreria Selenium.
Nella prima versione dello script, l'algoritmo filtrava gli annunci per regione e partendo dal primo annuncio raccoglieva i dati e passava all'annuncio successivo. In questo modo il programma andava in crash poiché determinati annunci andavano offline, sostituiti da una pagina informativa dalla quale non è possibile proseguire all'annuncio successivo né tantomeno tornare indietro.
Per evitare quindi di perdere il lavoro effettuato e per evitare che il programma raccogliesse gli stessi annunci più volte ho fatto sì che l'algoritmo filtrasse non solo per regione ma anche per fascia di prezzo di 1000€ esportando un file CSV per ognuna di queste  (es. Umbria: 1€-1000€, 1001€-2000€ e così via fino a raggiungere il prezzo massimo della regione filtrata).

I dati raccolti sono i seguenti: titolo annuncio, comune, località, tipologia contratto, tipologia immobile, prezzo, numero locali, numero bagni, piano, presenza di ascensore, tipologia riscaldamento, classe energetica.

È stato effettuato il debugging, i test e l'effettiva raccolta dei dati degli annunci contemporaneamente, ciò ha influenzato la pulizia del codice che verrà comunque successivamente pulito ed implementato.

Poiché l'algoritmo lavora su un'istanza di Chrome, di cui ho disabilitato la GUI, la velocità di raccolta è di circa 1,2 annunci al secondo con un consumo di circa 1,5 GB di RAM (eseguendo lo script da terminale anziché da IDE). Per accelerare il processo ho eseguito lo script su due PC in più terminali. Ho anche eseguito un test su un'istanza EC2 gratuita di AWS che avendo però un solo GB di RAM non ha ottenuto risultati interessanti.
Ritengo quindi che ci sia ancora un grosso margine per rendere più efficiente l'algoritmo.

Una volta raccolti i 750 mila annunci sono passato alla fase di ETL utilizzando Power Query in Power BI utilizzando come connettore la directory. Una volta combinati tutti i file CSV della prima regione ho pulito e preparato i dati. È stato poi sufficiente copiare il codice M e copiarlo su una nuova Query vuota per ottenere gli stessi passaggi applicati ed avere uniformità. Dopo aver creato una Query per ogni regione le ho accodate per avere un'unica entità dei fatti per lo star scheme. Ho inoltre scaricato un db normalizzato dei comuni italiani (autore: Garda Informatica) che ho denormalizzato in Power Query per ottenere la gerarchia regione-provincia-comune con la quale applicare filtri e non solo.

Al momento il report di Power BI consta di quattro pagine:
1. analisi della distribuzione geografica del numero di annunci e quindi di immobili in vendita.
2. Analisi della distribuzione del numero di annunci in base al prezzo con la presenza di indicatori statistici di base.
3. Analisi del prezzo medio al mq per area geografica e per tipologia di immobile.
4. Analisi sulla classe energetica degli immobili in vendita, in particolare il numero e il rispettivo prezzo al mq. (Questa analisi è stata fatta non sul totale degli annunci bensì sui circa 195 mila annunci nella quale era presente questa informazione)


Ringrazio EPICODE e i suoi docenti per aver tenuto questo corso durante il quale ho acquisito molte conoscenze informatiche e una metodologia all'analisi dei dati.