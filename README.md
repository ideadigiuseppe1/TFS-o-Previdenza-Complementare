# TFS-o-Previdenza-Complementare
Questo progetto è un modello di simulazione finanziaria che valuta l'impatto economico di lungo periodo derivante dall'eventuale transizione del personale del Comparto Sicurezza e Difesa dall'attuale regime di Trattamento di Fine Servizio (TFS) al sistema di Trattamento di Fine Rapporto (TFR) integrato con la previdenza complementare negoziale.

🎯 Il senso del progetto
Il personale in regime di diritto pubblico si trova in una condizione di *stallo previdenziale*. Le proiezioni della Ragioneria Generale dello Stato evidenziano tassi di sostituzione del sistema pensionistico pubblico in costante contrazione. Il problema è amplificato per il comparto militare, caratterizzato da un accesso al pensionamento anagraficamente anticipato rispetto al mondo civile.

Il simulatore dimostra scientificamente l'esistenza di un doppio beneficio ottimale:
• Per il Lavoratore: a fronte di un contributo minimo (1% della RAL), si beneficia del contributo paritetico del datore di lavoro (1%) e della deducibilità fiscale IRPEF. Al posto del vecchio TFS (erogato a rate dallo Stato con anni di ritardo), il nuovo sistema basato su TFR e Fondo Pensione garantisce la liquidazione immediata del 60% dell'intero montante netto come capitale subito all'atto del pensionamento, mentre il restante 40% viene erogato come rendita vitalizia a integrazione della pensione.
• Per lo Stato: l'erogazione dei flussi correnti al Fondo Pensione genera un risparmio netto rispetto all'esborso differito delle ingenti liquidazioni TFS.

## 📚 Presupposti e contesto normativo
• Regime Pubblico (TFS): pari a 1/12 dell'80% dell'ultima retribuzione utile per gli anni di servizio.
• Maggiorazione Art. 6-bis D.L. 387/1987: il modello include per tutti gli scenari l'incremento del 15% (c.d. "sei scatt"i) sulla base computabile TFS. La condizione di accesso (35 anni di servizio o 55 anni di età alla cessazione per limiti di ordinamento) risulta verificata in ognuna delle simulazioni.
• Tassazione Differenziata: il TFS sconta la tassazione separata su base imponibile ridotta da franchigia. Il Fondo Pensione applica un'aliquota sostitutiva agevolata sul capitale che decresce dal 15% fino al 9% minimo in base agli anni di permanenza.

## 📊 Ipotesi finanziarie e metodologia
### 1. Dati Retributivi di Riferimento
* I parametri stipendiali inseriti originano dai dati ufficiali del **Ministero dell'Economia e delle Finanze (MEF)**.
* I flussi rispecchiano le progressioni storiche e i rinnovi contrattuali applicati al personale della **Guardia di Finanza**.
* Il modello isola la retribuzione tabellare, l'IIS conglobata e l'**Assegno Funzionale**. Quest'ultimo viene mantenuto nominalmente statico e **privo di rivalutazione contrattuale**, rispecchiando fedelmente le dinamiche reali post-2008.

### 2. Strategia di Investimento "Life Cycle" e Rendimenti Netti
* Il modello adotta una strategia multi-comparto mutuata dalle linee guida *Target Date* di Vanguard:
  * **Fino a 45 anni:** 100% Comparto Azionario.
  * **Da 46 a 50 anni:** 100% Profilo Bilanciato Dinamico (**70% Az. / 30% Obbl.**).
  * **Da 51 a 55 anni:** 100% Profilo Bilanciato Crescita (**50% Az. / 50% Obbl.**).
  * **Da 56 anni alla pensione:** 100% Profilo Bilanciato Prudente (**30% Az. / 70% Obbl.**).
* I rendimenti storici e i costi (**TER medio** del fondo negoziale Perseo-Sirio) sono estratti dalle Note Informative **COVIP**.
* I rendimenti sono stati normalizzati tramite un **Factor Drop** cautelativo per azzerare l'ottimismo da benchmark (abbattimento del **3,5%** annuo sull'azionario e dello **0,60%** sull'obbligazionario), incorporando l'imposta sostitutiva annua del **20%** e il *cash drag*.

### 3. Attualizzazione dei Ritardi dello Stato (VAN)
* Lo Stato eroga il TFS con differimenti normativi compresi tra **12 e 36 mesi** a seconda dell'importo lordo.
* Il simulatore calcola il **Valore Attuale Netto (VAN)** di tali flussi futuri differiti, utilizzando come tasso di sconto finanziario il **2,00%**, ancorato al target di stabilità monetaria della **Banca Centrale Europea (BCE)**. Ciò quantifica l'esatta perdita di potere d'acquisto reale dovuta al ritardo pubblico.

### 4. Fase di Rendita
* La conversione del **40% del montante netto** in rendita si basa sulle tabelle di mortalità **ISTAT aggiornate al 2026**.
* I coefficienti di trasformazione derivano dai prospetti ufficiali del Fondo Perseo-Sirio aggiornati al **6 ottobre 2026**. La rendita viene rivalutata a un tasso netto prudenziale del **2,00% annuo**.

---

## 🔬 Gli Scenari Analizzati

Il lavoro confronta i due regimi su **4 carriere**:

* **Scenario 1:** Arruolamento a 18 anni, pensionamento a 61 anni (Senza Ausiliaria).
* **Scenario 2:** Arruolamento a 18 anni, pensionamento a 66 anni (Con 5 anni di Ausiliaria).
* **Scenario 3:** Arruolamento a 25 anni, pensionamento a 61 anni (Senza Ausiliaria).
* **Scenario 4:** Arruolamento a 25 anni, pensionamento a 66 anni (Con 5 anni di Ausiliaria).

---

## 🛠️ Come utilizzare il progetto

### 💻 Per gli analisti (Uso dei file Python via Release)
Tutti gli script principali sono distribuiti all'interno delle Releases del progetto. Ogni release contiene il codice sorgente autoconsistente.

1. **Clonare la repository** e accedere alla cartella principale:
   ```bash
   git clone https://github.com/tuo-username/TFS-o-Previdenza-Complementare.git
   cd TFS-o-Previdenza-Complementare
   ```
2. Assicurarsi di aver posizionato i fogli parametrici nella cartella `dati/`.
3. **Eseguire lo script** d'interesse:
   ```bash
   python src/scenario_1.py
   ```
4. **Personalizzazione:** All'inizio di ogni file `.py` sono isolate le variabili globali (`ETA_INIZIALE`, `ETA_PENSIONAMENTO`, `TASSO_INFLAZIONE`). È possibile modificare liberamente tali valori numerici per adattare la proiezione a carriere personalizzate.

### 📄 Per i non addetti ai lavori (Guida PDF Prossimamente Disponibile)
Per chi non possiede competenze di programmazione o non ha installato l'ambiente Python sul proprio PC, verrà pubblicata all'interno delle Releases **un testo in PDF** . Questo documento conterrà i report testuali, i grafici di sintesi e la spiegazione di tutte le variabili calcolate dal motore algoritmico, rendendo lo studio pienamente accessibile.
