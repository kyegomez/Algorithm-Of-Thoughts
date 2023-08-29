from swarms import OpenAI


class AoT:
    def __init__(self,
                 llm = None,
                 task: str = None):
        super(AoT, self).__init__()
        self.llm = llm
        self.task = task
    
    def run(self):
        self.llm.run(self.task)
