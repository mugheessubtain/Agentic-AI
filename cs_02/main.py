from agents import Agent, Runner , AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled,function_tool
import os
from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv("GOOGLE_API_KEY")
print(gemini_api_key)

set_tracing_disabled(disabled=True)

external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
llm_model : OpenAIChatCompletionsModel=OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=  external_client,
)
# from agents import enable_verbose_stdout_logging;
# enable_verbose_stdout_logging();

# agent = Agent(name="Assistant", instructions="You are a helpful assistant" ,model=llm_model)

# result = Runner.run_sync(agent, "Write the name of founder of openai.")
# print(result.final_output)


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