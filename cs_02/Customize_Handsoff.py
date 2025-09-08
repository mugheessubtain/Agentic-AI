from agents import Agent,Runner, function_tool,handoff,RunContextWrapper,function_tool
from myTools.math_tools import subtract_numbers, add_numbers, multiply_numbers, divide_numbers
from my_config.config import llm_model
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions,RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel
from agents.extensions import handoff_filters


# should be in input_Schema folder
# jb bhi dusra agent handsoff khry gaa sath woh yeh data bhi dy gaa woh advise, reason ya summary ho sakhti jo woh iss agent ko dy gaa
class InputData(BaseModel):
    reason:str
# agent communication depends on this wording or keywords

# In certain situations, you want the LLM to provide some data when it calls a handoff. 
# For example, imagine a handoff to an "MAth agent". You might want a reason to be provided, so you can log it.

#restriction to handsoff or condittion based to handsoff
async def check_handoff_enabled(ctx:RunContextWrapper,agent):
    if ctx.context["age"]>=18:
        return True
    return False




@function_tool
def weather(location:str)->str:
    """ weather Tool"""
    print(f"Weather tool called ->>>>>>>")
    return f"{location} Weather is very nice."



# should be in service folder
async def service(ctx:RunContextWrapper,input_data:InputData):
    print(ctx.context)
    print(f"math Agent Called with reason: {input_data.reason}")
# handsoff sa phaly ap context sa update ya manipulate kar saktay hein db sa data fetch kar saktay hein or km bhi handsoff sa phaly iss function ma kr saktay hein(LOGS MAINTAIN KAR SAKTAY HEIN)

math_assistant=Agent(
    name="Math Agent",
    instructions=prompt_with_handoff_instructions("You are helpful Math Agent"),
    # instructions=f"""{RECOMMENDED_PROMPT_PREFIX} andYou are helpful MAth Agent""",
    model=llm_model,
    tools=[add_numbers,subtract_numbers,multiply_numbers,divide_numbers],
    handoff_description="If the user asks for math-related help, provide detailed explanations and solutions."
    # this is for other agents to know when to handsoff to this agent
)


math_teacher=handoff(
    agent=math_assistant,
    tool_name_override="Mathematics_Teacher", # default is transfer_to_<agent_name>
    tool_description_override="This is specialized Mathematics Teacher.", # default is Transfers to any description of agent>,
    on_handoff=service ,# jab bhi handsoff hoga phaly yeh function chaly gaa phir agent chaly gaa.
    input_type=InputData,
    input_filter=handoff_filters.remove_all_tools,
    # jb handsoff hota haa woh tamam history deta haa iss agent ko iss sa bacchny ka lia yeh input filter use hota haa ky sirf specific info ya input ko filter kr ky dy
    # content mai tool call ka answer nhi ja raha
    # Calls _remove_tool_types_from_input to strip out any dict items of type "function_call", "function_call_output", "file_search_call", etc.
    # Calls _remove_tools_from_items to strip out any object versions of those (ToolCallItem, ToolCallOutputItem).
    is_enabled=check_handoff_enabled

)
assistant=Agent(
    name="Assistant Agent",
    instructions="You are helpful Agent and handsoff to sepecialized agents as needed",
    model=llm_model,
    handoffs=[math_teacher],
    tools=[weather],
)

result=Runner.run_sync(
    starting_agent=assistant,
    input="what is square of 12",
    # input="weather in karachi and what is square of 12",
# Weather tool called ->>>>>>>
# {'name': 'Mughees', 'age': 18, 'phone': 1234567890}
# math Agent Called with reason: What is the square of 12?
# The square of 12 is 144.

# Math Agent

# To avoid this we use input filter
    context={"name":"Mughees","age":17,"phone":1234567890}
)

print(result.final_output)
print(result.last_agent.name)

# print(assistant.handoffs)








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

