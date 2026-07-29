class FakeLLM:

    def decide(self, question, history):

        # Primer paso:
        # todavía no tengo historias

  
        if len(history) == 0:

            return {
                "thought": "Todavía no conozco las User Stories. Primero debo obtenerlas.",
                "tool": "get_pending_user_stories",
                "args": {}
            }


        # Segundo paso:
        # ya tengo historias

        if history[-1]["tool"] == "get_pending_user_stories":

            stories = history[-1]["result"]["data"]


            return {
                "thought": "Ya obtuve las historias. Ahora crearé un test para la primera.",
                "tool": "create_test_case",
                "args": {
                    "test_case": {
                        "title": f"Test para {stories[0]['title']}"
                    }
                }
            }

        last_result = history[-1]["result"]

        if not last_result["success"]:

            return {

                "thought": (
                    f"La herramienta falló: {last_result['error']}. "
                    "Finalizaré la ejecución."
                ),

                "tool": "finish",

                "args": {}

    }

        return {
            "thought": "Ya ejecuté todas las acciones necesarias.",
            "tool": "finish",
            "args": {}
        }


    def final_answer(self, history):

        lines = []

        for step in history:

            result = step["result"]

            if result["success"]:

                lines.append(
                    f"✔ {step['tool']} ejecutada correctamente."
                )

            else:

                lines.append(
                    f"✘ {step['tool']} falló: {result['error']}"
                )

        return "\n".join(lines) 