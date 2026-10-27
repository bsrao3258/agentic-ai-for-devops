"""Two simple functions demonstrate separated responsibilities."""


def investigator_agent(logs):
    if "timeout" in logs.lower():
        return "Likely network or server timeout."
    if "null pointer" in logs.lower():
        return "Likely uninitialized or unexpected null value."
    return "Cause not identified; collect more evidence."


def recommendation_agent(finding):
    return (
        f"Recommended next step: investigate the finding: {finding} "
        "and obtain human approval before changes."
    )


if __name__ == "__main__":
    logs = "Jenkins connection timeout"
    finding = investigator_agent(logs)
    print("Investigation:", finding)
    print(recommendation_agent(finding))
