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
        print(f"\033[1;33;40m Decomposing the task: {self.task}  \n\033[0m") # Yellow color for thoughts
        self.llm.run(f"{self.system_prompt} Your task: {self.task}")
    
    def propose_solutions(self, subproblem):
        #propose solutions to subproblem ussing llm
        print(f"\033[1;33;40m Proposing solutions for: {subproblem}  \n\033[0m") # Yellow color for thoughts
        llm = OpenAI()
        response = llm(subproblem)
        return response
    
    def gauge_promise(self, solution, result):
        print(f"\033[1;33;40m Gauging promise for solution: {solution}  \n\033[0m") # Yellow color for thoughts
        return solution == result
    
    def backtrack(self):
        #backtrack to the most recent subproblems that still has unexplored solutions
        print(f"\033[1;33;40m Backtracking...  \n\033[0m") # Yellow color for thoughts
        if self.subproblems:
            print(f"\033[1;34;40m Sub Problems: {self.subproblems}  \n\033[0m") # Blue color for subproblems
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
            print(f"\033[1;32;40m Solution: {solution}  \n\033[0m") # Green color for solutions
            expected_result="expected_result"
            if self.gauge_promise(solution, expected_result):
                self.solutions.append(solution)    
        return self.solutions