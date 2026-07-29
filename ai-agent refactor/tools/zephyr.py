

def create_test_case(test_case):

    return {

        "success": True,

        "data": {
            "id": "TC-101"
        },

        "error": None

    }

def check_test_case_exists(story_id):

    existing_cases = {

        "US-101": True,
        "US-102": False

    }

    return {
        "success": True,
        "data": {
            "exists": existing_cases.get(story_id, False)
        },
        "error": None
    }