from agents import Agent, Runner ,function_tool,RunConfig,set_default_openai_client,set_default_openai_api
from my_config.config import llm_model,external_client
# Global Level Configuration( used same company LLMs)
set_default_openai_client(external_client)
set_default_openai_api("chat_completions")
# only pass model at Agent in model parameter like model="gemini-2.5-flash"

agent = Agent(name="Assistant", instructions="You are a helpful assistant" ,model="gemini-2.5-flash")
# Agent level Config

result = Runner.run_sync(
                        starting_agent=agent, 
                         input="Write the name of founder of openai.",
                        #  run_config=RunConfig(model=llm_model,model_provider=external_client)
                         )
print(result.final_output)
# Runner level Config

# from agents import enable_verbose_stdout_logging;
# enable_verbose_stdout_logging();
#TOOLS

# from agents import Agent, Runner,function_tool
# @function_tool
# def weather(city:str):
#     return f"The weather in {city} is sunny"


# agent = Agent(name="Assistant",tools=[weather] ,model=llm_model)

# result = Runner.run_sync(agent, "What is weather in karachi.")
# print(result.final_output)

## LLM will give final result 
# 1. Request goes to LLM 
# 2. LLM task to call Tool
# 3. then tool answer goes to LLM and then it give final result

# CLASS-02


# from agents import Agent, Runner, function_tool, ModelSettings
# @function_tool
# def get_weather(city: str) -> str:
#     """Returns weather info for the specified city."""
#     return f"The weather in {city} is sunny"


# agent = Agent(
#     name="General Agent",
#     instructions="Get weather or sum numbers.",
#     tools=[get_weather],
#     tool_use_behavior="stop_on_first_tool",
#     model=llm_model
# )

# result=Runner.run_sync(agent,"What is the weather in Islamabad ")
# print(result.final_output)

## In this case Tool will give final result 
# 1. Request goes to LLM 
# 2. LLM task to call Tool and then tool give final result


from agents import  ModelSettings
from agents.agent import StopAtTools
@function_tool
def get_weather(city: str) -> str:
    """Returns weather info for the specified city."""
    return f"The weather in {city} is sunny"
@function_tool
def sum_numbers(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b
# in functtion tool there is an parameter of is_enabled if we can make false to it the tool can't reach to the LLM but if we make model_settings.tool_choice="none" then it will reach to LLM but can't call the tool
agent = Agent(
    name="General Agent",
    instructions="Get weather or sum numbers.",
    tools=[get_weather,sum_numbers],
    # tool_use_behavior="stop_on_first_tool",
    # run_llm_again (DEfault)
    tool_use_behavior=StopAtTools(stop_at_tool_names=[get_weather]),
    model=llm_model,
    model_settings=ModelSettings(tool_choice="required"),
    # model_settings=ModelSettings(parallel_tool_calls=False),
    # LLM call , tool call , LLM response, tool call 2 and Final Res 

    # reset_tool_choice=False
    # if requied must call tool if need or not.
)
# result=Runner.run_sync(agent,"How are you")
# print(result.final_output)


result=Runner.run_sync(agent,"What is the weather in Islamabad and sum of 2+2")
print(result.final_output)

## In this case Tool will give final result for weather while for sum LLM will respond finally
# only weather tool if call then pause not for others