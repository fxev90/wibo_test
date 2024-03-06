
def userSchema(user) -> dict:
    return {
        "id" : str(user["_id"]),
        "name" : user.get("name"),
        "username" : user.get("username"),
        "email" : user.get("email"),
    }
    
def usersSchema(users) -> list:
    return [userSchema(user) for user in users]

def serializeDict(a) -> dict:
    return {**{i: str(a[i]) for i in a if i == '_id'}, **{i: a[i] for i in a if i != '_id'}}


def serializeList(user) -> list:
    return [serializeDict(a) for a in user]