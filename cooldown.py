class Cooldown:
    
    def __init__(self, tijd):
        self.tijd = tijd
        self.time = 0

    @property
    def ready(self):
        if self.time >= self.tijd:
            return True
        else:
            return False

    def update(self, elapsed_seconds):
        self.time += elapsed_seconds

    def reset(self):
        self.time = 0


class Cooldownmine:
  
    def __init__(self, tijd):
        self.tijd = tijd
        self.time = 0

    @property
    def ready(self):
        if self.time >= self.tijd:
            return True
        else:
            return False

    def update(self, elapsed_seconds):
        self.time += elapsed_seconds

    def reset(self):
        self.time = 0


