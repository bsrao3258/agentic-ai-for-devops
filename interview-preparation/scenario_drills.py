"""Example 2: interactive-free interview practice with model answers.

Run the script to print questions and a short answer outline. Practice expanding
each outline in your own words before reading it.
"""

DRILLS = [
    {
        "question": "A Jenkins pipeline times out. What do you check first?",
        "answer_outline": [
            "Preserve the relevant sanitized log lines and timestamps.",
            "Check upstream health, DNS, network path, and latency.",
            "Review timeout and retry settings without changing production.",
            "Propose a fix and request approval before any state change.",
        ],
    },
    {
        "question": "Why is a rule-based classifier not a full AI agent?",
        "answer_outline": [
            "Its decisions follow predefined conditions.",
            "It does not necessarily use an LLM to reason over context.",
            "An agent usually combines a goal, state, model reasoning, and tools.",
            "Tool access still needs validation, limits, and human approval.",
        ],
    },
]


if __name__ == "__main__":
    for index, drill in enumerate(DRILLS, start=1):
        print(f"Question {index}: {drill['question']}")
        for point in drill["answer_outline"]:
            print(f"  - {point}")
        print()
