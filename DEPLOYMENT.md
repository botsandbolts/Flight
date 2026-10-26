# Veröffentlichung auf Streamlit Community Cloud

Die App wird unmittelbar aus GitHub bereitgestellt. Ein Codespace ist nicht erforderlich.

## Zielkonfiguration

- Repository: `botsandbolts/Flight`
- Branch: `main`
- Main file path: `app.py`
- Python: `3.11`
- Abhängigkeiten: `requirements.txt`
- API-Schlüssel: keine für Version 0.1

## Veröffentlichung

In Streamlit Community Cloud anmelden, eine App aus dem vorhandenen GitHub-Repository erstellen und die Zielkonfiguration auswählen. Nach erfolgreichem Build die tatsächlich zugewiesene App-URL verwenden. Es wird keine noch nicht bestätigte URL behauptet.

Updates auf dem gewählten Branch werden von Community Cloud übernommen. Die GitHub-Prüfung testet alle acht Kapitel und zentrale Interaktionen. Der erste vollständige Modelldatenbestand und trainierte Transformer sind noch nicht enthalten; der Status steht im Dashboard.

Für größere Modelle Training und Artefakterzeugung getrennt vom interaktiven Webprozess durchführen. Nur kompakte geprüfte Inferenzartefakte laden. Keine privaten Kundendaten oder Geheimnisse ins öffentliche Repository schreiben.
