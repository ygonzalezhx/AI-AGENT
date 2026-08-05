import json
import ollama


class OllamaLLM:

    def decide(self, prompt):

        response = ollama.chat(

            model="llama3",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        )

        text = response["message"]["content"]

        print("\n========== RESPUESTA DEL MODELO ==========\n")
        print(text)

        return json.loads(text)