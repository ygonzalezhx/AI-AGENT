class PromptBuilder:

    def build(self, state, tools):
        prompt = f"""
        Pregunta:
        {state["question"]}

        Estado:
        Current Story: {state["current_story"]}
        Test Case Exists: {state["test_case_exists"]}
        Herramientas disponibles:
        """

        for tool in tools:
            prompt += f"- {tool['name']}: {tool['description']}\n"

        return prompt