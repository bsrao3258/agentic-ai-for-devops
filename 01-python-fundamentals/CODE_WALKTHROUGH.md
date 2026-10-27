# Python Fundamentals — Line-by-Line Code Walkthrough

This guide explains what each important line does. Run the examples from the repository root or from this folder as noted.

## Example 1: Variables and types

```python
service = "jenkins"
retry_count = 3
pipeline_ok = False
print(service, retry_count, pipeline_ok)
print(type(retry_count).__name__)
```

Line by line:
- `service = "jenkins"`: creates a variable named `service` and stores text (a string).
- `retry_count = 3`: stores the integer `3`; it could represent a retry count.
- `pipeline_ok = False`: stores a Boolean value, either `True` or `False`.
- `print(...)`: displays all three values separated by spaces.
- `type(retry_count)`: asks Python for the value's type; `. __name__` (written `.__name__` without the space) gets the readable type name.

Output:
```text
jenkins 3 False
int
```

## Example 2: Strings and case-insensitive matching

```python
message = "ERROR: Connection TIMEOUT"
print(message.lower())
print("timeout" in message.lower())
```

- The first line stores a log message in a string.
- `message.lower()` returns a lowercase copy; it does not change the original string.
- `"timeout" in message.lower()` checks whether the substring `timeout` occurs in the normalized text. The result is a Boolean.

Output:
```text
error: connection timeout
True
```

## Example 3: Conditions

```python
log = "Connection timeout".lower()
if "timeout" in log:
    print("Check network latency and server health.")
elif "null pointer" in log:
    print("Check variable initialization.")
else:
    print("Collect more evidence.")
```

- `log = ...` stores a lowercase log string.
- `if` checks the first condition. If it is true, Python runs its indented block.
- `elif` means “otherwise, check this condition.” It is checked only if the preceding `if` was false.
- `else` runs only if none of the previous conditions matched.
- Indentation defines which statements belong to each block.

Output: `Check network latency and server health.`

## Example 4: Functions, parameters, and return values

```python
def classify(logs):
    text = logs.lower()
    if "timeout" in text:
        return "TIMEOUT"
    if "null pointer" in text:
        return "NULL_POINTER"
    return "UNKNOWN"

print(classify("Jenkins TIMEOUT"))
```

- `def classify(logs):` defines a reusable function named `classify`; `logs` is its parameter.
- `text = logs.lower()` normalizes the supplied input.
- The first `if` looks for a timeout pattern.
- `return "TIMEOUT"` sends a result back to the caller and exits the function.
- The second `if` checks a different known pattern.
- `return "UNKNOWN"` is the fallback when neither pattern matches.
- `classify("Jenkins TIMEOUT")` calls the function with an argument.
- `print(...)` displays the returned result.

Output: `TIMEOUT`

## Example 5: The examples.py classifier

Open [examples.py](examples.py). Its main ideas are:
- `def classify(logs: str) -> str`: defines a function; the annotations suggest a string input and string result. Python does not enforce these annotations automatically.
- `text = logs.lower()`: normalizes case once.
- Each `if` / `elif` checks a known log pattern in priority order.
- `return` stops the function at the first match.
- `return "UNKNOWN"` handles unrecognized input.
- `recommendation(error_type: str) -> str`: maps a category to a human-readable suggestion.
- `suggestions = {...}`: a dictionary maps category keys to text values.
- `suggestions[error_type]`: retrieves the value for the requested category. An unexpected key would raise `KeyError`, so validate categories if input can be untrusted.
- `if __name__ == "__main__":`: runs the demonstration only when this file is executed directly, not when imported as a module.
- `for sample in samples:`: processes each example in sequence.
- The f-strings such as `f"Class: {result}"` insert variable values into output text.

Run it with `python .\01-python-fundamentals\examples.py` on Windows or `python ./01-python-fundamentals/examples.py` on Linux from the repository root.

## Practice
Change a sample to `Permission denied`, run the program, and trace which condition matches. Then add a new condition and explain why its position matters.
