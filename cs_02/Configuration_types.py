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
