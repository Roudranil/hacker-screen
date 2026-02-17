import subprocess
import sys
import time
from pathlib import Path


def test_binary(binary_path: str, timeout: int = 15) -> None:
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
        # Run the binary
        # We expect it to run indefinitely (matrix rain), so a TimeoutExpired is a success.
        # A quick return (crash) is a failure.
        proc = subprocess.run(
            [str(path)], timeout=timeout, capture_output=True, text=True
        )

        # If it returns naturally, that's unexpected for this app (unless it crashed)
        print("Binary exited early!")
        print("STDOUT:", proc.stdout)
        print("STDERR:", proc.stderr)

        if proc.returncode != 0:
            print(f"Binary failed with return code {proc.returncode}")
            sys.exit(proc.returncode)

    except subprocess.TimeoutExpired:
        print(f"Success: Binary ran for {timeout}s without crashing.")
        sys.exit(0)
    except Exception as e:
        print(f"Error running binary: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_binary.py <path_to_binary>")
        sys.exit(1)

    test_binary(sys.argv[1])
