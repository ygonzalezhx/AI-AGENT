

def get_user_stories():
    return [
        {
            "id": "US-101",
            "title": "Login"
        }
    ]

def get_pending_user_stories():

    return {

        "success": True,

        "data": [

            {
                "id": "US-101",
                "title": "Login de usuario",
                "description": "Como usuario quiere iniciar sesión"
            },
            {
                "id": "US-102",
                "title": "Registro",
                "description": "Como usuario quiere registrarse"
            }

        ],

        "error": None

    }