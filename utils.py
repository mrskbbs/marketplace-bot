def fetchToken() -> tuple[str, str]:
    """
    Fetches data from .token file: 
     - First line is bot's token.
     - Second line is bot's name
    """
    
    with open(".token", "r", encoding = "utf-8") as f:
        token, name = f.readline().strip(), f.readline().strip()
    
    return token, name