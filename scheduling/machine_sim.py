import subprocess
import time
import signal
import os
import sys


if len(sys.argv) != 2:
    print("Usage: python machine_sim.py [N]")
    sys.exit(1)

# Nombre de machines à lancer
N = int(sys.argv[1])

processes = []

def launch_machine(name):
    cmd = ["python3", "./Exercice3/machine.py", name]
    p = subprocess.Popen(cmd)
    print(f"Machine lancée : {name} (pid={p.pid})")
    return p

def stop_all():
    print("Arrêt des machines")
    for name, p in processes:
        try:
            os.kill(p.pid, signal.SIGTERM)
            print(f"Machine arrêtée : {name}")
        except ProcessLookupError:
            pass

def main():
    print(f"Lancement de {N} machines")

    # Lancer les machines
    for i in range(1, N+1):
        name = f"machine{i}"
        p = launch_machine(name)
        processes.append((name, p))
        time.sleep(0.2)  # pour éviter de lancer trop vite et saturer

    print("\nMachines en fonctionnement. Ctrl+C pour arrêter.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_all()

if __name__ == "__main__":
    main()
