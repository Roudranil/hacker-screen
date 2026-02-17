import os
import subprocess
import sys
import time
from pathlib import Path


def test_binary(binary_path: str, timeout: int = 120) -> None:
    path = Path(binary_path).resolve()
    print(f"Testing binary at: {path}")

    if not path.exists():
        print(f"Error: Binary not found at {path}")
        sys.exit(1)

    # Windows requires .exe extension check if not provided
    if sys.platform == "win32" and path.suffix != ".exe":
        path = path.with_suffix(".exe")

    start_time = time.time()
    try:
        # Run the binary with test mode enabled (skips infinite matrix rain loop)

        # Force UTF-8 encoding/ANSI for windows CI
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUTF8"] = "1"
        env["TERM"] = "xterm-256color"
        env["ANSICON"] = "1"

        # Tell the app to exit after final sequence instead of looping forever
        env["HACKER_SCREEN_TEST_MODE"] = "1"

        print(f"Running binary with timeout={timeout}s...")
        proc = subprocess.run(
            [str(path)],
            timeout=timeout,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
        )

        print("Binary exited!")

        # In test mode, we expect a clean exit (0)
        if proc.returncode == 0:
            print(
                f"Success: Binary ran through all phases and exited cleanly in {time.time() - start_time:.2f}s."
            )
            sys.exit(0)
        else:
            print(f"Binary failed with return code {proc.returncode}")
            print("STDOUT:", proc.stdout)
            print("STDERR:", proc.stderr)
            sys.exit(proc.returncode)

    except subprocess.TimeoutExpired as e:
        print(
            f"Error: Binary timed out after {timeout}s (it should have exited in test mode)."
        )
        # If we have output (partial), print it
        if e.stdout:
            print(
                "STDOUT (partial):",
                e.stdout.decode("utf-8", errors="replace")
                if isinstance(e.stdout, bytes)
                else e.stdout,
            )
        if e.stderr:
            print(
                "STDERR (partial):",
                e.stderr.decode("utf-8", errors="replace")
                if isinstance(e.stderr, bytes)
                else e.stderr,
            )
        sys.exit(1)

    except Exception as e:
        print(f"Error running binary: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_binary.py <path_to_binary>")
        sys.exit(1)

    test_binary(sys.argv[1])
