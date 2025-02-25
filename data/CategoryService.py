from data.Service import Service

service = Service()

def get_categories_place():
    return service.get("place-categories")

def get_categories_event():
    return service.get("event-categories")
