#TODO: Implement DFS over thoughts evaluated with a series from 0,1 
#TODO: All thoughts over 0.5 are added to cache or longterm vectorstore 
from logging import Logger
from aot.chatgpt import ChatGPT


class AoT:
    def __init__(self,
                #  llm = None,
                 task: str = None,
                 system_prompt: str = None):
        super(AoT, self).__init__()
        self.llm = ChatGPT()
        self.task = task
        self.subproblems = []
        self.solutions = []
        self.system_prompt = system_prompt

    def decompose(self):
        print(f"\033[1;33;40m Decomposing the task: {self.task}  \n\033[0m") # Yellow color for thoughts
        self.llm.run(query=f"{self.system_prompt} Your task: {self.task}")
    
    def propose_solutions(self, subproblem):
        #propose solutions to subproblem ussing llm
        print(f"\033[1;33;40m Proposing solutions for: {subproblem}  \n\033[0m") # Yellow color for thoughts
        response = self.llm.run(query=subproblem)
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
    

class DFS:
    def __init__(self, 
                 num_thoughts: int = None, 
                 max_steps: int = None, 
                 value_threshold: float = None, 
                 pruning_threshold=0.5,
                 initial_prompt=None):
        self.num_thoughts = num_thoughts
        self.max_steps = max_steps
        self.value_threshold = value_threshold
        self.pruning_threshold = pruning_threshold
        self.initial_prompt = initial_prompt
        self.output = []

    def solve(self):
        try:
            self.dfs(self.initial_prompt, 1)
            best_state, _ = max(self.output, key=lambda x: x[1])
            solution = self.model.generate_solution(self.initial_prompt, best_state)
            print(f"Solution is {solution}")
            return solution if solution else best_state
        except Exception as e:
            Logger.error(f"Error in tot_dfs: {e}")
            raise e

    def dfs(self, state, step):
        if step > self.max_steps:
            thought, value = self.evaluate_thought(state)
            self.output.append((thought, value))
            return

        thoughts = self.generate_and_filter_thoughts(state)
        for next_state in thoughts:
            state_value = self.evaluated_thoughts[next_state]
            if state_value > self.value_threshold:
                child = (state, next_state) if isinstance(state, str) else (*state, next_state)
                self.dfs(child, step + 1)

    def generate_and_filter_thoughts(self, state):
        thoughts = self.model.generate_thoughts(state, self.num_thoughts, self.initial_prompt)
        self.evaluated_thoughts = self.model.evaluate_states(thoughts, self.initial_prompt)
        filtered_thoughts = [thought for thought in thoughts if self.evaluated_thoughts[thought] >= self.pruning_threshold]
        print(f"filtered_thoughts: {filtered_thoughts}")
        return filtered_thoughts

    def evaluate_thought(self, state):
        thought = self.model.generate_thoughts(state, 1, self.initial_prompt)
        value = self.model.evaluate_states([state], self.initial_prompt)[state]
        print(f"Evaluated thought: {value}")
        return thought, value
