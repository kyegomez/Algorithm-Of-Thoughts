[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)

# Algorithm-Of-Thoughts
![Discord](https://img.shields.io/discord/999382051935506503)
[![Twitter](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fkyegomez%2FAlgorithm-Of-Thoughts)](https://twitter.com/intent/tweet?text=Check%20out%20this%20amazing%20project%20on%20improving%20AI%20reasoning%20-%20Algorithm%20of%20Thoughts!%20https://github.com/kyegomez/Algorithm-Of-Thoughts)
[![LinkedIn](https://img.shields.io/badge/Share-LinkedIn-blue?style=social&logo=linkedin)](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fgithub.com%2Fkyegomez%2FAlgorithm-Of-Thoughts)
[![Facebook](https://img.shields.io/badge/Share-Facebook-blue?style=social&logo=facebook)](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fgithub.com%2Fkyegomez%2FAlgorithm-Of-Thoughts)
[![Reddit](https://img.shields.io/badge/Share-Reddit-orange?style=social&logo=reddit)](https://www.reddit.com/submit?url=https%3A%2F%2Fgithub.com%2Fkyegomez%2FAlgorithm-Of-Thoughts&title=Check%20out%20this%20amazing%20project%20on%20improving%20AI%20reasoning%20-%20Algorithm%20of%20Thoughts%21)
[![Hacker News](https://img.shields.io/badge/Share-Hacker%20News-orange?style=social&logo=y-combinator)](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fgithub.com%2Fkyegomez%2FAlgorithm-Of-Thoughts&t=Check%20out%20this%20amazing%20project%20on%20improving%20AI%20reasoning%20-%20Algorithm%20of%20Thoughts%21)
[![Pinterest](https://img.shields.io/badge/Share-Pinterest-red?style=social&logo=pinterest)](https://pinterest.com/pin/create/button/?url=https%3A%2F%2Fgithub.com%2Fkyegomez%2FAlgorithm-Of-Thoughts&media=https%3A%2F%2Fgithub.com%2Fkyegomez%2FAlgorithm-Of-Thoughts%2Fraw%2Fmain%2FAlgorithm-Of-Thoughts.jpeg&description=Check%20out%20this%20amazing%20project%20on%20improving%20AI%20reasoning%20-%20Algorithm%20of%20Thoughts%21)
[![WhatsApp](https://img.shields.io/badge/Share-WhatsApp-green?style=social&logo=whatsapp)](https://api.whatsapp.com/send?text=Check%20out%20this%20amazing%20project%20on%20improving%20AI%20reasoning%20-%20Algorithm%20of%20Thoughts%21%20https%3A%2F%2Fgithub.com%2Fkyegomez%2FAlgorithm-Of-Thoughts)


![AOT BANNER](aot.png)
The open source implementation of "Algorithm of Thoughts: Enhancing Exploration of Ideas in Large Language Models" that increases model reasoning by nearly 80% or 10% more than [Tree of thoughts!](https://github.com/kyegomez/Algorithm-Of-Thoughts)

[Algorithm of Thoughts: Enhancing Exploration of Ideas in Large Language Models](https://arxiv.org/abs/2308.10379)

# Installation
`pip install aot-x`


# Usage
```python
from aot.main import AoT

task = """

Use numbers and basic arithmetic operations (+ - * /) to obtain 24. When
considering the next steps, do not choose operations that will result in a
negative or fractional number. In order to help with the calculations, the
numbers in the parenthesis represent the numbers that are left after the
operations and they are in descending order.
Another thing we do is when there are only two numbers left in the parenthesis, we
check whether we can arrive at 24 only by using basic arithmetic operations
(+ - * /). Some examples regarding this idea:
(21 2) no
since 21 + 2 = 23, 21 - 2 = 19, 21 * 2 = 42, 21 / 2 = 10.5, none of which is equal
to 24.
(30 6) 30 - 6 = 24 yes
(8 3) 8 * 3 = 24 yes
(12 8) no
(48 2) 48 / 2 = 24 yes
Most importantly, do not give up, all the numbers that will be given has indeed a
solution.

14 8 8 2

OBJECTIVE
#########
5 10 5 2
"""


dfs = AoT(
    num_thoughts=2,
    max_steps=10, 
    value_threshold=1,
    initial_prompt=task,
    openai_api_key="ENETER IN YOUR API KEY"
)

result = dfs.solve()
print(result)
```

# Todo
- [ ] All thoughts over 0.5 are added to cache or longterm vectorstore 
- [x] DFS search similiar to Algorithm of thoughts
- [x] Propose solutions function
- [x] Backtrack to nearest successful states
- [x] Implement evaluation strategy similiar to tot with [0.0, 1.0]
- [x] Working demo: Conducts search then backtracks through states, provide visuals green text
- [ ] Streamlit demo


## Citation
```
@misc{2308.10379,
Author = {Bilgehan Sel and Ahmad Al-Tawaha and Vanshaj Khattar and Lu Wang and Ruoxi Jia and Ming Jin},
Title = {Algorithm of Thoughts: Enhancing Exploration of Ideas in Large Language Models},
Year = {2023},
```