# main.py
from __future__ import annotations
import argparse
import pathlib
import sys

from App.config.settings import Settings
from App.config.logger import get_logger
from App.Functions.reader import leer_solo_tabla_csv_filtrado, file_fingerprint
from App.Functions.payloads import build_json_para_n8n
from App.Functions.sender import send

DEFAULT_CSV_PATH = r"C:\Users\1032497498\PycharmProjects\Modelo__observacion_talleres\input\Reporte_Hallazgos.csv"

def cli():
    ap = argparse.ArgumentParser(description="Transforma CSV y envía a n8n")
    ap.add_argument(
        "csv_path",
        nargs="?",
        default=DEFAULT_CSV_PATH,
        help=f"Ruta al CSV de observaciones (por defecto {DEFAULT_CSV_PATH})"
    )
    ap.add_argument("--throttle", type=float, default=0.0, help="Pausa en segundos entre envíos")
    ap.add_argument("--no-send", action="store_true", help="No enviar a n8n, solo procesar")
    ap.add_argument("--log-file", default=None, help="Ruta de log JSON (sobrescribe settings)")
    args = ap.parse_args()

    settings = Settings.from_env()
    if args.log_file:
        object.__setattr__(settings, "log_file", args.log_file)
    logger = get_logger(log_file=settings.log_file)

    csv_path = pathlib.Path(args.csv_path)
    df = leer_solo_tabla_csv_filtrado(str(csv_path))
    payload = build_json_para_n8n(df)

    if not args.no_send:
        send(settings, payload)
        if args.throttle > 0:
            import time as _t
            _t.sleep(args.throttle)
        logger.info("sent_count", extra={"extra": {"count": len(payload['registros'])}})
        print(f"Listo. Se envió un payload con {len(payload['registros'])} registro(s) a n8n.")

if __name__ == "__main__":
    cli()
