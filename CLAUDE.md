# Project: scholenkalender regio Gent

Zie README.md voor de opbouw. Kort:

- `make.py` is de enige bron van waarheid voor events en adressen. Wijzig daar, niet in het .ics of in schools.json.
- Na elke wijziging: `python3 make.py && python3 export.py && python3 build_page.py`.
- Eventtitels hebben de vorm "Schoolnaam – Soort event". Taal: Nederlands (Vlaams).
- Tijdzone: Europe/Brussels. Controleer bij nieuwe data of de weekdag klopt.
- `index.html` drukt af als lijst op A4 liggend (zonder kaart en zonder de uitklapbare details); met heel Oost-Vlaanderen zijn dat vijf bladen.
- De scholenlijst = `schools.json` (uit `make.py`, met infomomenten) + alle andere adressen met studieaanbod uit de officiële lijst van Oost-Vlaanderen (`"nieuw": true` in `aanbod.json`, zonder infomomenten).
- `index.html` is statisch en moet ook zonder internet werken: de vaste kaartbeelden zitten erin als data-URI; de OpenStreetMap-kaart is een extra die alleen start als de tegels laden. Net en studieaanbod alleen wijzigen via `fetch_aanbod.py`, niet met de hand in `aanbod.json`.
