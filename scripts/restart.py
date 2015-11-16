import subprocess

subprocess.call(["sudo", "systemctl", "stop", "gunicorn"])
subprocess.call(["sudo", "systemctl", "start", "gunicorn"])

subprocess.call(["sudo", "systemctl", "stop", "crossbar"])
subprocess.call(["sudo", "systemctl", "start", "crossbar"])

subprocess.call(["sudo", "nginx", "-s", "reload"])
