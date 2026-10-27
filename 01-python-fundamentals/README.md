# 01 — Python Fundamentals

Type examples yourself, run them, compare output, then change one thing at a time.

## 1. Variables and types

```python
service = "jenkins"
retry_count = 3
pipeline_ok = False
print(service, retry_count, pipeline_ok)
print(type(retry_count).__name__)
```
Output:
```text
jenkins 3 False
int
```

## 2. Strings

```python
message = "ERROR: Connection TIMEOUT"
print(message.lower())
print("timeout" in message.lower())
```
Output:
```text
error: connection timeout
True
```
Use normalization for case-insensitive matching.

## 3. Lists and dictionaries

```python
services = ["jenkins", "docker", "kubernetes"]
incident = {"service": "jenkins", "status": "failed"}
print(services[0])
print(incident["status"])
print(incident.get("owner", "unassigned"))
```
Output: `jenkins`, `failed`, `unassigned` on separate lines.

## 4. if / elif / else

```python
log = "Connection timeout".lower()
if "timeout" in log:
    print("Check network latency and server health.")
elif "null pointer" in log:
    print("Check variable initialization.")
else:
    print("Collect more evidence.")
```
Output: `Check network latency and server health.`

Change the log to `Null pointer exception`, then `Disk quota exceeded`, and observe which branch runs.

## 5. Loops

```python
for error in ["timeout", "disk full", "timeout"]:
    print("Investigating:", error)
```
Output:
```text
Investigating: timeout
Investigating: disk full
Investigating: timeout
```

## 6. Functions and return values

```python
def classify(logs):
    text = logs.lower()
    if "timeout" in text:
        return "TIMEOUT"
    if "null pointer" in text:
        return "NULL_POINTER"
    return "UNKNOWN"

for sample in ["Jenkins TIMEOUT", "Null pointer exception", "Disk full"]:
    print(classify(sample))
```
Output:
```text
TIMEOUT
NULL_POINTER
UNKNOWN
```
Parameters receive input. `return` gives a value to the caller; `print` displays information.

## 7. Exceptions

```python
from pathlib import Path
try:
    text = Path("sample.log").read_text(encoding="utf-8")
except FileNotFoundError:
    print("Log file not found; check the path.")
else:
    print("Read", len(text), "characters")
```
If the file is absent, output is `Log file not found; check the path.`.

## 8. Run examples and tests

Run `python examples.py` from this folder. From repository root, run:
```powershell
python -m unittest discover -s .\07-devops-ai-project\tests -v
```

## Exercises
1. Add a `permission denied` category.
2. Add tests for empty and unknown logs.
3. Return a recommendation instead of printing it.
4. Explain syntax errors versus runtime exceptions.

## Interview questions
- List versus dictionary?
- `print` versus `return`?
- How do `if`, `elif`, and `else` work?
- Why use exception handling for files?
- What does a unit test assert?
