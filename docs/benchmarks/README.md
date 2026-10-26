# Ausgeführte Benchmarks

- synthetic_smoke.json: alle sechs Modelle, künstliche Sequenzen, je eine Epoche bei neuronalen Modellen. Funktionstest, kein öffentlicher Qualitätsvergleich.
- amazon_reviews_sample.json: alle sechs Modelle auf den ersten 40.000 Rezensionen der Kategorie All_Beauty, globaler Zeitsplit, erste 100 geeignete Historienfälle, 31 warme und 69 kalte Ziele. Alle Modelle erreichten auf den 31 warmen Fällen Recall@10 und NDCG@10 von null. Kein Modellgewinn und keine kommerzielle Verbesserung nachgewiesen. Diese kleine und schwierige Präfixauswahl ist ungeeignet, um die allgemeine Modellqualität zu beurteilen.
- criteo_validation.json: erste 20.000 Zeilen enthalten nur Treatment. Der Uplift-Versuch wurde vor Training abgebrochen. Keine künstliche Kontrollgruppe wurde ergänzt.

Versionsstand, Fingerprints, Laufzeiten und Protokolle stehen in JSON. Für aussagekräftige Vergleiche geeignete vollständige Daten, validierte Stichproben, separates Validierungsset und größere Testmengen verwenden. Diese Ergebnisse bleiben als nachvollziehbarer Entwicklungsstand erhalten.
