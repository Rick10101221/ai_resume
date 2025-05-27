from langchain_ollama import ChatOllama
from browser_use import Agent
import asyncio


async def main():
    #llm = ChatOllama(model="qwen3:30b", num_ctx=32000)
    #llm = ChatOllama(model="gemma3:27b", num_ctx=32000)
    llm = ChatOllama(model='qwen2.5:32b-instruct', num_ctx=32000)

    agent = Agent(
        task = "Open Google.com, wait for 5 seconds, and then close",
        llm = llm,
    )

    result = await agent.run()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())