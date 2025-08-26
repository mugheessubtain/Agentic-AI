from my_config.config import llm_model
from agents import Agent,Runner
# from Output_types import MyData
from myTools.math_tools import add_numbers, subtract_numbers, multiply_numbers, divide_numbers


mathAgent=Agent(
    name="Math Agent",
    instructions="Perform basic math operations.",
    model=llm_model,
    tools=[
        add_numbers,
        subtract_numbers,
        multiply_numbers,
        divide_numbers
    ]
)


result= Runner.run_sync(
    starting_agent=mathAgent,
    input=
    "What is 10 + 5, 20 - 4, 3 * 7, and 16 / 4?" 

)
print(result.final_output)