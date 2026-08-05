class FakeLLM:

    def decide(self, prompt, state):


        if "Current Story: None" in prompt and state["stories"] is not None:

            return {
                "thought": "Ya procesé todas las User Stories.",
                "tool": "finish",
                "args": {}
            }
        
        stories = state["stories"]
        current_story = state["current_story"]
        test_case_exists = state["test_case_exists"]


        # Estado 1: todavia no conozco historias. Debo obtenerlas
         
        if stories is None:

            return {
                "thought": "Todavía no conozco las User Stories. Primero debo obtenerlas.",
                "tool": "get_pending_user_stories",
                "args": {}
            }


        # Estado 2 : ya conozco las User Stories, pero no se aún si existen test cases
        # Acción: chequear que tengan test case

        if current_story is not None and test_case_exists is None:  
            return {

                "thought":
                f"Debo comprobar si {current_story['id']} ya tiene Test Cases.",

                "tool":
                "check_test_case_exists",

                "args":
                {
                    "story_id": current_story["id"]
                }

            }

        #Estado 3. Ya se si existe
        if test_case_exists is True:

            return {

                "thought":
                "La historia ya tiene Test Cases. Continuaré con la siguiente historia.",

                "tool":"finish",

                "args": {}

            }

        if test_case_exists is False:

            return {

                "thought":
                f"La historia  {current_story['id']} no tiene Test Cases. Crearé uno.",

                "tool":
                "create_test_case",

                "args":
                {
                    "test_case":
                    {
                        "title":
                        f"Test para {current_story['title']}"
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