# ✈️ FLIGHT – Kaufrausch & Kassensturz

**Anna sucht Kaffee. Der CFO sucht sein Geld.** Ein deutschsprachiges E-Commerce-Portfolio von Amit Steinberg.

![Projektposter](assets/flight_poster.jpg)

## Direkt im Codespace starten

Repository in GitHub Codespaces öffnen. Die Devcontainer-Konfiguration installiert die Basis- und ML-Abhängigkeiten, startet Streamlit und gibt Port **8501** frei. Falls nötig:

```bash
bash setup.sh
bash start.sh
```

Für eine schlanke Installation genügt `bash setup.sh --base`. Die vollständige Codespace-Installation nutzt automatisch CPU-PyTorch. Bei manueller Einrichtung für die neuronalen Modelle zuerst die CPU-Version von PyTorch installieren, damit der Codespace keine unnötigen CUDA-Pakete lädt:

```bash
python -m pip install 'torch>=2.4,<3' --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements-ml.txt
```

## Oberfläche und Geschichte

Die Startseite erzählt acht Kapitel in einfacher Sprache, mit Geschäftsterminologie, technischen Erklärungen und Humor. Die zusätzlichen Arbeitsbereiche führen tatsächliche Berechnungen aus:

- **Trainingslabor:** Popularität, ItemKNN, Markov, kompakte BERT4Rec-/SASRec-artige Transformer und LightGCN mit Training und Testmetriken.
- **Suchstudio:** TF-IDF, optional mehrsprachige Sentence Transformers und CLIP-Text-Bild-Retrieval aus hochgeladenen Katalogbildern.
- **Marketinglabor:** T-Learner auf Criteo-Treatmentdaten, stratifizierter Train/Test-Split, IPW-Upliftkurve und AUUC oberhalb Zufall.
- **Evidenzstudio:** ESCI-Kandidatenranking und Difference-in-Differences per OLS mit HC3- oder Cluster-Standardfehlern.
- **Vorstellung:** Projektposter, sieben Folien, herunterladbare PowerPoint-Datei und gespeicherte Benchmarkprotokolle.

Story-Simulationen bleiben ausdrücklich als solche gekennzeichnet. Keine KI-Methode bekommt Ergebnisse zugeschrieben, die eine Heuristik berechnet hat.

## Öffentliche Datenquellen

Datensätze bleiben getrennte Aufgaben. Keine gemeinsame Kundenidentität wird erfunden. Rohdaten sind nicht im Repository enthalten. Externe Datenlizenzen gelten unabhängig vom Projektcode.

