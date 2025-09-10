from pydantic import BaseModel, Field
from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
import os
import asyncio
from rich.console import Console
from rich.markdown import Markdown

console = Console()
load_dotenv()

class Scenario(BaseModel):
    scenario: str = Field(..., description="Realistic work scenario prompt")
    followup: str = Field(..., description="Follow-up challenge or unexpected event")

def parse_scenario_from_text(text: str) -> Scenario:
    lines = text.splitlines()
    scenario = ""
    followup = ""
    current_section = None

    for line in lines:
        line_stripped = line.strip()
        lower_line = line_stripped.lower()

        if lower_line.startswith("scenario:"):
            current_section = "scenario"
            scenario = line_stripped[len("scenario:"):].strip()
        elif lower_line.startswith("follow-up:") or lower_line.startswith("followup:"):
            current_section = "followup"
            followup = line_stripped.split(":", 1)[1].strip()
        else:
            if current_section == "scenario" and line_stripped:
                scenario += " " + line_stripped
            elif current_section == "followup" and line_stripped:
                followup += " " + line_stripped

    if not scenario:
        scenario = "No scenario provided."
    if not followup:
        followup = "No follow-up provided."

    return Scenario(scenario=scenario.strip(), followup=followup.strip())

async def create_expert_agent():
    agent = Agent(
        model = Gemini(id="gemini-2.0-flash"),
        description=("You are an expert in project management assessments. "
                     "Generate realistic work scenarios that test cognitive flexibility, adaptability, "
                     "and creativity for software developers. Then generate a follow-up challenge or "
                     "unexpected event related to the scenario. Provide the output with headings "
                     "'Scenario:' and 'Follow-up:' clearly labeled."),
        markdown=True,
    )
    return agent

async def run_dynamic_scenario_generation():
    agent = await create_expert_agent()
    prompt = ("Generate a short, realistic work scenario and a brief follow-up question "
              "testing adaptability, creativity, and openness for a software developer. "
              "Output clearly labeled: 'Scenario:' and 'Follow-up:'.")
    console.print("[bold cyan]Requesting scenario generation from agent...[/bold cyan]")
    result = agent.run(prompt)
    console.print("[bold green]Raw AI-generated text:[/bold green]")
    console.print(Markdown(result.content))
    scenario = parse_scenario_from_text(result.content)
    console.print("\n[bold yellow]Parsed Scenario Model:[/bold yellow]")
    console.print(f"Scenario: {scenario.scenario}")
    console.print(f"Follow-up: {scenario.followup}")
    user_response = input("\nYour response to the scenario: ")
    followup_response = input("Your response to the follow-up: ")
    console.print("\n[bold magenta]Thank you for your responses![/bold magenta]")
    return scenario, user_response, followup_response
