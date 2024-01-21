import datetime
import requests
from config import TOKENS




class User:
    """
    Basic User class impl to hold data from API request properly.

    Attributes
    - username - user's login. Type: string
    - is_staff - check if user is staff. Type: bool
    """
    id: int
    username: str
    email: str
    is_staff: bool
    access: str
    refersh: str
    
    def __init__(self, identifier, username, email, is_staff, access, refresh):
        """
        This class is basically a data bucket for all of the user info
        """
        self.id = identifier
        self.username = username
        self.email = email
        self.is_staff = is_staff
        self.access = access
        self.refersh = refresh

    def __str__(self):
        if self.is_staff:
            return f"Marketplace staff\nUsername: {self.login}\nID: {self.id}\nAccess: {self.access}\nRefresh: {self.refersh}"
        return f"Marketplace customer\nUsername: {self.login}\nID: {self.id}\nAccess: {self.access}\nRefresh: {self.refersh}"




def getUser(email, password) -> User:
    """
    Sends an API request to the server and gets the user dict if succesfull.
    Otherwise returns None
    """
    # Send an api request to retrive user access and refresh tokens
    post = {"email": email, "password": password}
    data = requests.post(f"{TOKENS['ADRESS']}:{TOKENS['USER_PORT']}/api/v1/auth/jwt/create/", data = post)

    # If something went wrong drop out of the function
    if data.status_code != 200:
        return None

    # Collect tokens and send API get request
    tokens = data.json()
    get = {"authorization": f"JWT {tokens['access']}"}
    data = requests.get(f"{TOKENS['ADRESS']}:{TOKENS['USER_PORT']}/api/v1/auth/users/me/", headers = get).json()

    # Init user with the data from API GET call  
    user = User(
        identifier = data["id"], 
        username = data["username"],
        email = data["email"],
        is_staff = data["is_staff"],
        access = tokens["access"],
        refresh = tokens["refresh"],
    )
    
    return user




def getOrders(filter: dict) -> str:
    """
    Makes an API call which retrives order info based on provided filters
    """
    def prettify(order) -> str:
        """
        Creates a pretty output string, basically formatting function
        """
        header: str = f"<u>ID заказа: #{order['status']['id']} | Пользователь: {order['user_email']}</u>\n"
        body: str = f"Статус: {order['status']['status']}\n"

        date = datetime.datetime.fromisoformat(order['status']['created']) 
        body += f"Создан: {date.strftime('%d.%m.%Y %H:%M')}\n"

        body += f"Общая стоимость: {order['cost']}\n"

        count = 1
        for product in order['products']:
            body += f"Продукт №{count}: {product['product']['name']}\n"
            body += f"  -Количество: {product['amount']}\n"
            body += f"  -Стоимость одной штуки: {product['product']['final_cost']}\n"
            body += f"  -Стоимость всего: {product['product_cost']}\n"
            count += 1

        return header+body

    # Make an API call
    try:
        orders: list[dict] = requests.get(f"{TOKENS['ADRESS']}:{TOKENS['ORDER_PORT']}/api/v1/orders/", params = filter).json()["results"]
    except requests.JSONDecodeError:
        return None
    
    out: list[str] = []

    # A bit of shitty code down here
    # Filter out fresh orders 
    if "fresh" in filter:
        for order in orders:
            delta: datetime.timedelta = datetime.datetime.now().astimezone() - datetime.datetime.fromisoformat(order['status']['created']).astimezone()
            fresh: bool = delta.days < 11
            if fresh:
                out.append(prettify(order))
    # If there's no fresh, just put loop through the orders and call it a day
    else:
        for order in orders:
            out.append(prettify(order))

    if len(out) == 0:
        return "Заказов нет"
    return "\n\n".join(out)