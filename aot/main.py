from swarms import OpenAI


class AoT:
    def __init__(self,
                 llm = None,
                 task: str = None,
                 system_prompt: str = None):
        super(AoT, self).__init__()
        self.llm = llm
        self.task = task
        self.subproblems = []
        self.solutions = []
        self.system_prompt = system_prompt

    def decompose(self):
        self.llm.run(f"{self.system_prompt} Your task: {self.task}")
    
    def propose_solutions(self, subproblem):
        #propose solutions to subproblem ussing llm
        llm = OpenAI()
        response = llm(subproblem)
        return response
    
    def gauge_promise(self, solution, result):
        return solution == result
    
    def backtrack(self):
        #backtrack to the most recent subproblems that still has unexplored solutions
        if self.subproblems:
            return self.subproblems.pop()
        else:
            return None

    
    def run(self):
        self.decompose()
        while self.subproblems:
            subproblem = self.backtrack()
            if subproblem is None:
                break
            solution = self.propose_solutions(subproblem)
            expected_result="expected_result"
            if self.gauge_promise(solution, expected_result):
                self.solutions.append(solution)    
        return self.solutions