import os
from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools

load_dotenv()

agent = Agent(
    model=Groq(id="qwen/qwen3.8-27b"),
    markdown=True
)

agent.print_response("Apa itu baterai Lithium?", stream=True)
