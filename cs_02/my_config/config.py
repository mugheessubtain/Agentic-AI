from agents import AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
import os 

from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv("GOOGLE_API_KEY")
gemini_base_url = os.getenv("GEMINI_BASE_URL")

# print(gemini_api_key)

set_tracing_disabled(disabled=False)
# there are 3 types of configuration 
# 1. Agent level Configuration (based on llm expertise give model configuration on the agent level )
# 2. Runner  level Configuration ( in runner loop give configuration at the runner level all agent in this loop use same config irrespect of agent config if runner level only use this instead of agent level)
# 3. Global Level configuration (at global level set config for the whole project but have option to change model)

external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=gemini_base_url,
)
llm_model : OpenAIChatCompletionsModel=OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=  external_client,

)