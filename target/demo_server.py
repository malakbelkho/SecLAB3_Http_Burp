from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from datetime import datetime

HOST = "0.0.0.0"
PORT = 8000

class LabHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        html = f"""
        <!doctype html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>LAB3 Burp Android</title>
        </head>
        <body>
            <h1>LAB 3 - Cible locale autorisée</h1>
            <p>Cette page sert uniquement à observer le trafic HTTP dans Burp.</p>

            <h2>Test GET</h2>
            <form method="GET" action="/search">
                <input name="q" value="android-burp-lab">
                <input name="device" value="emulator">
                <button type="submit">Envoyer GET</button>
            </form>

            <h2>Test POST</h2>
            <form method="POST" action="/feedback">
                <input name="note" value="trace-demo">
                <input name="student_context" value="lab-mobile-security">
                <button type="submit">Envoyer POST</button>
            </form>

            <p>Date serveur : {datetime.now()}</p>
            <p>Chemin demandé : {parsed.path}</p>
            <p>Paramètres reçus : {params}</p>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Set-Cookie", "lab_session=demo_cookie_123; Path=/; HttpOnly")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")

        response = f"""
        <html>
        <body>
            <h1>POST reçu</h1>
            <p>Corps de la requête :</p>
            <pre>{body}</pre>
            <a href="/">Retour</a>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Set-Cookie", "post_trace=observed_by_burp; Path=/; HttpOnly")
        self.end_headers()
        self.wfile.write(response.encode("utf-8"))

print(f"[+] Mini cible HTTP lancée sur http://127.0.0.1:{PORT}")
print("[+] Garde cette fenêtre ouverte pendant le lab.")
HTTPServer((HOST, PORT), LabHandler).serve_forever()