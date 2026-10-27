# 01 — Python Fundamentals

This module assumes no prior AI knowledge. Type the examples into Python files, run them, compare the output, and modify them.

## 1. Run Python

From the repository root:
```powershell
python --version
python .\01-python-fundamentals\agent.py
```
On Linux use `python3 --version`; when your virtual environment is activated, `python` should refer to that environment.

## 2. Variables and data types

```python
service = "jenkins"
retry_count = 3
pipeline_ok = False
latency_seconds = 2.4
print(service, retry_count, pipeline_ok, latency_seconds)
print(type(retry_count).__name__)
```
Expected output:
```text
jenkins 3 False 2.4
int
```

## 3. Strings and normalization

```python
message = "ERROR: Connection TIMEOUT"
print(message.lower())
print("timeout" in message.lower())
print(message.startswith("ERROR"))
```
Expected output:
```text
error: connection timeout
True
True
```
Normalize case before matching log patterns so uppercase and lowercase variations work.

## 4. Lists and dictionaries

```python
services = ["jenkins", "docker", "kubernetes"]
incident = {"service": "jenkins", "status": "failed", "attempt": 2}
print(services[0])
print(incident["status"])
print(incident.get("owner", "unassigned"))
```
Expected output:
```text
jenkins
failed
unassigned
```

## 5. Conditions: if / elif / else

```python
log = "Connection timeout".lower()
if "timeout" in log:
    print("Check network latency and server health.")
elif "null pointer" in log:
    print("Check variable initialization.")
else:
    print("Collect more evidence.")
```
Expected output: `Check network latency and server health.`

Only the first matching branch executes. Try changing `log` to `Null pointer exception` and then to `Disk quota exceeded`.

## 6. Loops

```python
errors = ["timeout", "disk full", "timeout"]
for error in errors:
    print("Investigating:", error)
```
Expected output:
```text
Investigating: timeout
Investigating: disk full
Investigating: timeout
```

## 7. Functions, parameters, and return values

```python
def classify(logs):
    text = logs.lower()
    if "timeout" in text:
        return "TIMEOUT"
    if "null pointer" in text:
        return "NULL_POINTER"
    return "UNKNOWN"

print(classify("Jenkins TIMEOUT"))
print(classify("Null pointer exception"))
print(classify("Disk full"))
```
Expected output:
```text
TIMEOUT
NULL_POINTER
UNKNOWN
```
A parameter receives input; `return` sends a value back to the caller. `print` displays information but does not replace a return value.

## 8. Exceptions and safe file reading

```python
from pathlib import Path

path = Path("sample.log")
try:
    text = path.read_text(encoding="utf-8")
except FileNotFoundError:
    print("Log file not found; check the path.")
else:
    print("Read", len(text), "characters")
```
If `sample.log` is absent, expected output is `Log file not found; check the path.`. Never assume files or log content exist.

## 9. Unit testing

Run from repository root:
```powershell
python -m unittest discover -s .\07-devops-ai-project\tests -v
```
Expected output includes tests marked `ok` and `OK` at the end, provided all tests pass.

## Exercises

1. Add a `"permission denied"` category.
2. Make matching case-insensitive.
3. Create a function that returns a recommendation instead of printing it.
4. Add tests for empty strings and unknown errors.
5. Explain the difference between a syntax error and an exception.

## Interview questions

- What are lists versus dictionaries?
- What is the difference between `print` and `return`?
- How do `if`, `elif`, and `else` work?
- Why use exceptions when reading logs?
- What is a unit test, and what does an assertion verify?
