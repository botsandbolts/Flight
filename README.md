# FLIGHT · Annas Einkauf verständlich erklärt

Ein deutschsprachiges E-Commerce-Portfolio von Amit Steinberg. Anna sucht eine kleine Kaffeemaschine. Die Geschichte erklärt die Entscheidungen des Shops an diesem einen Einkauf.

![Anna im Beispielshop](assets/story_hero.jpg)

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

Die Startseite hat eine geführte Reihenfolge mit Vor-/Zurück-Navigation. Sie beginnt bei Annas Wunsch und erklärt sechs Entscheidungen: **Finden, Empfehlen, Rechnen, Rabatt entscheiden, Abstimmen und Prüfen**. Einstieg und Fazit rahmen diese Schritte ein.

Jeder Schritt zeigt ein konkretes Beispiel und eine erklärte Entscheidung. Geschäftliche Kennzahlen und technische Methoden sind optional aufklappbar. Vertiefende Werkzeuge stehen hinter einem eigenen Navigationsabschnitt. Die Präsentation folgt derselben Geschichte. Die letzten zwei Folien sind der technische Anhang.

Die zusätzlichen Arbeitsbereiche führen tatsächliche Berechnungen aus:

- **Trainingslabor:** Popularität, ItemKNN, Markov, kompakte BERT4Rec-/SASRec-artige Transformer und LightGCN mit Training und Testmetriken.
- **Suchstudio:** TF-IDF, optional mehrsprachige Sentence Transformers und CLIP-Text-Bild-Retrieval aus hochgeladenen Katalogbildern.
- **Marketinglabor:** T-Learner auf Criteo-Treatmentdaten, stratifizierter Train/Test-Split, IPW-Upliftkurve und AUUC oberhalb Zufall.
- **Evidenzstudio:** ESCI-Kandidatenranking und Difference-in-Differences per OLS mit HC3- oder Cluster-Standardfehlern.
- **Folien und Nachweise:** 15 neu geschriebene Folien, herunterladbare PowerPoint-Datei und getrennte Benchmarkprotokolle.

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

## Rechenbeispiele und Aussagegrenzen

Die Kostenrechnung verwendet eine separate runde Beispielbestellung von 100 € netto: 50 € Ware, 6 € Versand/Zahlung, 8 € erwartete Retourenkosten und 12 € Werbung. Damit bleiben 24 € vor Fixkosten. Ein Rabatt von 10 € lässt 14 € übrig. Das ist keine Behauptung über den zuvor gezeigten Artikelpreis oder echte Einkaufsmargen.

Die Gutscheinrechnung verwendet bekannte erfundene Wahrscheinlichkeiten: `(p1-p0) × 40 € − p1 × Gutschein − 0,20 € Kontaktkosten`. Bei 10 € Gutschein ergeben die Fälle 60 %/62 % und 10 %/25 % Zusatzbeiträge von −5,60 € beziehungsweise +3,30 € je Kontakt. Echte individuelle Gegenfälle sind nicht beobachtbar.

Im Bestandsbeispiel stehen 180 vorhandene Stück einem angenommenen Bedarf von 40 × 7 = 280 Stück gegenüber. Die Lücke beweist keinen individuellen Liefertermin. Im A/B-Lehrbeispiel sind 25/1000 und 29/1000 erfundene Käufe; deren Differenz von 0,4 Prozentpunkten belegt bei dieser Gruppengröße noch keinen positiven Effekt.

## Struktur

```text
app.py                  Geführte Geschichte: Einstieg, sechs Entscheidungen und Fazit
pages/                  Training, Suche, Marketing, Ökonometrie, Präsentation
flightlab/              Datenadapter, Baselines, neuronale Modelle, Evaluation
assets/                 Projektposter, Präsentation und Folien
artifacts/              Lokale Laufprotokolle und Modelle, nicht versioniert
docs/benchmarks/        Ausgewählte ausgeführte und eingeordnete Protokolle
tests/                  GUI-, Daten-, Metrik- und Modellprüfungen
```

API-Schlüssel sind nicht erforderlich. Sentence Transformers/CLIP laden öffentliche Gewichte beim ersten Aufruf. Die App sendet Uploads nicht an eine Inferenz-API. Verarbeitung und Hosting sind im Betrieb dennoch datenschutzrechtlich zu prüfen. Für eine öffentliche Demo nur geeignete öffentliche oder künstliche Daten verwenden.


## Weitere Anwendungen im Unternehmen

Zwölf optionale Fallkarten vertiefen Geschäftsprobleme anderer Abteilungen. Sie ergänzen die Geschichte, ohne den Einstieg zu unterbrechen. Weitere Arbeitsbereiche:

- **KI im Unternehmen:** Einkauf, Service, CRM, Content, Pricing, Recht, Wissensmanagement und Führung. Begriffe AI/KI, generative KI, Copilot, Agent, Workflow und RAG auf drei Erklärungsebenen.
- **Agenten-Kommandozentrale:** Fester lokaler Ablauf mit realen DB-/Meldebestand-Rechnungen, Handbuch-Retrieval und Entscheidungsprotokoll. Kein autonomer LLM-Agent und keine externen Aktionen.
- **Wissens- und Contentstudio:** Suche in einem synthetischen Handbuch und nachvollziehbare Marketingvorlagen. Keine erfundenen Produktclaims.
- **KI-Business-Case:** Nutzungsquote, Prüfzeit, realisierter Zeitwert, Tokenkosten, Betreuung und Amortisation mit sichtbaren Annahmen.

### Optionale Modellanbindungen

OpenAI Responses API und Anthropic Messages API können einen Entwurf aus dem sichtbaren Szenarioprotokoll erzeugen. Die Adapter werden nur auf ausdrücklichen Klick nach Auswahl von Anbieter und Modell-ID aufgerufen. Schlüssel gehören in Codespace-Secrets als `OPENAI_API_KEY` beziehungsweise `ANTHROPIC_API_KEY`, niemals ins Repository. Diese externen API-Wege wurden ohne Schlüssel nicht live getestet. ChatGPT/Claude-Abonnements und API-Abrechnung sind getrennte Zugänge. Keine pauschale Qualitätsrangliste der Anbieter. Gemini und lokale Modelle werden als Optionen erläutert, sind aber nicht implementiert.

Quellen: [OpenAI Tools](https://developers.openai.com/api/docs/guides/tools), [Anthropic Tool Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works).
