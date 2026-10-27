# Die Darstellung folgt einem Einkauf

## Ziel

Eine Person ohne ML-Vorkenntnisse soll verstehen, welche Entscheidung ansteht, welche Information hilft und wie das Team den Nutzen prüfen würde.

## Einheitliche Reihenfolge

Die Streamlit-Hauptansicht und die Folien folgen derselben Kette: Finden, Empfehlen, Rechnen, Rabatt entscheiden, Abstimmen und Prüfen. Ein kurzer Einstieg erklärt Anna und ihr Budget. Das Fazit trennt Demonstration, ausführbaren Code und offene Nachweise. Zusätzliche Modelle und Datenquellen stehen im technischen Anhang beziehungsweise in aufklappbaren Vertiefungen.

## Schreibregeln

- Eine Frage und eine konkrete Entscheidung pro Schritt.
- Einen Begriff erst am Beispiel erklären, dann fachlich benennen.
- Einen Wert mit Einheit und Bezugsgröße zeigen.
- Simulationen nicht wie gemessene Geschäftsergebnisse formulieren.
- Quellen, Modellstatus und Grenzen dort nennen, wo sie die Aussage beeinflussen.
- Humor als Gedächtnishilfe verwenden, nicht als Ersatz für Erklärung.
- Keine unerklärten Debug-Objekte oder rohen JSON-Ausgaben im Hauptfluss.

## Quellen der Darstellung

`flightlab/story.py` hält die gemeinsamen Beispielrechnungen und die Reihenfolge der Geschichte. `docs/presentation.json` enthält Titel, Inhalte und Kernaussagen der 15 Folien. Die Berechnungstests sichern die Beispielzahlen ab. Die eigentlichen Modell- und Datenmodule bleiben davon getrennt.
