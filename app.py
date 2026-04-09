import urllib.request
from pathlib import Path
import psutil
import yaml
from flask import Flask, render_template, jsonify

app = Flask(__name__, static_folder="static", template_folder="templates")
BASE_DIR = Path(__file__).resolve().parent

# Caché simple para no saturar la API de IP pública
cache = {"public_ip": None}

class NetworkManager:
    @staticmethod
    def get_public_ip():
        if cache["public_ip"]:
            return cache["public_ip"]
        try:
            # Timeout corto para no ralentizar el inicio
            resp = urllib.request.urlopen("https://ipify.org", timeout=2)
            cache["public_ip"] = resp.read().decode().strip()
            return cache["public_ip"]
        except:
            return "1.1.1.1" # Fallback

    @classmethod
    def get_interfaces(cls):
        interfaces = {}
        for iface, addrs in psutil.net_if_addrs().items():
            if iface == "lo": continue
            for addr in addrs:
                if addr.family.name == "AF_INET":
                    interfaces[iface] = addr.address
        
        interfaces["public"] = cls.get_public_ip()
        return interfaces

    @classmethod
    def get_best_ip(cls, ips):
        # Prioridad: VPN -> Ethernet -> WiFi -> Otros
        for prefix in ["tun", "tap", "eth", "wlan", "enp"]:
            for name, ip in ips.items():
                if name.startswith(prefix): return ip
        return next(iter(ips.values()), "127.0.0.1")

def load_data():
    with open(BASE_DIR / "payloads.yml", "r") as f:
        return yaml.safe_load(f)

@app.route("/")
def home():
    data = load_data()
    ips = NetworkManager.get_interfaces()
    return render_template(
        "index.html",
        ips=ips,
        default_ip=NetworkManager.get_best_ip(ips),
        payloads=data["payloads"],
        listeners=data["listeners"]
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
