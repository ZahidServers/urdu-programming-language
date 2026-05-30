import subprocess, signal, os, sys, time

proc = subprocess.Popen(
    [r"d:\Urdu_Programming_Language\build_env\Scripts\python.exe", "-m", "urdu", "run", "app.urdu"],
    cwd=r"d:\Urdu_Programming_Language\examples\DJANGO_CALC_APP",
    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
)

time.sleep(4)
print(f"Server started, PID={proc.pid}. Sending CTRL_C_EVENT...", flush=True)
os.kill(proc.pid, signal.CTRL_C_EVENT)

deadline = time.time() + 4
while time.time() < deadline:
    if proc.poll() is not None:
        print(f"PROCESS EXITED with code {proc.returncode} — Ctrl+C fix WORKS!", flush=True)
        sys.exit(0)
    time.sleep(0.2)

print("PROCESS STILL ALIVE after 4s — fix did NOT work", flush=True)
proc.kill()
