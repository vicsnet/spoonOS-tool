import asyncio

from spoon_ai.agents.toolcall import ToolCallAgent
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager
from spoon_ai.tools.base import BaseTool
from spoon_ai.tools.crypto_tools import get_crypto_tools

class GreetingTool(BaseTool):
    name: str = "greeting"
    description: str = "Generate personalised greetings"

    parameters: dict = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Person's name",
            }
        },
        "required": ["name"],
    }

    async def execute(self, name: str) -> str:
        # f"... {name} ..." is called an f-string in Python
        return f"Hello {name}! Welcome to SpoonOS!"
    

class CryptoPriceAgent(ToolCallAgent):
    name: str = "crypto_price_agent"
    description: str = "Agent can fetch crypto prices using Web3 tools"

    system_prompt: str = """
    You are a Web3-native AI assistant with access to crypto price tools.
    When the user asks about crypto prices, call the appropriate tool
    and answer in a clear, simple way.
    """

    available_tools: ToolManager = ToolManager(
        [
            GreetingTool(),
            *get_crypto_tools(),
        ]
    )


async def main():

    agent = CryptoPriceAgent(
        llm=ChatBot(
            llm_provider="deepseek",
            model_name="deepseek-chat",
        )
    )

    question = "What is the current price of Bitcoin in USD?"

    response = await agent.run(question)
    print(question)
    print("Agent response:")
    print(response)
    return response 

if __name__ == "__main__":
        result = asyncio.run(main())
