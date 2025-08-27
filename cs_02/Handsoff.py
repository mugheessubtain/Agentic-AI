from agents import function_tool,Agent,Runner, trace
from my_config.config import llm_model
from myTools.math_tools import add_numbers, subtract_numbers, multiply_numbers, divide_numbers

@function_tool
def weather(location:str)->str:
    return f"the Weather in {location} is very nice"


weather_agent=Agent(
    name="Weather Agent",
    instructions=(
        "Always call the `weather_forecast` tool when the user asks about weather. "
        "Do not answer directly yourself."
    ),
    tools=[weather],
    model=llm_model,
    handoff_description="If the user asks for weather information, use the tool."
)


math_agent=Agent(
    name="Math Agent",
    instructions="Provide mathematical assistance and problem-solving.",
    tools=[add_numbers,subtract_numbers,multiply_numbers,divide_numbers],
    model=llm_model,
    handoff_description="If the user asks for math-related help, provide detailed explanations and solutions. and if ask weather related then handsoff to weather agent"
)


triage_agent=Agent(
    name="Triage Agent",
    instructions="Assist with triaging user requests and directing them to the appropriate agent.",
    handoffs=[weather_agent,math_agent],
    model=llm_model,
    handoff_description="If the user has a request, determine the appropriate agent to handle it."
)


async def main():
    with trace("Hansoff workflow"):
        result=await Runner.run(
        triage_agent,
        input="What is the weather in New York call the tool must?"
        )
        # result=await Runner.run(
        # triage_agent,
        # input="What is the 2+2 call the tool must?"
        # )


        print(result.final_output)
        print(result.last_agent.name)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())