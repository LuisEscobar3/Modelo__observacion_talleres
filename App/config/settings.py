# App/config/settings.py
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    n8n_url: str
    n8n_shared_secret: str | None
    dry_run: bool
    request_timeout: int
    log_file: str | None

    @staticmethod
    def from_env() -> "Settings":
        # Configuración fija para pruebas
        url = "https://segurobolivar-trial.app.n8n.cloud/webhook-test/744e83b2-38fa-4a4a-ab99-aeb9dc1ed84a"
        secret = None
        dry = False
        timeout = 25
        log_file = "App/Output/app.log"  # se guardarán logs JSON en este archivo
        return Settings(url, secret, dry, timeout, log_file)
