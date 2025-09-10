import argparse
import asyncio
from scenario_generation_agent import run_dynamic_scenario_generation
from expert_evaluation_agent import run_evaluation

def main():
    parser = argparse.ArgumentParser(description="Cognitive Flexibility CLI Assessment")
    parser.add_argument('--run', action='store_true', help='Start the cognitive flexibility assessment')
    args = parser.parse_args()

    if args.run:
        asyncio.run(assessment_flow())

async def assessment_flow():
    scenario, user_resp, followup_resp = await run_dynamic_scenario_generation()
    await run_evaluation(scenario.scenario, user_resp, followup_resp)

if __name__ == "__main__":
    main()
