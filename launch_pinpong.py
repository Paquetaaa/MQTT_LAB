import subprocess
import time
import signal
import os

processes = []

def main():
    ## Lancement des processus ping pong
    cmd = ["python3", "TP1_exo2.py", "ping", "pong"]
    p = subprocess.Popen(cmd)
    processes.append(p)

    time.sleep(2)

    cmd = ["python3", "TP1_exo2.py", "pong", "ping"]
    p2 = subprocess.Popen(cmd)
    processes.append(p2)

    try:
        time.sleep(15)
    except KeyboardInterrupt:
        print("Interruption manuelle.")

    # Arrêt propre des agents
    print("Arrêt des agents...")
    for p in processes:
        try:
            p.terminate()      # demande d'arrêt propre
            p.wait(timeout=2)  
        except Exception:
            p.kill()           # arrêt forcé si besoin

    print("Tous les agents sont arrêtés.")

if __name__ == "__main__":
    main()
