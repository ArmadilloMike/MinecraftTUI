import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import threading
import webbrowser
import minecraft_launcher_lib
import requests
from urllib3 import BaseHTTPResponse


def show_progress():

    current_max = 0
    def set_status(status: str):
        print(status)

    def set_progress(progress: int):
        if current_max != 0:
            print(f"{progress}/{current_max}")

    def set_max(new_max: int):
        global current_max
        current_max = new_max

    callback = {
        "setStatus": set_status,
        "setProgress": set_progress,
        "setMax": set_max
    }
    return callback

def get_installed_versions():
    installations = os.listdir("installations")
    versions = []
    for installation in installations:
        installation = installation.replace("minecraft-","").replace("-",".")
        versions.append(installation)
    return versions

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code_received

        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        if "code" in query_params:
            auth_code_received = query_params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text-html')
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Success</h1><p>You can close this window and return to the terminal.</p></body></html>")
            print("\n Auth code received.")
        else:
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Error</h1><p>No authorization code received.</p></body></html>")

    def log_message(self, format, *args):
        pass

def start_callback_server():
    server = HTTPServer(("localhost", 7492), CallbackHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


class MinecraftAuthorization:
    def __init__(self, client_id: str, redirect_url: str):
        self.client_id = client_id
        self.redirect_url = redirect_url
        self.auth_code = None
        self.server = None
        self.login_data = None

    def start_callback_server(self):
        self.server = start_callback_server()
        print("Callback server started")

    def get_login_url(self):
        login_url, state, code_verifier = minecraft_launcher_lib.microsoft_account.get_secure_login_data(
            self.client_id, self.redirect_url
        )
        self.state = state
        self.code_verifier = code_verifier
        return login_url

    def open_browser(self, login_url: str):
        print(f"\nOpening browser to {login_url}")
        webbrowser.open(login_url)

    def wait_for_auth_code(self, timeout: int = 300) -> bool:
        elapsed = 0
        print("Waiting for authorization...")

        while self.auth_code is None and elapsed < timeout:
            time.sleep(1)
            elapsed += 1
            if elapsed % 10 == 0:
                print(f"Still waiting... ({elapsed}s)")

        if self.auth_code is None:
            print("Timeout! No auth code received")
            return False

        print(f"Auth code received!")
        return True

    def complete_login(self) -> bool:
        try:
            self.login_data = minecraft_launcher_lib.microsoft_account.complete_login(
                self.client_id, None, self.redirect_url, self.auth_code, self.code_verifier
            )
            print("\n✓ Login successful!")
            print(f"Username: {self.login_data['name']}")
            print(f"UUID: {self.login_data['id']}")
            print(f"Token: {self.login_data['access_token'][:20]}...")
            return True

        except KeyError as e:
            print(f"\nKeyError during login: {e}")
            self._manual_token_exchange()
            return False

    def _manual_token_exchange(self):
        token_data = {
            "client_id": self.client_id,
            "code": self.auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_url,
            "code_verifier": self.code_verifier
        }
        response = requests.post(
            "https://login.microsoftonline.com/consumers/oauth2/v2.0/token",
            data=token_data
        )
        print("Token response:", response.json())

    def get_credentials(self) -> dict:
        if not self.login_data:
            return None

        return {
            "username": self.login_data["name"],
            "uuid": self.login_data["id"],
            "token": self.login_data["access_token"]
        }

    def cleanup(self):
        if self.server:
            self.server.shutdown()
            print("Callback server shutdown")

    def authorize(self, timeout: int = 300) -> bool:
        try:
            self.start_callback_server()
            login_url = self.get_login_url()
            self.open_browser(login_url)

            if not self.wait_for_auth_code(timeout):
                return False

            return self.complete_login()

        finally:
            self.cleanup()