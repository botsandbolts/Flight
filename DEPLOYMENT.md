# GitHub Codespaces und Streamlit

Aktuelles Ziel: GitHub Codespaces als Python-Laufzeit und Streamlit auf Port 8501.

1. Codespace für botsandbolts/Flight öffnen.
2. Devcontainer installiert Basis- und ML-Abhängigkeiten über setup.sh und startet die App automatisch.
3. Unter Ports den Port 8501 öffnen. Die Oberfläche enthält die Story und fünf Arbeitsbereiche.
4. Neuronale Abhängigkeiten bei Bedarf installieren: zuerst PyTorch vom CPU-Index, dann requirements-ml.txt. Befehle in README.md.

Manueller Start: `bash start.sh`. Protokoll beim automatischen Start: `/tmp/flight-streamlit.log`.

Ein gestoppter Codespace betreibt keine App. Ein öffentlich freigegebener Port macht Uploads und Ressourcen anderen zugänglich. Standardmäßig keine Geheimnisse oder privaten Kundendaten in der Demo verwenden.

Optional später Community Cloud: Repository botsandbolts/Flight, Branch main, app.py, Python 3.11. Basisanforderungen reichen für Story und klassische Modelle. Große Trainingsläufe separat ausführen. Diese Version behauptet keine bereits veröffentlichte Cloud-URL.
