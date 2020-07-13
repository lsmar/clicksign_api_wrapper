from typing import Dict


def check_response(resp: Dict) -> Dict:
    if resp.status_code == 400:
        raise BadRequest()
    elif resp.status_code == 401:
        raise Unauthorized()
    elif resp.status_code == 403:
        raise Forbidden()
    elif resp.status_code == 404:
        raise NotFound()
    elif resp.status_code == 422:
        raise UnProcessableEntity(resp.json().get('errors'))
    elif resp.status_code == 500:
        raise UnknownServerError()

    return resp


class Forbidden(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return 'ClickSign API Error: Forbidden! Please verify if your token is valid and if you are in the right environment.'


class Unauthorized(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return 'ClickSign API Error: Unauthorized! Invalid token.'


class BadRequest(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return 'ClickSign API Error: BadRequest! The request you send is not valid.'


class UnProcessableEntity(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return f'ClickSign API Error: UnProcessableEntity! The server was not able to process the request. The server error was: {self.error}.'


class NotFound(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return 'ClickSign API Error: NotFound! The server was not able to find this recurse.'


class UnknownServerError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return 'ClickSign API Error: UnknownServerError! The server was not able to process the request. Internal server error.'
