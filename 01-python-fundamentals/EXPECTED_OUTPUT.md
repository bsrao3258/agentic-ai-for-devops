# Expected Output — Core Python Runnable Examples

Run from the repository root:

- Windows: `python .\\01-python-fundamentals\\examples_with_output.py`
- Linux/macOS: `python ./01-python-fundamentals/examples_with_output.py`

The following is the expected output. The path printed in section 11 can differ by operating system.

```text
1. VARIABLES AND TYPES
jenkins 3 int

2. OPERATORS
True True

3. STRINGS
error: connection timeout
True

4. LISTS
['jenkins', 'docker', 'kubernetes']
jenkins

5. TUPLES AND SETS
17.4
2

6. DICTIONARIES
jenkins
unassigned

7. CONDITIONS
Check network latency

8. LOOPS
Investigating: timeout
Investigating: disk full

9. FUNCTIONS
TIMEOUT
UNKNOWN

10. LIST COMPREHENSION
['jenkins', 'docker']

11. PATHS
logs/jenkins.log

12. EXCEPTIONS
Input must be an integer

13. CLASSES
jenkins: TIMEOUT

14. JSON
{"service": "jenkins", "severity": "high"}
high

15. ENVIRONMENT VARIABLES
development
```

On Windows, section 11 may print `logs\\jenkins.log` rather than `logs/jenkins.log`. If you set `APP_ENV` in your environment, section 15 prints that value instead of `development`.

## If your output differs

1. Check that you are running the script from the repository root.
2. Confirm you are using the intended Python interpreter.
3. Compare the section number where the output first differs.
4. Read the exception message carefully; do not hide it.
5. If you find a reproducible documentation or code error, open an issue or submit a fix.
