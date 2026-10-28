"""Example 2: summarize a small list of CI job results using core Python."""


def summarize_jobs(jobs: list[dict]) -> dict:
    total = len(jobs)
    failed = sum(1 for job in jobs if job["status"] == "failed")
    passed = total - failed
    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "failure_rate_percent": round((failed / total) * 100, 1) if total else 0.0,
    }


if __name__ == "__main__":
    sample_jobs = [
        {"name": "build", "status": "passed"},
        {"name": "unit-tests", "status": "failed"},
        {"name": "deploy-staging", "status": "passed"},
        {"name": "security-scan", "status": "failed"},
    ]
    print(summarize_jobs(sample_jobs))
