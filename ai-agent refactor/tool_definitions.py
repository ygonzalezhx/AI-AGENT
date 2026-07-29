#aca se describen las funciones

TOOL_DEFINITIONS = [

    {
        "name": "get_pending_user_stories",

        "description":
            "Obtiene todas las User Stories pendientes desde Jira.",

        "parameters": {}
    },

    {
        "name": "create_test_case",

        "description":
            "Crea un Test Case en Zephyr.",

        "parameters": {

            "test_case":
                "Información del test case a crear."

        }

    },

    {
        "name": "check_test_case_exists",

        "description": 
            "Comprueba si una User Story ya tiene Test Cases.",
            
        "parameters": {}
    },

]