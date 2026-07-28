def get_jira_stories():
    return [
        "US-101 Login",
        "US-102 Register",
        "US-103 Cart"
    ]


def create_test_case(story):
    return f"Test case creado para {story}"

def create_bug():
    return "Bug creado"


def get_open_bugs():
    return [
        "BUG-201",
        "BUG-202",
        "BUG-203",
        "BUG-204"
    ]

def assign_bug(bug_id, assignee):
    return f"Bug {bug_id} asignado a {assignee}"