# TrackerSystem — Home Assistant integratie

[![Validate](https://github.com/Ne0k/trackersystem-homeassistant/actions/workflows/validate.yml/badge.svg)](https://github.com/Ne0k/trackersystem-homeassistant/actions/workflows/validate.yml)

Haalt je voertuigen/objecten uit het **TrackerSystem-portaal** en zet ze als
apparaten in Home Assistant. Per gekozen object krijg je:

- **Device tracker** — positie op de HA-kaart (lat/lng, snelheid, koers, hoogte)
- **Sensoren** — Accu (%), Tankniveau (%), Brandstof (L), Voedingsspanning (V),
  Snelheid (km/u), Kilometerstand (km)
- **Binary sensors** — Contact (aan/uit), Online

Alles read-only; de integratie schrijft niets terug naar het portaal.

## Installatie

**Via HACS (custom repository)**
1. HACS → Integrations → ⋮ → *Custom repositories*
2. Repository: `https://github.com/Ne0k/trackersystem-homeassistant` — categorie *Integration*
3. Installeer "TrackerSystem" en herstart Home Assistant.

**Handmatig**
1. Kopieer de map `custom_components/trackersystem` naar de `config/custom_components/`
   van je Home Assistant.
2. Herstart Home Assistant.

## Instellen

1. **Instellingen → Apparaten & diensten → Integratie toevoegen → TrackerSystem**.
2. Vul in:
   - **Portaal-URL**: `https://portal.trackersystem.nl`
   - **API-sleutel**: je persoonlijke sleutel — die krijg je van de beheerder van
     het portaal. De sleutel bepaalt welke objecten je ziet.
3. Kies de objecten die je in Home Assistant wilt.
4. Klaar — je krijgt per object een apparaat met de bovenstaande entiteiten.

Het ververs-interval (standaard 300 s) pas je aan via de opties van de integratie.
Een tracker stuurt vooral data tijdens beweging; een interval van enkele minuten is
ruim voldoende.

## API

De integratie praat met de read-only endpoints op het portaal:

- `GET /api/ext/devices?full=1` — alle objecten met data (gebruikt voor polling)
- `GET /api/ext/device?imei=<imei>` — één object

Auth via header `X-Api-Key` met een **persoonlijke API-sleutel per gebruiker**
(beheerd in het portaal door de beheerder; intrekken = toegang weg). De respons is
gescope't op de objecten van die gebruiker.
