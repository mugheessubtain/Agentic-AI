from agents import Agent,Runner,SQLiteSession
from my_config.config import llm_model
import asyncio


    
# @function_tool
# async def summary_generator(ctx:RunContextWrapper[BookContext],agent:Agent)->str:
#     """"Generate Summary of the book name from the context"""
#     return f"The Book name is '{ctx.context.title}' by {ctx.context.author}, published in {ctx.context.year}.Summary is {agent.final_output if agent.final_output else 'No summary available yet.'}"

async def main():
    session=SQLiteSession("user1","assistant_sessions.db")
    Assistant=Agent(
        name="Assistant agent",
        instructions="You are helpful assistant that helps users ",
        model=llm_model,
        # tools=[summary_generator]
    )
    while True:
        user_input=input("User: ")
        if user_input.lower() in ['exit','quit']:
            print("Exiting the  assistant. Goodbye!")
            break
        result=await Runner.run(
            Assistant,
            input=user_input,
            session=session
        )
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())



