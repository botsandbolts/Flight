# Gesprächsleitfaden für zehn Minuten

1. **Geschäftsproblem (1 Minute):** Umsatz steigt, Beitrag sinkt. Mit Rabatt/Retouren erklären, warum reine Conversion-Optimierung falsche Anreize setzt.
2. **Kundenreise (2 Minuten):** Anna klickt anders, Empfehlungen ändern sich. Heuristiken sind erklärbar, Transformer müssen ihre Zusatzkosten im Trainingslabor rechtfertigen.
3. **Daten und Messung (2 Minuten):** Öffentliche Quellen erfüllen verschiedene Rollen. Chronologischer Split für Events, getrenntes Sessionprotokoll für M2, keine Fantasie-Verknüpfung über Shops.
4. **Technik (2 Minuten):** BERT4Rec/SASRec, LightGCN, hybride Produktverständnis mit Sentence Transformers und CLIP. Genau sagen, welcher Code ausgeführt und welches Modell geladen wurde.
5. **Marketing und Ökonometrie (2 Minuten):** Propensity ist keine zusätzliche Wirkung. Treatment statt exposure verwenden. DiD braucht Annahmen und Unsicherheit.
6. **Entscheidung (1 Minute):** Relevanz, erwarteten Umsatz und Deckungsbeitrag vergleichen. Nächster Produktionsschritt ist ein kontrolliertes Experiment, keine Behauptung garantierter Umsatzsteigerung.

## Mögliche Fragen

- Warum braucht es BERT4Rec, wenn Markov gewinnt? Dann gewinnt Markov. Modellkomplexität ist kein Selbstzweck.
- Wie verhindert ihr Leakage? Training vor dem Cutoff, Trainingsvokabular, getrennte Testfälle, keine Ergebniswahl nach Testscore.
- Warum stehen keine echten Einkaufsmargen im öffentlichen Datensatz? Weil sie fehlen. Szenarioannahmen sind sichtbar und von Messwerten getrennt.
- Was beweist das Portfolio? Implementierungs- und Bewertungsfähigkeit. Es ersetzt keinen Produktionsnachweis.
