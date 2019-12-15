import requests


def get_auth_token(request):
    """ 
    Возвращает токен аутентификации из реквеста
    """
    result = None
    auth_header = (request.headers or {}).get("Authorization")

    if auth_header:
        auth_method_name, token_value = auth_header.split(" ")
        if (auth_method_name or "").lower() == "token":
            result = token_value

    return result


def get_auth_token_from_request(request):
    """ Возвращает строку с токеном аутентификации из реквеста или None, если его там (в хедерах запроса) нет """
    return get_auth_token(request)


def check_auth_token(token_value):
    """ 
    Проверяет токен в сервисе auth
    """
    result = None

    try:
        r = requests.get("http://auth/auth", params=dict(token=token_value))

        if r.status_code == 200 and r.json().get("success"):
            result = r.json().get("data")

    except Exception as e:
        print("Exception: {}".format(e))

    return result


def region_identity(region):
    """ """
    return dict(region=region)
