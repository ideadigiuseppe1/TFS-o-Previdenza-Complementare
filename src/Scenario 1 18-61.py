# =====================================================================
#  SCENARIO 1: Da 18 a 61 anni  |  TFS vs TFR + Fondo Pensione
# =====================================================================

# --- PARAMETRI DELLO SCENARIO ---
ETA_INIZIALE = 18
ETA_PENSIONAMENTO = 61
ANNI_ASPETTATIVA_VITA = 24.884
COEFFICIENTE_PERSEO = 35.15255  # per mille, relativo all'età di pensionamento


def calcola_irpef(imponibile):
    """Scaglioni IRPEF 2026: 23% fino a 28k, 33% fino a 50k, 43% oltre."""
    if imponibile <= 0:
        return 0.0
    tasse = 0.0
    if imponibile > 50000:
        tasse += (imponibile - 50000) * 0.43
        imponibile = 50000
    if imponibile > 28000:
        tasse += (imponibile - 28000) * 0.33
        imponibile = 28000
    tasse += imponibile * 0.23
    return tasse


def aliquota_media_irpef(imponibile):
    """Aliquota media effettiva IRPEF su un dato imponibile."""
    if imponibile <= 0:
        return 0.0
    return calcola_irpef(imponibile) / imponibile


def ottieni_ral_militare_base(anni_servizio):
    """RAL base per gli anni di servizio (poi rivalutata del 2.03% annuo)."""
    if anni_servizio < 0.5:
        stipendio_m, assegno_a = 1268.95, 0.0
    elif anni_servizio < 2:
        stipendio_m, assegno_a = 1714.80, 0.0
    elif anni_servizio < 4:
        stipendio_m, assegno_a = 2032.39, 0.0
    elif anni_servizio < 10:
        stipendio_m, assegno_a = 2134.21, 0.0
    elif anni_servizio < 17:
        stipendio_m, assegno_a = 2174.94, 0.0
    elif anni_servizio < 25:
        stipendio_m, assegno_a = 2240.10, 1829.4
    elif anni_servizio < 29:
        stipendio_m = 2337.85
        assegno_a = 3070.5 if anni_servizio >= 27 else 1829.4
    else:
        stipendio_m = 2411.17
        assegno_a = 3082.5 if anni_servizio < 32 else 3543.03
    return stipendio_m * 13 + assegno_a


def get_rendimento_fp(eta):
    """Rendimenti NETTI (già al netto dell'imposta sui rendimenti del fondo)."""
    if eta <= 45:
        return 0.0502
    elif eta <= 50:
        return 0.0437
    elif eta <= 55:
        return 0.0309
    return 0.0232


