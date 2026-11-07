# hello.py: API IoT pentru citiri de la senzori

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field

app = FastAPI(title="TPI IoT API")

DEV_PATTERN = r"^[a-z0-9-]{1,32}$"


class Reading(BaseModel):
    dev: str = Field(pattern=DEV_PATTERN) #id ul dispozitivului, doar litere mici, cifre și cratime, max 32 caractere
    seq: int = Field(ge=0) #un nr >=0, secventa citirii pentru acel dispozitiv
    ts: int = Field(gt=1_600_000_000) # secunde Unix, UTC, respinge citiri cu timestamp mai mic de 1.600.000.000, de exemplu de la un ceas nesetat
    temp: float = Field(ge=-40, le=85) # °C, temperatura de tip float, între -40 și 85 °C
    hum: float | None = Field(default=None, ge=0, le=100) # umiditate, opțională, poate fi null sau între 0 și 100%


# "Baza de date" in memorie: dev_id -> {seq: Reading}
DB: dict[str, dict[int, Reading]] = {}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/readings", status_code=201, response_model=Reading)
def create_reading(reading: Reading) -> Reading:
    device_readings = DB.setdefault(reading.dev, {})
    if reading.seq in device_readings:
        raise HTTPException(
            status_code=409,
            detail=f"Citirea cu seq={reading.seq} exista deja pentru {reading.dev}.",
        )
    device_readings[reading.seq] = reading
    return reading


@app.get("/devices/{dev_id}/readings")
def readings(
    dev_id: str = Path(pattern=DEV_PATTERN),
    since: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
) -> list[Reading]:
    device_readings = DB.get(dev_id)
    if not device_readings:
        raise HTTPException(
            status_code=404, detail=f"Dispozitivul {dev_id} nu are citiri salvate."
        )

    # Filtram dupa seq (nu dupa ts), apoi ordonam si limitam.
    selected = [
        reading
        for reading in device_readings.values()
        if reading.seq > since
    ]
    return sorted(selected, key=lambda reading: reading.seq)[:limit]
