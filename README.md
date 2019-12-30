# Code-Anhang zu Beweisbar unbeweisbar - Formale Systeme und Gödels Unvollständigkeitssätze
Maturitätsarbeit von Ali Gottschall

## Installation
Installiere Python 3
`pip install -r requirements.txt`

### Typographische formale Systeme
Teste die Funktionalität:
 `python -i FormalSystem.py ali.toml`
 `tests()`
 Definiere ein eigenes System. Für das Konfigurationsformat lass dich von miu.toml und ali.toml inspirieren, sonst konsultiere die schriftliche Arbeit.

### Goodstein
`python -i goodstein.py`
Die Funktionen _hereditary_\_base(int,base)__ und __goodstein(n)__ sind definiert.

### Gödel-Codierung
`python -i numbering.py`
Die Funktionen _goedelisier(formel)_ und _inverse(gödelzahl)_ stehen zur Verfügung.
