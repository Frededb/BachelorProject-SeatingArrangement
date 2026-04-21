import subprocess
import sys
import time

import runAlgorithm

INPUT_FILE = "Inputs/realData/inputReal.json"
ATTRIBUTE_FILE = "Inputs/defaultAttributeSet.json"
TIMEOUT_SECONDS = 120


def main():
    algos = runAlgorithm.ALGORITHMS
    print(f"Function-level test for {len(algos)} algorithms")
    results = []
    skipped = []

    for key, fn in algos.items():
        if key == "bruteForce":
            skipped.append(key)
            print("SKIP", key)
            continue

        module_name = fn.__module__
        function_name = fn.__name__
        code = (
            "from Utils.reader import readPeople\n"
            "from Utils.UtilFunctions import makeEmptyArrangement\n"
            "from Utils.ValueCalc import calcArrangement\n"
            f"from {module_name} import {function_name}\n"
            f"people = readPeople('{INPUT_FILE}', '{ATTRIBUTE_FILE}')\n"
            "arrangement = makeEmptyArrangement(len(people), 8)\n"
            f"result = {function_name}(people, arrangement)\n"
            "score = calcArrangement(result)[0]\n"
            "print(f'SCORE:{score}')\n"
            "print('OK')\n"
        )

        try:
            start = time.perf_counter()
            completed = subprocess.run(
                [sys.executable, "-c", code],
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
            )
            elapsed = time.perf_counter() - start
            stdout_lines = completed.stdout.strip().splitlines() if completed.stdout.strip() else []
            score = None
            for line in stdout_lines:
                if line.startswith("SCORE:"):
                    score = line.split("SCORE:", 1)[1].strip()
                    break

            ok = completed.returncode == 0 and "OK" in completed.stdout
            if completed.stderr.strip():
                message = completed.stderr.strip()
            else:
                message = ""
            results.append((key, ok, score, elapsed, message))
            if ok:
                print("PASS", key, f"score={score}", f"time={elapsed:.2f}s")
            else:
                print("FAIL", key, message, f"time={elapsed:.2f}s")
        except Exception as exc:
            results.append((key, False, None, None, str(exc)))
            print("FAIL", key, str(exc))

    failures = [result for result in results if not result[1]]
    print(f"\nTotal failures: {len(failures)}")
    print(f"Total skipped: {len(skipped)}")

    print("\nScores:")
    for key, ok, score, elapsed, _ in results:
        if ok:
            print(f"{key}: {score} (time={elapsed:.2f}s)")

    for key in skipped:
        print(f"{key} -> skipped by request")
    for key, _, _, elapsed, message in failures:
        suffix = f" (time={elapsed:.2f}s)" if elapsed is not None else ""
        print(f"{key} -> {message}{suffix}")


if __name__ == "__main__":
    main()

