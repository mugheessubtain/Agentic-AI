from my_config.config import llm_model
from agents import Agent,Runner,ModelSettings
from agents.agent import StopAtTools
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
    ],


    # tool_use_behavior="run_llm_again"
    # llm refine the tool response 


    tool_use_behavior=StopAtTools(stop_at_tool_names=["add_numbers"]),
    # if this tool is invoked then agent loop stops and return the answer which comes from this tool

    # tool_use_behavior="stop_on_first_tool"
    # return the tool response directly without llm refinement
    
    
    
    # model_settings=ModelSettings(tool_choice="required")
    # Default is auto Depend on llm to decide to call tool or not
    # none means tool can't reach to llm
    # required means tool must be called if needed or not

    model_settings=ModelSettings(tool_choice="subtract_numbers",parallel_tool_calls=False),
    # must yehi chaly gaa irrelevant to input bd mai phir thek tool khry gaa agr stop at tool choice na hoo

    reset_tool_choice=True
    

    # default is True


)

async def main():

    result= await Runner.run(
        starting_agent=mathAgent,
        input=
        "2+5 then -1?" ,
        max_turns=4
        # default is 10

    )
    print(result.final_output)
    # print(mathAgent.tools)




# Agent As a tool
# In some workflows, you may want a central agent to orchestrate a network of specialized agents, 
# instead of handing off control
# control reamin to an orchestrator agent while in hanfsoff the control is transfered to another agent


spanish_agent = Agent(
    name="Spanish agent",
    instructions="You translate the user's message to Spanish",
    model=llm_model,
)

french_agent = Agent(
    name="French agent",
    instructions="You translate the user's message to French",
    model=llm_model,
)

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools."
    ),
    model=llm_model,
    tools=[
        spanish_agent.as_tool(
            # these 2 are required parameters
            tool_name="spanish_Agent",
            tool_description="Translate the user's message to Spanish",
        ),
        french_agent.as_tool(
            tool_name="french_Agent",
            tool_description="Translate the user's message to French",
        ),
    ],
)

# async def main():
    # result = await Runner.run(orchestrator_agent, input="Say 'Hello, how are you?' in Spanish.")
    # print(result.final_output)
    # print(result.last_agent.name)
    # print(orchestrator_agent.tools)



if __name__ == "__main__":
    import asyncio
    asyncio.run(main())