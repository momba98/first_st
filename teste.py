import subprocess

subprocess.run(["git", "add", "*"])
subprocess.run(["git", "commit", "-m", "vintenove"])
subprocess.run(["git", "push", "origin", "master"])