def simula_mondo_parallelo():
    eta_iniziale = ETA_INIZIALE
    eta_pensionamento = ETA_PENSIONAMENTO
    anni_servizio = eta_pensionamento - eta_iniziale
    anni_aspettativa_vita = ANNI_ASPETTATIVA_VITA
    tasso_inflazione = 0.02
    tasso_rivalutazione_stipendi = 0.0203
    franchigia_tfs_per_anno = 309.87

    storia_ral = []
    totale_netto_nominale_tfs = totale_netto_reale_tfs = 0.0
    totale_netto_nominale_fp = totale_netto_reale_fp = 0.0
    montante_fp_totale = totale_contributi_versati = 0.0
    totale_tfr_versato = totale_contributo_datore = totale_contributo_dipendente = 0.0

    # ---------------- SIMULAZIONE ANNO PER ANNO ----------------
    for anno in range(anni_servizio):
        eta = eta_iniziale + anno
        ral = ottieni_ral_militare_base(anno) * ((1 + tasso_rivalutazione_stipendi) ** anno)
        storia_ral.append(ral)

        inps = ral * 0.088
        fattore_sconto = (1 + tasso_inflazione) ** anno

        # Scenario TFS
        netto_tfs = ral - inps - calcola_irpef(ral - inps)
        totale_netto_nominale_tfs += netto_tfs
        totale_netto_reale_tfs += netto_tfs / fattore_sconto

        # Scenario TFR + Fondo Pensione
        contributo_dipendente = ral * 0.01
        contributo_datore = ral * 0.01
        imponibile_fp = ral - inps - contributo_dipendente
        netto_fp = ral - inps - calcola_irpef(imponibile_fp) - contributo_dipendente
        totale_netto_nominale_fp += netto_fp
        totale_netto_reale_fp += netto_fp / fattore_sconto

        tfr_annuo = (ral / 13.5) - (ral * 0.005)
        flusso_anno = contributo_dipendente + contributo_datore + tfr_annuo

        totale_tfr_versato += tfr_annuo
        totale_contributo_datore += contributo_datore
        totale_contributo_dipendente += contributo_dipendente

        montante_fp_totale *= (1 + get_rendimento_fp(eta))  # rivaluta il montante esistente
        montante_fp_totale += flusso_anno
        totale_contributi_versati += flusso_anno

    ultima_ral = storia_ral[-1]

    # ---------------- 1. TFS — Tassazione separata ----------------
    quota_base_computabile = 0.90
    maggiorazione_sei_scatti = 1.15
    base_tfs_finale = ultima_ral * quota_base_computabile * maggiorazione_sei_scatti
    tfs_lordo = (1.0 / 12.0) * 0.80 * base_tfs_finale * anni_servizio

    franchigia_totale = franchigia_tfs_per_anno * anni_servizio
    base_imponibile_tfs = max(0.0, tfs_lordo - franchigia_totale)
    reddito_riferimento = (base_imponibile_tfs / anni_servizio) * 12
    aliquota_tfs = aliquota_media_irpef(reddito_riferimento)
    imposta_tfs = base_imponibile_tfs * aliquota_tfs
    tfs_netto = tfs_lordo - imposta_tfs

    def sconto(n):
        return (1 + tasso_inflazione) ** (anni_servizio + n)

    if tfs_lordo <= 50000:
        payout_desc = f"1 Rata (dopo 12 mesi): € {tfs_netto:,.2f}"
        tfs_netto_reale = tfs_netto / sconto(1)
    elif tfs_lordo <= 100000:
        quota1 = tfs_netto * 50000 / tfs_lordo
        quota2 = tfs_netto - quota1
        payout_desc = f"2 Rate: dopo 12 mesi € {quota1:,.2f} | dopo 24 mesi € {quota2:,.2f}"
        tfs_netto_reale = quota1 / sconto(1) + quota2 / sconto(2)
    else:
        quota1 = tfs_netto * 50000 / tfs_lordo
        quota2 = tfs_netto * 50000 / tfs_lordo
        quota3 = tfs_netto - quota1 - quota2
        payout_desc = (f"3 Rate: dopo 12 mesi € {quota1:,.2f} | dopo 24 mesi € {quota2:,.2f} "
                       f"| dopo 36 mesi € {quota3:,.2f}")
        tfs_netto_reale = quota1 / sconto(1) + quota2 / sconto(2) + quota3 / sconto(3)

    # ---------------- 2. FONDO PENSIONE — 60% capitale / 40% rendita ----------------
    plusvalenza_netta = montante_fp_totale - totale_contributi_versati
    sconto_fp = min(0.06, max(0.0, (anni_servizio - 15) * 0.003))
    aliquota_fp = 0.15 - sconto_fp  # minimo 9%

    imposta_fp = totale_contributi_versati * aliquota_fp
    montante_fp_netto = montante_fp_totale - imposta_fp

    lump_sum_fp = montante_fp_netto * 0.60
    capitale_per_rendita = montante_fp_netto * 0.40
    lump_sum_fp_reale = lump_sum_fp / ((1 + tasso_inflazione) ** anni_servizio)

    rendita_annua_iniziale = capitale_per_rendita * (COEFFICIENTE_PERSEO / 1000.0)
    tasso_rivalutazione_rendita = 0.02

    rendita_totale_nominale = rendita_totale_reale = 0.0
    storia_rendite = []
    anni_rendita_int = int(anni_aspettativa_vita)
    fraz = anni_aspettativa_vita - anni_rendita_int
    rendita_corrente = rendita_annua_iniziale

    for k in range(1, anni_rendita_int + 1):
        r_reale = rendita_corrente / ((1 + tasso_inflazione) ** (anni_servizio + k))
        rendita_totale_nominale += rendita_corrente
        rendita_totale_reale += r_reale
        storia_rendite.append({'k': k, 'eta': eta_pensionamento + k,
                               'nominale': rendita_corrente, 'reale': r_reale})
        rendita_corrente *= (1 + tasso_rivalutazione_rendita)

    if fraz > 0:
        k = anni_rendita_int + 1
        rata_nom = rendita_corrente * fraz
        rata_reale = rata_nom / ((1 + tasso_inflazione) ** (anni_servizio + k))
        rendita_totale_nominale += rata_nom
        rendita_totale_reale += rata_reale
        storia_rendite.append({'k': k, 'eta': eta_pensionamento + k,
                               'nominale': rata_nom, 'reale': rata_reale})

    rendita_mensile_nominale = rendita_annua_iniziale / 12

    # ---------------- COSTO PER LO STATO ----------------
    costo_stato_tfs_lordo = tfs_lordo
    incasso_fiscale_tfs = imposta_tfs
    costo_stato_tfs_netto = tfs_lordo - imposta_tfs

    costo_stato_fp_lordo = totale_tfr_versato + totale_contributo_datore
    quota_stato = costo_stato_fp_lordo / totale_contributi_versati if totale_contributi_versati > 0 else 0.0
    incasso_fiscale_fp_su_quota_stato = imposta_fp * quota_stato
    costo_stato_fp_netto = costo_stato_fp_lordo - incasso_fiscale_fp_su_quota_stato

    # ---------------- METRICHE TOTALI ----------------
    valore_attuale_fp = lump_sum_fp_reale + rendita_totale_reale
    tot_nom_tfs = totale_netto_nominale_tfs + tfs_netto
    tot_nom_fp = totale_netto_nominale_fp + lump_sum_fp + rendita_totale_nominale
    tot_rea_tfs = totale_netto_reale_tfs + tfs_netto_reale
    tot_rea_fp = totale_netto_reale_fp + lump_sum_fp_reale + rendita_totale_reale
    m_nom_tfs = totale_netto_nominale_tfs / anni_servizio
    m_nom_fp = totale_netto_nominale_fp / anni_servizio
    m_rea_tfs = totale_netto_reale_tfs / anni_servizio
    m_rea_fp = totale_netto_reale_fp / anni_servizio

    # ---------------- CONTROLLI DI COERENZA ----------------
    assert abs(montante_fp_totale - (totale_contributi_versati + plusvalenza_netta)) < 1e-6
    assert abs(totale_contributi_versati - (totale_tfr_versato + totale_contributo_datore
                                            + totale_contributo_dipendente)) < 1e-6
    assert abs(lump_sum_fp + capitale_per_rendita - montante_fp_netto) < 1e-6
    assert abs(sum(r['nominale'] for r in storia_rendite) - rendita_totale_nominale) < 1e-6
    assert abs(sum(r['reale'] for r in storia_rendite) - rendita_totale_reale) < 1e-6

    # ---------------- REPORT ----------------
    L = 85
    eur = lambda x, d=0: f"€ {x:,.{d}f}"
    fattore_fine = (1 + tasso_inflazione) ** anni_servizio

    print("=" * L)
    print("    CONFRONTO MILITARE: SCENARIO TFS vs TFR + FONDO PENSIONE")
    print("=" * L)
    print(f"  Carriera            : Da {eta_iniziale} a {eta_pensionamento} anni ({anni_servizio} anni di servizio)")
    print(f"  Rivalutazione stip. : +{tasso_rivalutazione_stipendi*100:.2f}% annuo")
    print(f"  Inflazione          : +{tasso_inflazione*100:.2f}% annuo")
    print(f"  RAL Anno 1 (2026)   : {eur(storia_ral[0], 2)}")
    print(f"  Ultima RAL Nominale : {eur(ultima_ral, 2)}")
    print(f"  Ultima RAL Reale    : {eur(ultima_ral / fattore_fine, 2)}")
    print("-" * L)

    print(f"\n>>> 1. FLUSSI DI CASSA DURANTE LA CARRIERA ({anni_servizio} anni)")
    print(f"  {'':>38}{'TFS':>18}{'TFR+FP':>18}{'Delta':>18}")
    for lab, a, b, d in [
        ("Totale Netto Nominale", totale_netto_nominale_tfs, totale_netto_nominale_fp, 0),
        ("Totale Netto Reale (€ oggi)", totale_netto_reale_tfs, totale_netto_reale_fp, 0),
        ("Media Annua Nominale", m_nom_tfs, m_nom_fp, 2),
        ("Media Annua Reale (€ oggi)", m_rea_tfs, m_rea_fp, 2),
    ]:
        print(f"  {lab:>38}{eur(a, d):>18}{eur(b, d):>18}{eur(b - a, d):>18}")

    print("-" * L)
    print("\n>>> 2. LIQUIDAZIONE TFS (SCENARIO ATTUALE)")
    print(f"  Ultima RAL di fine carriera      : {eur(ultima_ral, 2)}")
    print(f"  Base Computabile TFS ({quota_base_computabile*100:.0f}% RAL)   : {eur(ultima_ral * quota_base_computabile, 2)}")
    print(f"  Maggiorazione 6 Scatti (+{(maggiorazione_sei_scatti-1)*100:.0f}%)    : {eur(base_tfs_finale, 2)}")
    print(f"  TFS Lordo Spettante (80% di 1/12): {eur(tfs_lordo, 2)}")
    print(f"  Franchigia (€{franchigia_tfs_per_anno:.2f} × {anni_servizio} anni)   : {eur(franchigia_totale, 2)}")
    print(f"  Base Imponibile TFS              : {eur(base_imponibile_tfs, 2)}")
    print(f"  Reddito di Riferimento           : {eur(reddito_riferimento, 2)}")
    print(f"  Aliquota Media Tass. Separata    : {aliquota_tfs*100:.2f}%")
    print(f"  Imposta TFS                      : {eur(imposta_tfs, 2)}")
    print(f"  TFS NETTO LIQUIDATO              : {eur(tfs_netto, 2)}")
    print(f"  TFS Netto Reale (€ oggi)         : {eur(tfs_netto_reale, 2)}")
    print(f"  Erogazione                       : {payout_desc}")

    print("-" * L)
    print("\n>>> 3. FONDO PENSIONE (SCENARIO IPOTETICO)")
    print("  --- Composizione Montante ---")
    print(f"  Contributi Versati (dip+datore+TFR) : {eur(totale_contributi_versati, 2)}")
    print(f"  Plusvalenze Nette (già tassate)     : {eur(plusvalenza_netta, 2)}")
    print(f"  MONTANTE TOTALE LORDO               : {eur(montante_fp_totale, 2)}")
    print("\n  --- Tassazione al Riscatto ---")
    print(f"  Aliquota agevolata (dopo {anni_servizio} anni)   : {aliquota_fp*100:.2f}%")
    print(f"  Base imponibile (solo contributi)   : {eur(totale_contributi_versati, 2)}")
    print(f"  Imposta al riscatto                 : {eur(imposta_fp, 2)}")
    print(f"  Plusvalenze (esenti, già tassate)   : {eur(plusvalenza_netta, 2)}")
    print(f"  MONTANTE NETTO DISPONIBILE          : {eur(montante_fp_netto, 2)}")
    print("\n  --- Erogazione ---")
    print(f"  60% Capitale (lump sum subito)      : {eur(lump_sum_fp, 2)}")
    print(f"       → in € oggi                    : {eur(lump_sum_fp_reale, 2)}")
    print(f"  40% Rendita Vitalizia ({anni_aspettativa_vita:.1f} anni)  :")
    print(f"       Rendita annua iniziale         : {eur(rendita_annua_iniziale, 2)}")
    print(f"       Rendita mensile iniziale       : {eur(rendita_mensile_nominale, 2)}")
    print(f"       Totale rendite nominali        : {eur(rendita_totale_nominale, 2)}")
    print(f"       Totale rendite reali (€ oggi)  : {eur(rendita_totale_reale, 2)}")
    print("\n  --- Valore Attuale di tutti i pagamenti futuri (capitale + rendite) ---")
    print(f"  VA Lump Sum                         : {eur(lump_sum_fp_reale, 2)}")
    print(f"  VA Rendite                          : {eur(rendita_totale_reale, 2)}")
    print(f"  VA TOTALE FONDO PENSIONE            : {eur(valore_attuale_fp, 2)}")

    print("-" * L)
    print("\n>>> 4. TOTAL RETURN VITA INTERA")
    print("  (Somma stipendi netti + liquidazione/rendite)")
    print(f"  {'':>42}{'TFS':>20}{'TFR+FP':>20}")
    print(f"  {'TOTALE NOMINALE':>42}{eur(tot_nom_tfs):>20}{eur(tot_nom_fp):>20}")
    print(f"  {'TOTALE REALE (€ oggi)':>42}{eur(tot_rea_tfs):>20}{eur(tot_rea_fp):>20}")
    v_nom = tot_nom_fp - tot_nom_tfs
    v_rea = tot_rea_fp - tot_rea_tfs
    print("\n  VANTAGGIO GLOBALE FONDO PENSIONE:")
    print(f"    Nominale : {'+ ' if v_nom >= 0 else ''}{eur(v_nom, 2)}")
    print(f"    Reale    : {'+ ' if v_rea >= 0 else ''}{eur(v_rea, 2)} (potere d'acquisto odierno)")

    print("-" * L)
    print("\n>>> 5. ANALISI COSTO PER LO STATO (DATORE DI LAVORO PUBBLICO)")
    print("  [SCENARIO TFS]")
    print(f"    Costo Lordo per lo Stato          : {eur(costo_stato_tfs_lordo, 2)}")
    print(f"    Ritenute IRPEF incassate          : -{eur(incasso_fiscale_tfs, 2)}")
    print(f"    Costo Netto effettivo per Stato   : {eur(costo_stato_tfs_netto, 2)}")
    print("\n  [SCENARIO TFR + FONDO PENSIONE]")
    print(f"    Totale TFR maturato e versato     : {eur(totale_tfr_versato, 2)}")
    print(f"    Totale Contributo 1% Datore       : {eur(totale_contributo_datore, 2)}")
    print(f"    Costo Lordo per lo Stato          : {eur(costo_stato_fp_lordo, 2)}")
    print(f"    Imposta al riscatto su quota Stato: -{eur(incasso_fiscale_fp_su_quota_stato, 2)}")
    print(f"    Costo Netto effettivo per Stato   : {eur(costo_stato_fp_netto, 2)}")
    d_lordo = costo_stato_fp_lordo - costo_stato_tfs_lordo
    d_netto = costo_stato_fp_netto - costo_stato_tfs_netto
    print("\n  [CONFRONTO IMPATTO PER LE CASSE DELLO STATO]")
    print(f"    Differenza Costo Lordo (FP vs TFS): {'+ ' if d_lordo >= 0 else ''}{eur(d_lordo, 2)}")
    print(f"    Differenza Costo Netto (FP vs TFS): {'+ ' if d_netto >= 0 else ''}{eur(d_netto, 2)}")
    if d_netto < 0:
        print(f"    --> Il passaggio a TFR+FP FA RISPARMIARE allo Stato {eur(abs(d_netto), 2)} netti per dipendente.")
    else:
        print(f"    --> Il passaggio a TFR+FP COSTA allo Stato {eur(d_netto, 2)} netti in più per dipendente.")
    print("=" * L)

    print("\n>>> APPENDICE: Rendita FP — Prime e ultime 5 rate attualizzate")
    print(f"  {'#':>6}{'Età':>6}{'Nominale':>18}{'Reale (€ oggi)':>20}")
    n = len(storia_rendite)
    righe = list(range(min(5, n)))
    if n > 10:
        righe.append(None)
    righe += list(range(max(5, n - 5), n))
    for i in righe:
        if i is None:
            print(f"  {'...':>6}{'...':>6}{'...':>18}{'...':>20}")
        else:
            r = storia_rendite[i]
            print(f"  {r['k']:>6}{r['eta']:>6}{eur(r['nominale'], 2):>18}{eur(r['reale'], 2):>20}")

    print("\n>>> APPENDICE: Composizione Montante Fondo Pensione")
    print(f"  Contributi dipendente (1% RAL)       : {eur(totale_contributo_dipendente, 2)}")
    print(f"  Contributi datore (1% RAL)           : {eur(totale_contributo_datore, 2)}")
    print(f"  Quote TFR versate                    : {eur(totale_tfr_versato, 2)}")
    print("  ─────────────────────────────────────")
    print(f"  Totale contributi                    : {eur(totale_contributi_versati, 2)}")
    print(f"  Plusvalenze nette (rendimenti)       : {eur(plusvalenza_netta, 2)}")
    print("  ─────────────────────────────────────")
    print(f"  Montante a scadenza                  : {eur(montante_fp_totale, 2)}")
    print(f"  Imposta {aliquota_fp*100:.0f}% su contributi             : -{eur(imposta_fp, 2)}")
    print("  Imposta su plusvalenze               : € 0.00 (già tassate anno per anno)")
    print("  ═════════════════════════════════════")
    print(f"  MONTANTE NETTO                       : {eur(montante_fp_netto, 2)}")
    print("=" * L)


simula_mondo_parallelo()
