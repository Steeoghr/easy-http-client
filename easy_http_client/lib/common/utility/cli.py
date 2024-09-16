import subprocess
import shlex
import sys
import os

def execute_command(command):
    """Esegue un comando shell e stampa l'output in tempo reale, con BuildKit abilitato per Docker."""
    try:
        if isinstance(command, str):
            command = shlex.split(command)
        
        # Assicuriamoci che BuildKit sia abilitato
        my_env = os.environ.copy()
        my_env["DOCKER_BUILDKIT"] = "1"

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=False,
            bufsize=0,  # Disabilita il buffering
            env=my_env
        )

        while True:
            output = process.stdout.read(1)
            if output == b'' and process.poll() is not None:
                break
            if output:
                try:
                    sys.stdout.buffer.write(output)
                    sys.stdout.flush()
                except Exception:
                    pass  # Ignora eventuali errori di scrittura

        return_code = process.poll()
        if return_code != 0:
            print(f"Command failed with return code {return_code}")
            return False
        return True

    except Exception as e:
        print(f"An error occurred during command execution: {e}")
        return False