from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
import os
import asyncio
from rich.console import Console
from rich.markdown import Markdown

console = Console()
load_dotenv()

async def create_flexibility_agent():
    agent = Agent(
        model = Gemini(id="gemini-2.0-flash"),
        description=("You are a project coach who evaluates cognitive flexibility. "
                     "Present work scenarios, ask for adaptation strategies, and prompt for follow-up decisions."),
        markdown=True,
    )
    return agent

async def run_evaluation(scenario_text: str, response1: str, response2: str):
    agent = await create_flexibility_agent()
    review_prompt = (
        f"Evaluate this response for adaptability, creativity, openness (1–5): '{response1}' "
        f"and follow-up '{response2}'. Give a brief feedback."
    )
    result = agent.run(review_prompt)
    print("\nAgent feedback and ratings:")
    console.print(Markdown(result.content))
    return result.content
