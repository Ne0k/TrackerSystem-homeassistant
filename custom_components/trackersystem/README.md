# TrackerSystem — Home Assistant integratie

Haalt je voertuigen/objecten uit het **TrackerSystem-portaal** en zet ze als
apparaten in Home Assistant. Per gekozen object krijg je:

- **Device tracker** — positie op de HA-kaart (lat/lng, snelheid, koers, hoogte)
- **Sensoren** — Accu (%), Tankniveau (%), Brandstof (L), Voedingsspanning (V),
  Snelheid (km/u), Kilometerstand (km)
- **Binary sensors** — Contact (aan/uit), Online

Alles read-only; de integratie schrijft niets terug naar het portaal.

## Installatie

**Handmatig**
1. Kopieer de map `custom_components/trackersystem` naar de `config/custom_components/`
   van je Home Assistant.
2. Herstart Home Assistant.

**Via HACS (custom repository)**
1. HACS → Integrations → ⋮ → *Custom repositories* → voeg de repo toe (categorie
   *Integration*).
2. Installeer "TrackerSystem" en herstart HA.

## Instellen

1. **Instellingen → Apparaten & diensten → Integratie toevoegen → TrackerSystem**.
2. Vul in:
   - **Portaal-URL**: `https://portal.trackersystem.nl`
   - **API-sleutel**: de sleutel uit `config/ha.php` op de server
     (`X-Api-Key`). *De beheerder levert deze apart aan.*
3. Kies de objecten die je in Home Assistant wilt.
4. Klaar — je krijgt per object een apparaat met de bovenstaande entiteiten.

Het ververs-interval (standaard 300 s) pas je aan via de opties van de integratie.
Een tracker stuurt vooral data tijdens beweging; een interval van enkele minuten is
ruim voldoende.

## API

De integratie praat met de read-only endpoints op het portaal:

- `GET /api/ext/devices?full=1` — alle objecten met data (gebruikt voor polling)
- `GET /api/ext/device?imei=<imei>` — één object

Auth via header `X-Api-Key`. Config staat server-side in `config/ha.php` (buiten git);
optioneel kun je daar een IP-allowlist zetten.
