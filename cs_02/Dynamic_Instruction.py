from agents import Agent, Runner,RunContextWrapper
from main import llm_model
from dataclasses import dataclass

# Context can be Dataclass , pydantic class , simple pyhon class or Typeclass
@dataclass
class UserContext:
    """Context for the user."""
    name:str
    age:int 
    phone:int
    current_conservation:list[str]
    def get_memories(self):
        return f"{self.name} is {self.age} years old and have phone no : {self.phone}"
    def update_memory(self,memory:str):
        self.memories = memory
    def update_conservation(self,message:str):
        self.current_conservation.append(message)
user_1=UserContext(name="Mughees", age=18,phone=1234567890,current_conservation=["Hello","How are you?"])
user_2=UserContext(name="Mutahir", age=16,phone=1234567890,current_conservation=["Hi","How are you?"])

def dynamic_instruction(context:RunContextWrapper[UserContext],agent:Agent[UserContext])-> str:
    # print("Context:",context.context) # not getting name
    # print("Agent:",agent)
    context.context.update_memory(f"{context.context.name} is a user has a phone number {context.context.phone}")
    context.context.update_conservation("Added Dynamic Instruction")
    return f" The user name is {context.context.name}You are a helpful assistant. You can answer questions"
    # return f"You are a helpful assistant. You can answer questions"

# in this Dynamic Instruction first argument is context and second is agent
# we can change the name of parameters but first should be context and second should be agent
# it dosnt matter how many parameters you pass in Dynamic Instruction
# it will always take first as context and second as agent






agent=Agent[UserContext](
    name="General Agent",
    instructions=dynamic_instruction,
    model=llm_model,
)

result= Runner.run_sync(agent, "What is the name of user" , context=user_1)
# context doesnt goes to LLM, it goes to Dynamic Instruction
# Proof: As an AI, I don't have a name. You can call me Assistant or AI.
# Dynamic Instruction can access context and agent
print(result.final_output)
print(user_2.get_memories())
print(user_2.current_conservation)