from pymud.dal import db


async def authenticate(username, password):
    """
    Authenticate a username and password against the database

    :param username:
    :param password:
    :return: bool indicating authentication success
    """
    doc = db.users.find_one({
        'username': username,
        'password': password
    })

    return doc is not None
