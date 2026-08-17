<p align="center">
  <img src="https://raw.githubusercontent.com/Ne0k/trackersystem-homeassistant/main/images/logo.png" alt="TrackerSystem" width="220">
</p>

# TrackerSystem — Home Assistant integration

[![Validate](https://github.com/Ne0k/trackersystem-homeassistant/actions/workflows/validate.yml/badge.svg)](https://github.com/Ne0k/trackersystem-homeassistant/actions/workflows/validate.yml)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

Brings your vehicles/objects from the **TrackerSystem portal** into Home Assistant
as devices. For every selected object you get:

- **Device tracker** — live position on the HA map (lat/lng, speed, course, altitude)
- **Sensors** — Battery (%), Fuel level (%), Fuel (L), Supply voltage (V),
  Speed (km/h), Odometer (km)
- **Binary sensors** — Ignition (on/off), Online
- Battery and fuel sensors are created only when the tracker actually reports them.

Everything is read-only; the integration never writes anything back to the portal.

## Installation

**Via HACS (custom repository)**
1. HACS → Integrations → ⋮ → *Custom repositories*
2. Repository: `https://github.com/Ne0k/trackersystem-homeassistant` — category *Integration*
3. Install "TrackerSystem" and restart Home Assistant.

**Manual**
1. Copy the `custom_components/trackersystem` folder into the
   `config/custom_components/` directory of your Home Assistant installation.
2. Restart Home Assistant.

## Configuration

1. **Settings → Devices & services → Add integration → TrackerSystem**.
2. Enter:
   - **Portal URL**: `https://portal.trackersystem.nl`
   - **API key**: your personal key — provided by the portal administrator.
     The key determines which objects you can see.
3. Select the objects you want in Home Assistant.
4. Done — each object appears as a device with the entities listed above.

The update interval (default 300 s) can be changed via the integration options.
A tracker mainly sends data while moving; an interval of a few minutes is plenty.

## API

The integration talks to read-only endpoints on the portal:

- `GET /api/ext/devices?full=1` — all objects with data (used for polling)
- `GET /api/ext/device?imei=<imei>` — a single object

Authentication uses the `X-Api-Key` header with a **personal per-user API key**
(managed by the portal administrator; revoking the key removes access). The
response is scoped to the objects linked to that user.