| Quelle | Eingabe | Aufgabe |
| --- | --- | --- |
| [Retailrocket](https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset) | events.csv: timestamp, visitorid, itemid, event | Zeitliche Empfehlungen |
| [REES46](https://rees46.com/en/datasets) | event_time, user_id, product_id, event_type | Zeitliche Empfehlungen |
| [Amazon-M2](https://github.com/HaitaoMao/Amazon-M2-Session-Recommendation) | prev_items, next_item, locale | Separater Session-Holdout |
| [Amazon Reviews 2023](https://amazon-reviews-2023.github.io/) | JSONL mit user_id, parent_asin, timestamp | Rezensionen als Interaktionsproxy |
| [Amazon ESCI](https://github.com/amazon-science/esci-data) | query_id, query, product_title, esci_label | Suchrelevanz E/S/C/I |
| [Criteo Uplift](https://huggingface.co/datasets/criteo/criteo-uplift) | f0–f11, treatment, conversion | Marketing-Uplift, CC-BY-NC-SA-4.0 |

Reviews sind keine vollständigen Käufe oder Klicks. Criteo wurde nichtuniform subsampelt und erlaubt keine Rekonstruktion der ursprünglichen Geschäftswirkung. Ein Datei-Präfix kann ausschließlich Treatment enthalten: Das Training bricht ohne beide Arme/Outcomes ab. Für aussagekräftige Resultate vollständige geeignete Daten verwenden, dann repräsentativ sampeln. Das optionale Fetch-Skript nimmt ein Präfix und dient nur dem Schema-/Zugangstest.

## Reproduzierbare Experimente

```bash
# Alle sechs Modelle: künstlicher Funktionstest, eine Epoche
python -m flightlab.cli --models Popularität ItemKNN Markov BERT4Rec SASRec LightGCN --epochs 1

# Echtes Retailrocket-Experiment
python -m flightlab.cli --input data/events.csv --source Retailrocket --limit 100000 --cases 300

# REES46
python -m flightlab.cli --input data/2019-Oct.csv --source REES46 --limit 100000

# Amazon-Rezensionen
python -m flightlab.cli --input data/reviews.jsonl --source 'Amazon Reviews 2023' --limit 100000

# Optional: kleine öffentliche Präfixe für Zugang und Schema laden
python -m pip install -r requirements-data.txt
python -m flightlab.fetch reviews --category All_Beauty --rows 20000 --out data/reviews.jsonl
python -m flightlab.fetch criteo --rows 20000 --out data/criteo.csv

# Tests
python -m unittest discover -s tests -v
```

Die CLI exportiert JSON-Protokolle und eigene Modellartefakte (JSON/NPZ, Torch state_dict). Keine fremden Pickle-Uploads laden. Große Daten/Modelle bleiben aus Git ausgeschlossen.

### Messprotokoll

Globaler zeitlicher 80/20-Split für Ereignisdaten. Vokabular, Graph und Modellparameter stammen aus Training. Testfälle laufen vorwärts mit inzwischen beobachteter Historie, ohne erneutes Fitten. Vollständiger Trainingskatalog, keine zufällig gesampelten Negativkandidaten. Wiederholte Artikel bleiben erlaubt. Kalte Zielartikel werden gezählt und aus warmen Recall/NDCG ausgeschlossen. Die ersten begrenzten Testfälle sind keine repräsentative Stichprobe. Amazon-M2 verwendet einen ausdrücklich nichtzeitlichen Session-Holdout und keinen offiziellen Challenge-Split.

### Modellgrenzen

Die neuronalen Modelle sind kompakte, eigenständige Implementierungen zur Portfolio-Demonstration. BERT nutzt Einzelmaskenrekonstruktion. SAS nutzt kausale Attention und nächste Artikel. LightGCN lernt mit BPR auf einem User-Item-Graphen; die Sessioninferenz mittelt Itemvektoren. Keine Behauptung einer paper-exakten Reproduktion oder Produktionsskalierung. Vollkatalog-Softmax und Auswertung sind für kleine bis mittlere Teilmengen gedacht. Hyperparameter nur auf einem zusätzlichen Validierungssplit auswählen, nicht auf den hier berichteten Testfällen.

## Deckungsbeitrag

Nettowerte ohne Umsatzsteuer. Erlös nach Rabatt/Retouren minus Wareneinsatz verkaufter Ware minus variable Abwicklung/Retourenkosten minus Werbung. Retourenware gilt im Szenario als wiederverkaufbar. Fixkosten fehlen. DB ist kein Unternehmensgewinn. Inkrementeller DB der Marketing-Simulation: `(p1-p0) × 40 € − p1 × Rabatt − Kontaktkosten`. Alle Kosteneingaben sind sichtbare Annahmen.

## Struktur

```text
app.py                  Deutsche Story mit acht Kapiteln
pages/                  Training, Suche, Marketing, Ökonometrie, Präsentation
flightlab/              Datenadapter, Baselines, neuronale Modelle, Evaluation
assets/                 Projektposter, Präsentation und Folien
artifacts/              Lokale Laufprotokolle und Modelle, nicht versioniert
docs/benchmarks/        Ausgewählte ausgeführte und eingeordnete Protokolle
tests/                  GUI-, Daten-, Metrik- und Modellprüfungen
```

API-Schlüssel sind nicht erforderlich. Sentence Transformers/CLIP laden öffentliche Gewichte beim ersten Aufruf. Die App sendet Uploads nicht an eine Inferenz-API. Verarbeitung und Hosting sind im Betrieb dennoch datenschutzrechtlich zu prüfen. Für eine öffentliche Demo nur geeignete öffentliche oder künstliche Daten verwenden.
