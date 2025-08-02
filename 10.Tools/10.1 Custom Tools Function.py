from autogen import AssistantAgent, UserProxyAgent
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

# Define a custom function to reverse a string
def reverse_string(text: str) -> str:
    """Reverse the given text.
    
    Args:
        text (str): Input string
        
    Returns:
        str: Reversed string
    """
    return text[::-1]

# Create configuration for the LLM
llm_config = {
    "config_list": [
        {
            "model": "gpt-4o",
            "api_key": api_key
        }
    ],
    "functions": [
        {
            "name": "reverse_string",
            "description": "Reverse a string",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to reverse",
                    }
                },
                "required": ["text"],
            },
        }
    ],
}

# Create an assistant agent with function calling
reverse_agent = AssistantAgent(
    name="ReverseAgent",
    llm_config=llm_config,
    system_message="You are a helpful assistant that can reverse text using the reverse_string function. Return the reversed string with a summary.",
)

# Create a user proxy agent to initiate conversations
user_proxy = UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    code_execution_config=False,
)

# Register the function with the user proxy
user_proxy.register_function(
    function_map={
        "reverse_string": reverse_string,
    }
)

# Define a task
task = "Reverse the text 'Hello, how are you Doing?'"

# Run the conversation
user_proxy.initiate_chat(
    reverse_agent,
    message=task,
)

# Print the conversation history
print("\nConversation History:")
for message in reverse_agent.chat_messages[user_proxy]:
    print(f"{message['name']}: {message['content']}")