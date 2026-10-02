"""Servidor local do Apex: escolhe uma porta livre, serve dist/ e abre o navegador."""

import functools
import http.server
import socket
import sys
import threading
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "dist"
PORTS = range(8080, 8100)

# Tipos fixos: no Windows o registro pode mapear .js para text/plain e o navegador
# recusa carregar módulos JavaScript servidos assim.
MIME_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".js": "text/javascript",
    ".mjs": "text/javascript",
    ".css": "text/css",
    ".json": "application/json",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".webp": "image/webp",
    ".avif": "image/avif",
    ".woff": "font/woff",
    ".woff2": "font/woff2",
    ".glb": "model/gltf-binary",
    ".txt": "text/plain; charset=utf-8",
}


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, **MIME_TYPES}

    def log_message(self, format, *args):
        pass


class Server(http.server.ThreadingHTTPServer):
    # No Windows, SO_REUSEADDR permitiria dividir uma porta já ocupada por outro programa.
    allow_reuse_address = False


def port_answers(port):
    try:
        with socket.create_connection(("localhost", port), timeout=0.3):
            return True
    except OSError:
        return False


def main():
    if not (ROOT / "index.html").is_file():
        print(f"Pasta dist não encontrada em {ROOT}. Extraia o zip inteiro antes de iniciar.")
        return 1

    handler = functools.partial(Handler, directory=str(ROOT))
    server = None
    for port in PORTS:
        if port_answers(port):
            continue
        try:
            server = Server(("127.0.0.1", port), handler)
            break
        except OSError:
            continue
    if server is None:
        print(f"Nenhuma porta livre entre {PORTS.start} e {PORTS.stop - 1}. Feche outros servidores e tente de novo.")
        return 1

    url = f"http://localhost:{server.server_address[1]}"
    print(f"Apex disponível em {url}", flush=True)
    print("Deixe esta janela aberta enquanto usa o Apex. Para encerrar, feche-a ou pressione Ctrl+C.", flush=True)
    if "--sem-navegador" not in sys.argv:
        threading.Timer(0.6, webbrowser.open, [url]).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
