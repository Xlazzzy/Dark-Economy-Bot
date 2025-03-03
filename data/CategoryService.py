from data.Service import Service

service = Service()

def get_categories_place():
    """Returns all location categories"""

    return service.get("place-categories")

def get_categories_event():
    """Returns all event categories"""

    return service.get("event-categories")
