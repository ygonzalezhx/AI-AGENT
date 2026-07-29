class FakeLLM:

    def decide(self, state,tools):
        stories = state["stories"]
        current_story = state["current_story"]
        existing_test_case = state["test_case_exists"]


        print("\n========== PROMPT ==========")
        print(f"Pregunta: {state['question']}")
        print()


        print("Herramientas disponibles:")

        for tool in tools:
            print(f"- {tool['name']}: {tool['description']}")

        print("============================\n")


        # Estado 1: todavia no conozco historias. Debo obtenerlas
         
        if stories is None:

            return {
                "thought": "Todavía no conozco las User Stories. Primero debo obtenerlas.",
                "tool": "get_pending_user_stories",
                "args": {}
            }


        # Estado 2 : ya conozco las User Stories
        # Acción: crear un Test Case.

        if current_story is not None:

            if existing_test_case is None:

                return {
                    "thought": f"Crearé un Test Case para {current_story['id']}.",
                    "tool": "create_test_case",
                    "args": {
                        "test_case": {
                            "title": f"Test para {current_story['title']}"
                        }
                    }
                }


        # Estado: no quedan historias por procesar
        # Acción: finalizar.
        return {
            "thought": "Ya procesé todas las User Story",
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