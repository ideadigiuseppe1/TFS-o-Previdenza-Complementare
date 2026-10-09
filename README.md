# TFS o previdenza complementare?

Questo progetto nasce da una domanda molto semplice:

_**a parità di carriera lavorativa, sarebbe economicamente più conveniente per il lavoratore rimanere nel sistema TFS oppure disporre di un sistema TFR associato alla previdenza complementare?**_

La domanda, apparentemente semplice, richiede in realtà di mettere insieme aspetti previdenziali, retributivi, fiscali e finanziari. Il progetto cerca quindi di costruire un modello quantitativo che permetta di confrontare i due sistemi mantenendo il più possibile identiche le condizioni di partenza.

L'obiettivo non è dimostrare a priori che una delle due alternative sia migliore. L'obiettivo è costruire un modello trasparente, modificabile e riproducibile, nel quale il risultato dipenda dalle ipotesi inserite.

## Il problema

Il trattamento di fine servizio (TFS) rappresenta una componente importante della remunerazione differita per il personale che rimane assoggettato al relativo regime.

**La previdenza complementare segue invece una logica differente.**

In un ipotetico sistema basato su TFR e previdenza complementare, le somme destinate al TFR vengono accantonate progressivamente e investite nel tempo. Al TFR possono aggiungersi i contributi del lavoratore e un eventuale contributo datoriale, qui assunto come ipotesi di simulazione.

La differenza fondamentale tra i due sistemi riguarda quindi anche il meccanismo di accumulazione:

- il TFS viene stimato a partire dalla retribuzione utile e dagli anni di servizio, secondo la formula implementata e le relative semplificazioni;
- il TFR viene accantonato progressivamente;
- la previdenza complementare investe nel tempo il capitale accumulato;
- il risultato dipende dalla durata dell'investimento, dai rendimenti, dai costi e dalla fiscalità.

Il progetto nasce dall'esigenza di quantificare questa differenza.

## Una simulazione, non una previsione

Il modello non cerca di prevedere quale sarà il rendimento effettivo dei mercati finanziari nei prossimi decenni. Allo stesso modo, non pretende di stabilire che la previdenza complementare sia universalmente più conveniente del TFS.

La domanda affrontata è più circoscritta:

_**che cosa accadrebbe, secondo determinate ipotesi retributive, finanziarie e fiscali, se una carriera comparabile fosse svolta alternativamente nel regime TFS oppure nel regime TFR più previdenza complementare?**_

Per questo motivo le principali ipotesi vengono esplicitate e gli script Python utilizzati per le simulazioni sono resi disponibili nel repository. In questo modo è possibile modificare i parametri e verificare come cambiano i risultati.

## La struttura del progetto

Il progetto ricostruisce una carriera di riferimento nella Guardia di Finanza, con una progressione retributiva basata sui gradi e sugli assegni funzionali indicati nei parametri del modello. La carriera è applicata a quattro combinazioni di età d'ingresso e pensionamento:

| Scenario | Età d'ingresso | Età di pensionamento | Anni simulati |
|---|---:|---:|---:|
| 1 | 18 anni | 61 anni | 43 |
| 2 | 18 anni | 66 anni | 48 |
| 3 | 25 anni | 61 anni | 36 |
| 4 | 25 anni | 66 anni | 41 |

Gli scenari a 66 anni includono, per convenzione di modello, cinque anni aggiuntivi di ausiliaria. Durante questi anni il grado e la componente stipendiale di riferimento rimangono quelli massimi raggiunti, mentre continua ad applicarsi la crescita annua ipotizzata del 2,03%. Gli anni sono conteggiati nel modello ai fini dell'anzianità utile al TFS e continuano a generare i flussi di TFR e i contributi alla previdenza complementare ipotizzati. Questa rappresentazione non è un modello amministrativo completo dell'ausiliaria.

I quattro scenari non rappresentano quattro carriere differenti per struttura, ma quattro applicazioni dello stesso impianto di calcolo a diverse combinazioni di età d'ingresso e pensionamento.

## Carriera e retribuzione

La scelta di una carriera di riferimento è motivata dalla disponibilità di informazioni su gradi, anzianità, stipendio tabellare e assegni funzionali. La progressione e le tabelle utilizzate sono riportate nella Wiki del progetto.

Il modello usa due componenti della crescita retributiva:

1. la progressione di carriera, che modifica lo stipendio tabellare e l'assegno funzionale in relazione all'anzianità;
2. la crescita retributiva nel tempo, rappresentata da una rivalutazione composta del 2,03% annuo.

Il 2,03% è ricavato dal tasso annuo composto tra il primo e l'ultimo dato della serie storica utilizzata, dal 1° gennaio 2001 al 1° gennaio 2024. È un parametro di simulazione, non una previsione certa dei futuri rinnovi contrattuali. La procedura e i dati sono descritti nella Wiki del progetto.

## Il TFS

Il modello contiene un calcolo del TFS. Nella wiki è descritta la formula concretamente utilizzata, i riferimenti normativi relativi alla base contributiva, ai sei scatti e alla franchigia fiscale, nonché le semplificazioni che impediscono di interpretare l'output come una liquidazione ufficiale individuale.

## Il TFR e la previdenza complementare

Il percorso alternativo ipotizza il conferimento del TFR a una forma pensionistica complementare e un contributo dell'1% della RAL da parte del lavoratore. È inoltre ipotizzato un contributo datoriale dell'1% della RAL. Quest'ultimo è un parametro del caso di studio e non implica che il personale considerato disponga già di un fondo di categoria operativo che riconosca tale versamento.

Il montante viene investito secondo una strategia Life-Cycle, con rendimenti medi netti distinti per fascia d'età. I rendimenti vengono trattati come già al netto della tassazione annuale degli investimenti. Al pensionamento il modello utilizza una ripartizione di riferimento del 50% in capitale e 50% destinato alla rendita, nei limiti e con le semplificazioni esplicitati nella Wiki. Nella stessa Wiki viene documentata la ricostruzione dei rendimenti dei comparti azionario e obbligazionario, basata sui benchmark e sui fattori di normalizzazione.

## Risultati

I risultati dei quattro scenari sono disponibili nella Wiki (si, sempre lì). Si tratta di risultati modellistici, dipendenti dalle formule e dalle ipotesi adottate. Non rappresentano una previsione finanziaria garantita né una prova che uno dei due sistemi sia sempre più conveniente.

## Limiti e riproducibilità

Il modello utilizza un aumento dello stipendio, pari al 2.03% annuo, già dal primo anno, periodo in cui il neo-militare è allievo e - nei fatti - potrebbe non ricevere una crescita salariale pari al tasso scelto; non ricostruisce ogni passaggio di carriera con precisione semestrale e non riproduce integralmente tutti i dettagli amministrativi, fiscali e attuariali. In particolare, la base retributiva utile al TFS è approssimata tramite un coefficiente del 90% della RAL prima dell'applicazione dei sei scatti: questo coefficiente è una scelta del modello, non una percentuale stabilita direttamente dalla norma.

Le ipotesi, i parametri, il codice Python e le fonti devono rimanere modificabili e verificabili. Quando una formula o un riferimento normativo viene aggiornato, occorre rieseguire tutti e quattro gli scenari e riallineare la pagina dei risultati con gli output degli script.
