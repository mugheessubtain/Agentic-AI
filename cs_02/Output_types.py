# By default, agents return plain text, but you can specify an `output_type` to get structured outputs (e.g., Pydantic models, dataclasses, lists, TypedDicts).
from my_config.config import llm_model
from agents import Agent,Runner
# from dataclasses import dataclass
from pydantic import BaseModel

# Using simple Dataclass (Best practice in folder of dataTypes and in DataTypes Schema.py file)
# @dataclass
# class MyData:
#     n1:int
#     n2:int
#     result:str


# Using Pydantic BaseModel
class MyData(BaseModel):
    n1:int
    n2:int
    result:str

Math_agent= Agent(
    name="Math Agent",
    instructions="Perform basic math operations.",
    # tools=[],
    model=llm_model,
    output_type=MyData
)

result= Runner.run_sync(
    starting_agent=Math_agent,
    input="What is 2+3?",
)

print(result.final_output)


