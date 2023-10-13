from aot.openai import OpenAI
import json
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AoT:
    def __init__(
        self,
        num_thoughts: int = None,
        max_steps: int = None,
        value_threshold: float = None,
        pruning_threshold=0.5,
        backtracking_threshold=0.4,
        initial_prompt=None,
        openai_api_key: str = None,
        thought_cache=None  # Set to None here
    ):
        if thought_cache is None:
            self.thought_cache = {'accepted': {}, 'pruned': {}}
        else:
            self.thought_cache = thought_cache
        self.num_thoughts = num_thoughts
        self.max_steps = max_steps
        self.value_threshold = value_threshold
        self.backtracking_threshold = backtracking_threshold
        self.pruning_threshold = pruning_threshold
        self.initial_prompt = initial_prompt
        self.output = []
        self.openai_api_key = openai_api_key
        self.model = OpenAI(api_key=self.openai_api_key)

    def solve(self):
        try:
            # Run DFS
            self.dfs(self.initial_prompt, 1)

            # Check if any thoughts were generated
            if not self.output:
                logger.error("No valid thoughts were generated during DFS")
                return None

            # Find the best thought and its value
            best_state, best_value = max(self.output, key=lambda x: x[1])

            # Cache the best thought
            self.thought_cache['accepted'][best_state] = best_value

            # Generate the final solution based on the best thought
            solution = self.model.generate_solution(self.initial_prompt, best_state)

            # Display and return the solution
            print(f"Solution is {solution}")

            # Write cache to JSON file
            # Change back to 'w' if you want to overwrite the file
            with open('./thought_cache.json', 'a') as json_file:
                json.dump(self.thought_cache, json_file)

            return solution if solution else best_state

        except Exception as error:
            logger.error(f"Error in tot_dfs: {error}")

            # Write cache to JSON file even if an error occurs
            # Change back to 'w' if you want to overwrite the file
            with open('./thought_cache_error.json', 'a') as json_file:
                json.dump(self.thought_cache, json_file)

            raise error

    def dfs(self, state, step):
        if step > self.max_steps:
            # Check cache before evaluating
            if state in self.thought_cache['accepted']:
                value = self.thought_cache['accepted'][state]
            elif state in self.thought_cache['pruned']:
                return
            else:
                thought, value = self.evaluate_thought(state)
                # Cache the evaluated thought
                self.thought_cache['accepted'][state] = value
            
            self.output.append((state, value))
            return

        # Check cache before generating and filtering
        if state in self.thought_cache['accepted']:
            thoughts = [state]
        elif state in self.thought_cache['pruned']:
            return
        else:
            thoughts = self.generate_and_filter_thoughts(state)

        for next_state in thoughts:
            state_value = self.evaluated_thoughts.get(next_state, 0)
            print("Entering DFS with state: ", state, " and step: ", step)

            # Cache pruned thoughts
            if state_value <= self.value_threshold:
                self.thought_cache['pruned'][next_state] = state_value
                continue

            # Proceed with DFS
            child = (
                (state, next_state)
                if isinstance(state, str)
                else (*state, next_state)
            )
            self.dfs(child, step + 1)

            # Backtracking
            best_value = max([value for _, value in self.output])
            if best_value < self.backtracking_threshold:
                self.output.pop()
                continue

    def generate_and_filter_thoughts(self, state):
        # Check if thoughts for this state are cached
        if state in self.thought_cache['accepted']:
            print(f"Retrieved accepted thoughts from cache for state: {state}")
            return [state]
        elif state in self.thought_cache['pruned']:
            print(f"Retrieved pruned thoughts from cache for state: {state}")
            return []

        # Else generate new thoughts
        thoughts = self.model.generate_thoughts(
            state, self.num_thoughts, self.initial_prompt
        )

        self.evaluated_thoughts = self.model.evaluate_states(
            thoughts, self.initial_prompt
        )

        filtered_thoughts = [
            thought
            for thought in thoughts
            if self.evaluated_thoughts[thought] >= self.pruning_threshold
        ]

        # Cache the filtered thoughts
        for thought in filtered_thoughts:
            self.thought_cache['accepted'][thought] = self.evaluated_thoughts[thought]

        for thought in thoughts:
            if self.evaluated_thoughts[thought] < self.pruning_threshold:
                self.thought_cache['pruned'][thought] = self.evaluated_thoughts[thought]

        print("Generated Thoughts: ", thoughts)
        print("Evaluated Thoughts: ", self.evaluated_thoughts)

        print(f"filtered_thoughts: {filtered_thoughts}")
        return filtered_thoughts

    def evaluate_thought(self, state):
        # Check if the thought is already in the cache
        if state in self.thought_cache['accepted']:
            value = self.thought_cache['accepted'][state]
            print(f"Retrieved accepted thought value from cache: {value}")
            return state, value
        elif state in self.thought_cache['pruned']:
            value = 0  # or whatever value you use for pruned thoughts
            print(f"Retrieved pruned thought value from cache: {value}")
            return state, value

        # Otherwise, evaluate the thought
        thought = self.model.generate_thoughts(state, 1, self.initial_prompt)
        value = self.model.evaluate_states([state], self.initial_prompt)[state]

        # Update the cache based on the evaluation
        if value >= self.pruning_threshold:
            self.thought_cache['accepted'][state] = value
        else:
            self.thought_cache['pruned'][state] = value

        print(f"Evaluated thought: {value}")
        return thought, value