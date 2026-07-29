from llm import FakeLLM
from registry import TOOLS

MAX_STEPS = 10

class Agent:

    def __init__(self):
        self.llm = FakeLLM()

    def run(self, question):
        history = [] #aca se podria guardar el historial de preguntas y respuestas, 
        #para que el llm pueda tener contexto. El historial solo vive en esa ejecucion
        
        for _ in range(MAX_STEPS):
            
        
            decision = self.llm.decide(question,history) #aca le mando la pregunta al llm y me devuelve la 
                #decision de que herramienta usar y qué argumentos
            print(f"\nThought: {decision['thought']}")
            print(f"Action: {decision['tool']}")

            if decision["tool"] == "finish":
                print("\nAgent finished.\n")
                break
                    
                
            tool_name = decision["tool"] #a tool_name le asigno el nombre de la tool que me devolvio
                    #la linea anterior, que es la decision del llm. Ejemplo: "create_test_case" o "get_open_bugs"
            
            args = decision["args"] #a args le asigno el nombre de los args que me devolvio
                    #la linea anterior, que es la decision del llm. Ejemplo: {"story": "US-123"} o {}

            tool = TOOLS.get(tool_name) #del registry de tools, busca la tool que coincide con el nombre
                    #que me devolvio la llm. Pr ejempo: si tool_name es "create_test_case", tool va a ser la funcion 
                    #create_test_case que esta en tools.py
            if tool is None:
                return f"No existe la herramienta {tool_name}"

            result = tool(**args)
                    #aca ejecuto la tool que me devolvio el llm, con los args que me devolvio el llm. Es como
                    #hacer -si estoy en la tool create_test_cases: result = create_test_cases(test_case)

            history.append({
                    "thought": decision["thought"],
                    "tool": decision["tool"],
                    "args": decision["args"],
                    "result": result
                })
            
            if result["success"]:
                print("Observation:")
                print(result["data"])
            else:
                print("Observation:")
                print(f"ERROR: {result['error']}")

               

        return self.llm.final_answer(history)

       

        