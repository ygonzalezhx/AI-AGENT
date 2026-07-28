class FakeLLM:

    def decide(self, question, history):

        # Primer paso:
        # todavía no tengo historias

  
        if len(history) == 0:

            return {
                "tool": "get_pending_user_stories",
                "args": {}
            }


        # Segundo paso:
        # ya tengo historias

        if history[-1]["tool"] == "get_pending_user_stories":

            stories = history[-1]["result"]


            return {
                "tool": "create_test_case",
                "args": {
                    "test_case": {
                        "title": f"Test para {stories[0]['title']}"
                    }
                }
            }


        return {
            "tool": "finish",
            "args": {}
        }



    def final_answer(self, history):

        return "\n".join(
            str(step["result"])
            for step in history
        )