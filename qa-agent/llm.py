import re

class FakeLLM:

    def decide(self, question, history):
            
        question = question.lower()

        if "bug" in question:
            return self.handle_bug(question, history)

        if "historia" in question:
            return self.handle_story(question, history)

        if "test" in question:
            return self.handle_test_case(question, history)

        return {
            "tool": "finish",
            "args": {}
        }

    
    def handle_bug(self, question, history):

        if len(history) == 0:

            return {
                "tool": "create_bug",
                "args": {}
            }

        if history[-1]["tool"] == "create_bug":  #Si el ultimo valor de history (que es result) es create bug

            return {
                "tool": "assign_bug",
                "args": {
                    "bug_id": history[-1]["result"],
                    "assignee": "Juan"
                }
            }

        return {
            "tool": "finish",
            "args": {}
        }

    
    def handle_story(self, question, history):

        if len(history) == 0:

            return {
                "tool": "get_jira_stories",
                "args": {}
            }

        return {
            "tool": "finish",
            "args": {}
        }
    
    def handle_test_case(self, question, history):

        if len(history) == 0:

            return {
                "tool": "get_jira_stories",
                "args": {}
            }

        if history[-1]["tool"] == "get_jira_stories":

            first_story = history[-1]["result"][0]

            return {
                "tool": "create_test_case",
                "args": {
                    "story": first_story
                }
            }

        return {
            "tool": "finish",
            "args": {}
        }

    def final_answer(self, history):

        if not history:
            return "No realicé ninguna acción."

        return "\n".join(
            f"{step['tool']} -> {step['result']}"
            for step in history
        )

       