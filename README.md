# ✈️ Flight – Kaufrausch & Kassensturz

Ein deutschsprachiges Streamlit-Portfolio von Amit Steinberg: Vom Kundenverhalten zum Deckungsbeitrag. Acht Kapitel erzählen eine zusammenhängende Geschichte mit interaktiven Entscheidungen, Humor und drei Erklärungsebenen: einfach, geschäftlich, technisch.

## Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

Python 3.11 empfohlen. Kein GPU, API-Schlüssel oder Datendownload erforderlich. In GitHub Codespaces Port 8501 öffnen. Die Devcontainer-Konfiguration installiert Abhängigkeiten und startet die App. Für Streamlit Community Cloud dieses Repository und `app.py` auswählen; ein Deployment ist nicht Bestandteil dieses Commits.

## Kapitel

1. Gewinnbrücke: Retouren, Rabatte, variable Kosten, Werbung.
2. Annas Reise: interaktive Historie mit drei transparenten Empfehlungsheuristiken.
3. Produktsuche mit Preisfilter; Erklärung von Text-, Bild- und generativen Modellen.
4. Interaktiver Produktgraph mit Alternativen und Ergänzungen.
5. Marketingpolitik mit bekannten synthetischen Treatment-Effekten und inkrementellem DB.
6. Wechsel zwischen Kaufwahrscheinlichkeit, Umsatz und Deckungsbeitrag; CSV-Export.
7. Difference-in-Differences und randomisierte A/B-Simulation mit Unsicherheit.
8. Datenquellen, Status und Retailrocket-CSV-Vorschau/Validierung.

## Ehrlicher Modellstatus

Version 0.1 ist ein interaktives Entscheidungslabor. BERT4Rec, SASRec, LightGCN, Sentence Transformers und CLIP sind erläuterte nächste Ausbaustufen, **keine bereits trainierten Modelle**. Empfehlungen sind Heuristiken, Suche nutzt Wortüberschneidung, Graphkanten sind redaktionell. Marketingeffekte und Produktdaten sind synthetisch. Keine empirischen Modellgüten oder gemessenen Geschäftseffekte werden behauptet.

Datensätze bleiben getrennte Benchmarks: Retailrocket, Amazon-M2, REES46, Amazon Reviews 2023, Amazon ESCI. Links im Dashboard. Nutzungsbedingungen/Zugang vor Import prüfen. Die vorhandenen Shopdaten belegen keine kausalen Rabatteffekte. Dafür ein geeignetes Treatment-/Kontroll-Dataset separat auswählen.

## Finanzielle Definitionen

Nettowerte ohne Umsatzsteuer. In Kapitel 1: Erlös nach Rabatt/Retouren minus Wareneinsatz verkaufter Ware minus Abwicklung/Retourenkosten minus Werbung. Retournierte Ware wird als wiederverkaufbar angenommen. Fixkosten fehlen. DB nach Marketing ist kein Unternehmensgewinn. Kapitel 5: zusätzlicher DB = (p1-p0) × 40 € − p1 × Rabatt − Kontaktkosten. Kapitel 6: erwarteter DB pro Produktexposition unter synthetischer Kaufwahrscheinlichkeit, ohne Werbekosten.

## Nächste technische Meilensteine

- Retailrocket-Pipeline mit chronologischem Split und reproduzierbaren Popularitäts-/Item-KNN-Benchmarks.
- SASRec/BERT4Rec auf Amazon-M2; Recall/NDCG, kurze Sessions, kalte Artikel, Laufzeit.
- Sentence Transformers/CLIP-Retrieval mit echten Produktmetadaten und Bildern.
- LightGCN und hybrider Ranker, echte Messwerte statt Demo-Scores.
- Separater randomisierter Uplift-Benchmark und Policy Evaluation.

Kein Bild wird an externe APIs gesendet. Uploads werden nur im Streamlit-Prozess verarbeitet; Datenschutz/Hosting vor öffentlicher Nutzung konfigurieren.
