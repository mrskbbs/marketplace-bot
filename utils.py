import requests

class User:
    """
    Basic User class impl to hold data from API request properly.

    Attributes
    - username - user's login. Type: string
    - is_staff - check if user is staff. Type: bool
    """
    id: int
    username: str
    is_staff: bool
    
    def __init__(self, identifier, username, is_staff):
        self.id = identifier
        self.username = username
        self.is_staff = is_staff

    def __str__(self):
        if self.is_staff:
            return f"Marketplace staff\nUsername: {self.login}\nID: {self.id}"
        return f"Marketplace customer\nUsername: {self.login}\nID: {self.id}"


def fetchToken() -> tuple[str, str]:
    """
    Fetches data from .token file: 
     - First line is bot's token.
     - Second line is bot's name
    """
    d: dict = dict()

    with open(".token", "r", encoding = "utf-8") as f:
        for line in f:
            try:
                key, val = line.split("=")
                d[key.strip()] = val.strip()
            except ValueError:
                continue

    return d

def getUser(username, password) -> User:
    """
    Sends an API request to the server and gets the user dict if succesfull.
    Otherwise returns None
    """
    #! TODO: API request impl
    #########################
    # json = {"username": username, "password": password}
    # data = requests.post("http://5.35.91.117:8000/api/v1/auth/jwt/create/", data = json)

    # if data.status_code != 200:
    #     return None
    
    user: User = None
    if username == "mrskbbs" and password == "admin1":
        user = User(1,username, True)
    elif username == "johndoe" and password == "customer":
        user = User(1,username, False)
    
    return user

def getOrders(filter) -> str:
    """
    Makes an API call and retrives order info based on provided filters
    """
    #! TODO: API request the orders
    #        Parse JSON and get the orders data in orders array
    #        !!! Return None if user is invalid  !!!!
    ###############################################################
    filtered: list[str] = []
    for order in orders:
        valid: bool = True
        for key in filter:
            if order[key] != filter[key]:
                valid = False
                break
        if valid:
            filtered.append(f"Id: #{order['id']} | User: {order['user']}")

    if filtered != []:
        return "\n".join(filtered)
    
    return None