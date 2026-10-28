"""Runnable examples for the core Python curriculum.

Run from this folder:
    python examples_with_output.py

The program prints a short demonstration for each major concept.
"""

from pathlib import Path
import json
import os


def main():
    print("1. VARIABLES AND TYPES")
    service = "jenkins"
    retries = 3
    print(service, retries, type(retries).__name__)

    print("\n2. OPERATORS")
    latency_ms = 850
    print(latency_ms > 500, latency_ms > 500 and True)

    print("\n3. STRINGS")
    message = "  ERROR: Connection TIMEOUT  "
    normalized = message.strip().lower()
    print(normalized)
    print("timeout" in normalized)

    print("\n4. LISTS")
    services = ["jenkins", "docker"]
    services.append("kubernetes")
    print(services)
    print(services[0])

    print("\n5. TUPLES AND SETS")
    coordinates = (17.4, 78.4)
    unique_errors = {"timeout", "disk_full", "timeout"}
    print(coordinates[0])
    print(len(unique_errors))

    print("\n6. DICTIONARIES")
    incident = {"service": "jenkins", "status": "failed"}
    print(incident["service"])
    print(incident.get("owner", "unassigned"))

    print("\n7. CONDITIONS")
    log_line = "Jenkins connection timeout".lower()
    if "timeout" in log_line:
        print("Check network latency")
    elif "permission denied" in log_line:
        print("Check permissions")
    else:
        print("Collect more evidence")

    print("\n8. LOOPS")
    for error in ["timeout", "disk full"]:
        print("Investigating:", error)

    print("\n9. FUNCTIONS")
    def classify(text):
        return "TIMEOUT" if "timeout" in text.lower() else "UNKNOWN"
    print(classify("API TIMEOUT"))
    print(classify("unexpected response"))

    print("\n10. LIST COMPREHENSION")
    print([name.lower() for name in ["Jenkins", "Docker"]])

    print("\n11. PATHS")
    print(Path("logs") / "jenkins.log")

    print("\n12. EXCEPTIONS")
    try:
        int("not-a-number")
    except ValueError:
        print("Input must be an integer")

    print("\n13. CLASSES")
    class Incident:
        def __init__(self, service_name, error_type):
            self.service_name = service_name
            self.error_type = error_type

        def summary(self):
            return f"{self.service_name}: {self.error_type}"
    print(Incident("jenkins", "TIMEOUT").summary())

    print("\n14. JSON")
    payload = json.dumps({"service": "jenkins", "severity": "high"}, sort_keys=True)
    print(payload)
    print(json.loads(payload)["severity"])

    print("\n15. ENVIRONMENT VARIABLES")
    print(os.getenv("APP_ENV", "development"))


if __name__ == "__main__":
    main()
