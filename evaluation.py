test_cases = [
    {
        "question": "Can I work remotely from another country?",
        "expected_route": "RAG"
    },
    {
        "question": "How long do I have to submit travel expenses?",
        "expected_route": "RAG"
    },
    {
        "question": "What is the company headquarters?",
        "expected_route": "TOOL"
    },
    {
        "question": "How many employees does the company have?",
        "expected_route": "TOOL"
    }
]

from rag import route_question

correct = 0

for test in test_cases:
    actual_route = route_question(test["question"])

    if actual_route == test["expected_route"]:
        correct += 1
        print("PASS:", test["question"])
    else:
        print(
            "FAIL:",
            test["question"],
            "| Expected:", test["expected_route"],
            "| Got:", actual_route
        )

print(f"\nScore: {correct}/{len(test_cases)}")