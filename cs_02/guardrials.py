from agents import Agent,Runner,input_guardrail,RunContextWrapper,GuardrailFunctionOutput,InputGuardrailTripwireTriggered,output_guardrail,OutputGuardrailTripwireTriggered,TResponseInputItem
from my_config.config import llm_model
import asyncio
from pydantic import BaseModel

class myDataOutput(BaseModel):
    is_hotel_greenland_related: bool
    is_account_related_query_of_greenland: bool
    reason: str






guardrail_agent=Agent(
    name="Guardrail Agent",
    instructions= 
    """
    You are a guardrail agent that ensures the assistant follows the rules.
    - Check only hotel greenland related queries
    - Check  account related queries of hotel greenland
    """,
    model = llm_model,
    output_type=myDataOutput
)




@input_guardrail
async def guardrail_input_function(ctx:RunContextWrapper, agent:Agent,input:str | list[TResponseInputItem])->GuardrailFunctionOutput:
    res= await Runner.run(guardrail_agent,input=input,context=ctx.context)
    return GuardrailFunctionOutput(
        output_info= res.final_output,
        tripwire_triggered = not res.final_output.is_hotel_greenland_related
        # True hoga toh tripwire trigger ho jayega or exception raise hogi
    )

@output_guardrail
async def guardrail_output_function(ctx:RunContextWrapper, agent:Agent,output:str)->GuardrailFunctionOutput:
    res= await Runner.run(guardrail_agent,input=output,context=ctx.context)
    return GuardrailFunctionOutput(
        output_info= res.final_output,
        tripwire_triggered = res.final_output.is_account_related_query_of_greenland
        # True hoga toh tripwire trigger ho jayega or exception raise hogi
    )

hotel_assistant=Agent(
    name="Hotel Assistant",
    instructions= 
    """
    Your are a hotel GreenLand Customer care Assistant.Your name is GreenLand Assistant.
    - hotel has 3 types of rooms: Single, Double, Suite.
    - hotel owner name is Mughees
    - hotel location is New York City
    - hotel has 20 rooms available
    - these are not avaliable for public booking it only for special guests
    """,
    model = llm_model,
    input_guardrails=[guardrail_input_function],
    output_guardrails=[guardrail_output_function],
)

async def main():
    try:
        res= await Runner.run(
            starting_agent=hotel_assistant,
            # input="2+2?" # Input Tripwire Triggered
            # input="Can you tell me about the hotel GreenLand?",
            # input="Can you tell me about the hotel GreenLand Accounts?", # Output Tripwire Triggered
            input="Can you tell me about the hotel GreenLand rooms and Owner?",

        )
        print(res.final_output)
    except InputGuardrailTripwireTriggered as e:
        print("Tripwire triggered:", e)
    
    except OutputGuardrailTripwireTriggered as e:
        print("Tripwire triggered:", e)


if __name__== "__main__":
    asyncio.run(main())








# from pydantic import BaseModel
# from my_config.config import llm_model
# import asyncio
# from agents import (
#     Agent,
#     GuardrailFunctionOutput,
#     OutputGuardrailTripwireTriggered,
#     RunContextWrapper,
#     Runner,
#     output_guardrail,
# )
# class MessageOutput(BaseModel): 
#     response: str

# class MathOutput(BaseModel): 
#     reasoning: str
#     is_math: bool

# guardrail_agent = Agent(
#     name="Guardrail check",
#     instructions="Check if the output includes any math.",
#     output_type=MathOutput,
#     model = llm_model,
# )

# @output_guardrail
# async def math_guardrail(  
#     ctx: RunContextWrapper, agent: Agent, output: MessageOutput
# ) -> GuardrailFunctionOutput:
#     result = await Runner.run(guardrail_agent, output.response, context=ctx.context)

#     return GuardrailFunctionOutput(
#         output_info=result.final_output,
#         tripwire_triggered=result.final_output.is_math,
#     )

# agent = Agent( 
#     name="Customer support agent",
#     instructions="You are a customer support agent. You help customers with their questions.",
#     output_guardrails=[math_guardrail],
#     output_type=MessageOutput,
#     model = llm_model,

# )

# async def main():
#     # This should trip the guardrail
#     try:
#         res=await Runner.run(agent, "Hello, can you help me solve for x: 2x + 3 = 11?")
#         print(res.final_output)
#         print("Guardrail didn't trip - this is unexpected")

#     except OutputGuardrailTripwireTriggered:
#         print("Math output guardrail tripped")

# if __name__== "__main__":
#     asyncio.run(main())


