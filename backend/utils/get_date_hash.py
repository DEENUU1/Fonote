from datetime import datetime


def get_date_hash() -> str:
    """
    Generates a hashed string based on the current date and time.

    Returns:
        str: A string representing the hashed value of the current date and time.
    """
    now = datetime.now()

    hashed = abs(hash(now))
    return str(hashed)
