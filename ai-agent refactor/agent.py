from llm.fake_llm import FakeLLM
from llm.ollama_llm import OllamaLLM
from registry import TOOLS
from tool_definitions import TOOL_DEFINITIONS
from state_manager import StateManager
from prompt_builder import PromptBuilder

MAX_STEPS = 10

class Agent:

    def __init__(self):
        self.llm = FakeLLM()
        #self.llm = OllamaLLM()
        self.state_manager = StateManager()
        self.prompt_builder = PromptBuilder()


    def run(self, question):
        state = {
            "question": question,
            "history": [],
            "finished": False,
            "stories": None,
            "current_story": None,
            "generated_test_cases": [],
            "current_story_index": 0,
            "test_case_exists": None
        }
        
        
        for _ in range(MAX_STEPS):
            prompt = self.prompt_builder.build(
                state,
                TOOL_DEFINITIONS
            )

            DEBUG = True

            if DEBUG:
                print(prompt)
            
        
            decision = self.llm.decide(prompt,state) #aca le el state
            print(f"\nThought: {decision['thought']}")
            print(f"Action: {decision['tool']}")

                    
            #a tool_name le asigno el nombre de la tool que me devolvio
            #la linea anterior, que es la decision del llm. Ejemplo: "create_test_case" o "get_open_bugs"             
            tool_name = decision["tool"] 

            #lo primero que chequeo, es que la tool no sea finish
            if decision["tool"] == "finish":
                print("\nAgent finished.\n")
                break


            #a args le asigno el nombre de los args que me devolvio
            #la linea anterior, que es la decision del llm. Ejemplo: {"story": "US-123"} o {}   
            args = decision["args"]
            
            #del registry de tools, busca la tool que coincide con el nombre
            #que me devolvio la llm. Pr ejempo: si tool_name es "create_test_case", tool va a ser la funcion 
            #create_test_case que esta en tools.py
            tool = TOOLS.get(tool_name) 

            if tool is None:
                return f"No existe la herramienta {tool_name}"

            #aca ejecuto la tool que me devolvio el llm, con los args que me devolvio el llm. Es como
            #hacer -si estoy en la tool create_test_cases: result = create_test_cases(test_case)
            result = tool(**args)
            self.state_manager.update(
                    state,
                    tool_name,
                    result
                )
                      
            
            
            if result["success"]:
                print("Observation:")
                print(result["data"])
            else:
                print("Observation:")
                print(f"ERROR: {result['error']}")

            state["history"].append({
                    "thought": decision["thought"],
                    "tool": decision["tool"],
                    "args": decision["args"],
                    "result": result
                })

            



               

        return self.llm.final_answer(state["history"])

       

        