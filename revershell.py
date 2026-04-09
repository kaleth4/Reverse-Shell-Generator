import urllib.request
from pathlib import Path

import psutil
import yaml
from flask import Flask, render_template

app = Flask(__name__, static_folder="templates", static_url_path="/static")


class NetworkInterfaces:
    @staticmethod
    def _get_public_ip():
        try:
            resp = urllib.request.urlopen("https://api4.ipify.org", timeout=3)
            return resp.read().decode().strip()
        except Exception:
            return None

    @classmethod
    def get_all(cls):
        ips = {}

        for iface, addrs in psutil.net_if_addrs().items():
            if iface == "lo":
                continue
            for addr in addrs:
                if addr.family.name == "AF_INET":
                    ips[iface] = addr.address
                    break

        public = cls._get_public_ip()
        if public:
            ips["public"] = public

        return ips or {"lo": "127.0.0.1"}

    @classmethod
def get_default(cls):
    ips = cls.get_all()
    # Prioridad: VPN -> Ethernet -> WiFi
    for preferred in ["tun0", "eth0", "wlan0"]:
        if preferred in ips:
            return ips[preferred]
    # Si no, cualquier cosa que no sea la pública
    return next((ip for name, ip in ips.items() if name != "public"), "127.0.0.1")



BASE_DIR = Path(__file__).resolve().parent


def load_payloads():
    return yaml.safe_load((BASE_DIR / "payloads.yml").read_text())


@app.route("/")
def home():
    data = load_payloads()
    return render_template(
        "index.html",
        ips=NetworkInterfaces.get_all(),
        default_ip=NetworkInterfaces.get_default(),
        payloads=data["payloads"],
        listeners=data["listeners"],
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)