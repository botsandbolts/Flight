# KI im Unternehmen: fachlicher und technischer Entwurf

## Geschäftlicher Zusammenhang

Kundenverhalten, Produktverständnis und operative Entscheidungen beeinflussen sich. Ein Empfehlungsmodell kann Nachfrage erhöhen, aber keinen verfügbaren Lagerbestand erzeugen. Ein Contentmodell kann Varianten formulieren, aber keine Produkteigenschaft beweisen. Ein Servicecopilot kann Zeit freisetzen, aber diese Zeit wird nicht automatisch zu einer Budgeteinsparung.

Flight verbindet diese Perspektiven in zwölf fiktiven Unternehmensgeschichten. Je Geschichte stehen Problem, Rolle, Datenbedarf, Entscheidung, Zielmetrik und drei Erklärungsebenen nebeneinander. Die Story demonstriert Arbeitsweisen, keine nachgewiesene Transformation eines echten Unternehmens.

## Ausführbare Funktionen

- Der feste lokale Workflow rechnet Nettoumsatz und Deckungsbeitrag unter sichtbaren Annahmen.
- Das Bestandswerkzeug rechnet einen Meldebestand aus Nachfrage während konstanter Lieferzeit plus Sicherheitsbestand. Der Auffüllvorschlag ist kein optimales Bestelllos.
- Ein TF-IDF-Retriever findet Fundstellen im kleinen synthetischen Unternehmenshandbuch.
- Der Trace zeigt aufgerufene Werkzeuge und Ergebnisse. Es gibt keine externen Buchungen, Erstattungen oder Nachrichten.
- OpenAI und Anthropic können optional einen Textentwurf aus dem sichtbaren Szenarioprotokoll formulieren. Die Modelle wählen dabei keine Werkzeuge. Ein Modellaufruf allein ist kein autonomer Agent.
- Das Contentstudio erzeugt regelbasierte Vorlagen. Der Business-Case-Rechner zeigt Zeitwert, Realisierungsanteil, Tokenkosten, laufende Betreuung und einfache Amortisation.

## Möglicher Produktionsausbau

Ein Agentenruntime könnte anhand definierter Schemas Werkzeuge auswählen. Dafür braucht sie auf die konkrete Aufgabe begrenzte Rechte, Zugriff auf eine Kennzahlenschicht und Quellen mit passenden Berechtigungen. Eine Auswertung sollte mit festen Testfällen prüfen, ob die richtigen Tools, Zahlen und Belege verwendet werden. Ein weiterer Sprachmodellprüfer kann helfen, ersetzt aber keine unabhängige Evidenz.

Neue organisatorische Rollen wären fachlicher Prozesseigner, technischer Betreiber und Verantwortlicher für Qualität und Nutzenmessung. Ob diese Funktionen eigene Stellen benötigen, hängt von Umfang und Organisation ab. Unnötige Arbeit sollte vor ihrer Automatisierung hinterfragt werden.

## Modellanbieter

ChatGPT/OpenAI und Claude/Anthropic werden als mögliche Werkzeuge beschrieben, ohne pauschale Überlegenheitsbehauptungen. Flight nutzt bei aktivierter Option separate APIs. Aktuelle Modell-IDs kommen aus dem jeweiligen API-Konto. Gemini und lokale offene Modelle sind erläuterte Architekturoptionen ohne implementierte Anbindung.

Die API-Adapter sind ohne Zugangsschlüssel nicht live geprüft. Lokale Tests rufen keine kostenpflichtigen Dienste auf. API-Schlüssel ausschließlich serverseitig hinterlegen.

Quellen:
- https://developers.openai.com/api/docs/guides/tools
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works

## Humor mit fachlichem Zweck

„Der Bot bekommt eine Kostenstelle“ führt zur Vollkostenrechnung. „Ein Markenname ist kein Konfidenzintervall“ führt zu eigenen Evaluationsfällen. „Wasserfest entsteht nicht durch einen flüssigen Prompt“ führt zur belegten Produktkommunikation. Die Pointe soll ein Konzept verankern und keine Unsicherheit verdecken.
