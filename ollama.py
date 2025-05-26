from langchain_ollama import ChatOllama
from browser_use import Agent
import asyncio


async def main():
    #llm = ChatOllama(model="qwen3:30b", num_ctx=32000)
    #llm = ChatOllama(model="gemma3:27b", num_ctx=32000)
    llm = ChatOllama(model='qwen2.5:32b-instruct', num_ctx=32000)

    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3",
        llm=llm,
    )

    result = await agent.run()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())