class StateManager:

    def update(self, state, tool_name, result):

        #si la tool actual es get_pending_user_stories, actualizo el state, y ahora las stories alli 
        #son una lista [], con las user stories obtenidas del metodo get_pending_user_stories
        
        if tool_name == "get_pending_user_stories" and result["success"]:
            state["stories"] = result["data"]

            #inicializo con la primera historia de usuario
            state["current_story"] = result["data"][0]

            return

        if tool_name == "check_test_case_exists" and result["success"]:
            state["test_case_exists"] = result["data"]["exists"]

            if state["test_case_exists"]:
                self._move_to_next_story(state)
            return
        
        if tool_name == "create_test_case" and result["success"]:
            state["generated_test_cases"].append({
                "story": state["current_story"]["id"],
                "test_case": result["data"]["id"]})

            self._move_to_next_story(state)

    def _move_to_next_story(self, state):

        state["current_story_index"] += 1

        if state["current_story_index"] < len(state["stories"]):

            state["current_story"] = state["stories"][
                state["current_story_index"]
            ]

            state["test_case_exists"] = None

        else:

            state["current_story"] = None
            state["test_case_exists"] = None