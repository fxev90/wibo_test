
def userSchema(user) -> dict:
    return {
        "id" : str(user["_id"]),
        "name" : user.get("name"),
        "username" : user.get("username"),
        "email" : user.get("email"),
    }