from idom.backend import fastapi
from idom import component


base_url = "http://fastapi:8002"


def get_user():
    """
    Return role of logged in user.
    """
    role = None
    session = fastapi.use_scope()["session"]
    role = session["role"]
    return role


def fetch_username():
    """
    Return GitHub username of logged in user.
    """
    session = fastapi.use_scope()["session"]
    username = session["username"]
    return username
