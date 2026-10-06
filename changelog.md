# Changelog
Tutte le modifiche effettuate in questo progetto saranno documentate in questo file.

## 01-07-2026
In questo mese è stata scritta la base del codice, creato il file "issues" dove ci sono tutte le future funzioni e tutto quello che devo implementare nel tempo.
## 06-10-2026
Nell'aggiornamento al codice del 06.10.2026, ci sono state queste modifiche:
- lo stipendio, ai fini del calcolo del TFS, viene corretto e considerato al 90% visto che, per legge, le indennità accessorie variabili vengono escluse da tale calcolo.
- sempre ai fini del TFS, viene applicata la maggiorazione dei "sei scatti" (ex art. 6-bis DL 387/1987)
- verificato e confermato il modello matematico-normativo per la tassazione al momento del riscatto del Fondo Pensione (9% su contributi e TFR confluiti, le plusvalenze esenti perché già viene utilizzato un rendimento al netto delle imposte)
- aggiornato l'intero motore di calcolo della previdenza complementare integrando le metriche reali del Fondo Perseo Sirio (ottobre 2026): implementati i coefficienti attuariali di conversione in rendita mensile (comprensivi di caricamento implicito dell'1,30%) per le età di 61 e 66 anni con tasso tecnico allo 0%. Fissato prudenzialmente al 2,00% il tasso annuo di rivalutazione netta della rendita erogata, basato sullo storico della Gestione Separata UnipolSai FONDICOLL al netto dei costi di gestione.
