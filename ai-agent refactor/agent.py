from llm import FakeLLM
from registry import TOOLS
from tool_definitions import TOOL_DEFINITIONS
MAX_STEPS = 10

class Agent:

    def __init__(self):
        self.llm = FakeLLM()

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
            
        
            decision = self.llm.decide(state,TOOL_DEFINITIONS) #aca le el state
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
                  
            #si la tool actual es get_pending_user_stories, actualizo el state, y ahora las stories alli 
            #son una lista [], con las user stories obtenidas del metodo get_pending_user_stories
            if tool_name == "get_pending_user_stories" and result["success"]:
                state["stories"] = result["data"]

                #inicializo con la primera historia de usuario
                state["current_story"] = result["data"][0]

            state["history"].append({
                    "thought": decision["thought"],
                    "tool": decision["tool"],
                    "args": decision["args"],
                    "result": result
                })

            if tool_name == "check_test_case_exists":
                state["test_case_exists"]

            
            if tool_name == "create_test_case" and result["success"]:
                state["generated_test_cases"].append({
                    "story": state["current_story"]["id"],
                    "test_case": result["data"]["id"]})

                state["current_story_index"] += 1
            
            
            if result["success"]:
                print("Observation:")
                print(result["data"])
            else:
                print("Observation:")
                print(f"ERROR: {result['error']}")

            if state["current_story_index"] < len(state["stories"]):
                state["current_story"] = state["stories"][state["current_story_index"]]
            else:
                state["current_story"] = None
           
            



               

        return self.llm.final_answer(state["history"])

       

        