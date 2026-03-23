import os
import asyncio
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters

from dotenv import load_dotenv

load_dotenv()
MENSAGE_MAX_LENGTH = 2000

model = ChatOllama(model=os.getenv("OLLAMA_CHAT_MODEL"), temperature=0.0)
firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")


server_params = StdioServerParameters(
    command="npx",
    env={
        "FIRECRAWL_API_KEY": firecrawl_api_key,
    },
    args=["firecrawl-mcp"],
)


async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent = create_react_agent(model, tools)
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that can scrape websites, crawl pages and extract information use Firecrawl tools. You can use the following tools: "
                    + ", ".join([tool.name for tool in tools])
                    + ", Think step by step and use the tools when necessary to answer the user's question.",
                },
            ]
            print(
                "Available tools: " + ", ".join([tool.name for tool in tools])
            )
            while True:
                user_input = input("\nUser: ")
                if user_input.lower() in ["exit", "quit"]:
                    print("Exiting...")
                    break
                messages.append(
                    {"role": "user", "content": user_input[:MENSAGE_MAX_LENGTH]}
                )
                try:

                    response = await agent.ainvoke({"messages": messages})
                    ai_mensage = response["messages"][-1].content
                    print("\nAI: " + ai_mensage)
                    messages.append(
                        {"role": "assistant", "content": ai_mensage}
                    )
                except Exception as e:
                    print("Error: " + str(e))


if __name__ == "__main__":
    asyncio.run(main())
