from tools import get_jira_stories
from agent import Agent


agent = Agent()

response = agent.run("Obtener historia y crear test para ella")

print(response)