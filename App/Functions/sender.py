# App/Functions/sender.py
from __future__ import annotations
import json
import time
import hmac
import hashlib
from typing import Any, Optional
import requests
from App.config.settings import Settings
from App.config.logger import get_logger

def _sign_payload(secret: Optional[str], payload: Any) -> str:
    if not secret:
        return ""
    body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()

def send(settings: Settings, payload: Any, retries: int = 3, timeout: int | None = None) -> requests.Response | None:
    """
    Envía el payload (por ejemplo: {"registros": [...]}) al webhook de n8n.
    - Respeta settings.dry_run (no envía, solo loguea).
    - Firma opcional con HMAC si settings.n8n_shared_secret no es None.
    - Reintentos simples para errores de red / 5xx.
    """
    logger = get_logger(log_file=settings.log_file)
    url = settings.n8n_url
    timeout = timeout or settings.request_timeout

    headers = {"Content-Type": "application/json"}
    sig = _sign_payload(settings.n8n_shared_secret, payload)
    if sig:
        headers["X-Signature"] = sig

    if settings.dry_run:
        logger.info("dry_run_send", extra={"extra": {"url": url, "preview": str(payload)[:300]}})
        return None

    last_exc: Exception | None = None
    for attempt in range(1, retries + 1):
        start = time.perf_counter()
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=timeout)
            elapsed_ms = round((time.perf_counter() - start) * 1000)
            # Si no es error 5xx, devolvemos respuesta (200-499)
            logger.info("send_attempt", extra={"extra": {"attempt": attempt, "status": resp.status_code, "ms": elapsed_ms}})
            if resp.status_code < 500:
                if resp.status_code >= 400:
                    logger.error("send_error", extra={"extra": {"status": resp.status_code, "body": resp.text[:500]}})
                return resp
        except requests.RequestException as e:
            last_exc = e
            logger.error("send_exception", extra={"extra": {"attempt": attempt, "error": str(e)}})

        # Backoff exponencial: 2, 4, 8...
        time.sleep(2 ** attempt)

    if last_exc:
        raise last_exc
    raise RuntimeError("No fue posible contactar n8n después de los reintentos")
