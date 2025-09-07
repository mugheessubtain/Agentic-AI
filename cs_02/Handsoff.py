from agents import function_tool,Agent,Runner, trace,handoff,RunContextWrapper
from my_config.config import llm_model
from myTools.math_tools import add_numbers, subtract_numbers, multiply_numbers, divide_numbers
# from agents.extensions import handoff_filters

@function_tool
def weather(location:str)->str:
    """Get the current weather for a given location."""
    return f"the Weather in {location} is very nice"


weather_agent=Agent(
    name="Weather Agent",
    instructions=(
        "Always call the `weather` tool when the user asks about weather. "
        "Do not answer directly yourself."
    ),
    tools=[weather],
    model=llm_model,
 
    handoff_description="If the user asks for weather information, use the tool."

# instructions: How the agent should behave once it’s chosen.

# handoff_description: A “routing guide” that tells other agents (like triage) when to choose this agent.

# So, handoff_description isn’t used by the agent itself — it’s used by other agents (usually triage) to decide who should handle the request.
)


math_agent=Agent(
    name="Math Agent",
    instructions="Provide mathematical assistance and problem-solving.",
    tools=[add_numbers,subtract_numbers,multiply_numbers,divide_numbers],
    model=llm_model,
    handoffs=[weather_agent],
    handoff_description="If the user asks for math-related help, provide detailed explanations and solutions. and if ask weather related then handsoff to weather agent"
)


triage_agent=Agent(
    name="Triage Agent",
    instructions=(
         "If the user request involves multiple topics (e.g., math and weather), "
        "split the query, send each part to the correct agent, "
        "and then combine the responses into one final answer."

        # linear approach handsoff in sequence 

        # "If the user asks multiple questions (e.g., weather + math), "
        # "split them, send each part to the right agent, "
        # "collect their answers, and combine into a single response."
        # it gives proper ochestration (combines + collect but better approach is to use guardrails if user ask two domains questions in once )
        ),
    handoffs=[weather_agent,math_agent],
    model=llm_model,
    handoff_description="If the user has a request, determine the appropriate agent to handle it."
)


async def main():
    with trace("Hansoff workflow"):
        # result=await Runner.run(
        # triage_agent,
        # input="What is the weather in New York call the tool must?"
        # )

        # result=await Runner.run(
        # triage_agent,
        # input="What is the 2+2 call the tool must?"
        # )
        result= await Runner.run(
            triage_agent,
            "what is weather in karachi"
        )


        print(result.final_output)
        print(result.last_agent.name)



### Handsoff Function Parameters explained
# 1. agent

# The target agent you want to transfer to.

# Example: Weather agent, Math agent, Search agent, etc.

# 2. tool_name_override

# By default, the handoff tool name is auto-generated like:
# transfer_to_<agent_name>.

# If you want to give your handoff a custom name, you override this.

# Useful if you want more descriptive or shorter tool names.

# 3. tool_description_override

# Each tool has a default description, but you may want to provide a custom one.

# Example: Instead of "Transfers to weather agent", you can override with "Switch to weather assistant for current temperature updates".

# 4. on_handoff

# A callback function that runs as soon as the handoff is triggered.

# Can be used to:

# Start fetching data in the background

# Log the transfer

# Transform input before sending

# The callback gets:

# agent_context → the current state

# llm_input (optional) → if you want LLM-generated input passed through.

# 5. input_type

# Specifies what type of input this handoff expects.

# Example:

# "string" → expecting plain text

# "json" → structured data

# "number" → math input

# Helps ensure the next agent gets valid data.

# 6. input_filter

# Lets you filter or modify input before passing it to the next agent.

# Example:

# User says: “Tell me weather in Karachi tomorrow.”

# Input filter can extract only "Karachi" and send it to weather agent.

# 7. is_enabled

# Controls whether the handoff is active or not.

# Can be:

# true / false → static

# a function → dynamic runtime condition

# Example: Only enable handoff_to_weather if user is asking about weather.



if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
