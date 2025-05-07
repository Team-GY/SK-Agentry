class BaseAgent:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def run(self, input_data):
        raise NotImplementedError("Agent must implement run() method.")