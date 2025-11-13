import constants as c

class ChatLog():
    def __init__(self):
        self.council_cl = []
        self.peasant_cl = []

    def add_message(self, sender, log, message):
        if log == c.COUNCIL:
            self.council_cl.append((sender, message))
        elif log == c.PEASANT:
            self.peasant_cl.append((sender, message))
        else:
            raise ValueError(f"Unknown log: {log}")

    def clear_chat_log(self, log = "all"):
        if log == c.COUNCIL:
            self.council_cl = []
        elif log == c.PEASANT:
            self.peasant_cl = []
        elif log == "all":
            self.council_cl = []
            self.peasant_cl = []
        else:
            raise ValueError(f"Unknown log: {log}")
    