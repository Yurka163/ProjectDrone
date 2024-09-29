class Drone:
    def __init__(self, id: int, model: str):
        self.id = id
        self.model = model
        self.status = None
        self.battery_lvl = 100

