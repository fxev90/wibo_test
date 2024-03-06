
def catSchema(cat) -> dict:
    return {
        "id" : str(cat["_id"]),
        "name" : cat.get("name"),
        "breed" : cat.get("breed"),
        "age" : cat.get("age"),
        "gender" : cat.get("gender"),
        "status" : cat.get("status"),
        "description" : cat.get("description"),
    }
    
def catsSchema(cats) -> list:
    return [catSchema(cat) for cat in cats]
