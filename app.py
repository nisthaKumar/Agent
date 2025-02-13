from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel, load_tool, tool, LiteLLMModel
import datetime
import requests
import pytz
import yaml
import os
from tools.final_answer import FinalAnswerTool
from tools.visit_webpage import VisitWebpageTool
from tools.web_search import DuckDuckGoSearchTool

from Gradio_UI import GradioUI

# Below is an example of a tool that does nothing. Amaze us with your creativity !
@tool
def my_cutom_tool(arg1:str, arg2:int)-> str: #it's import to specify the return type
    #Keep this format for the description / args / args description but feel free to modify the tool
    """A tool that does nothing yet 
    Args:
        arg1: the first argument
        arg2: the second argument
    """
    return "What magic will you build ?"

@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


visit_webpage = VisitWebpageTool()
web_search = DuckDuckGoSearchTool()
final_answer = FinalAnswerTool()

# model = HfApiModel(
# max_tokens=2096,
# temperature=0.5,
# model_id='Qwen/Qwen2.5-Coder-32B-Instruct',# it is possible that this model may be overloaded
# custom_role_conversions=None,
# )

model = LiteLLMModel(
  model_id="gemini/gemini-2.0-flash-exp",
  max_tokens=2096,
  temperature=0.6,
  api_key=os.getenv("GEMINI_API_KEY")
)


# Import tool from Hub
#image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)
    
agent = CodeAgent(
    model=model,
    tools=[final_answer, visit_webpage, web_search], ## add your tools here (don't remove final answer)
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates
)


if __name__ == "__main__":
  try:
    GradioUI(agent, "documents").launch()
  except Exception as e:
    print(f"Error launching GradioUI: {str(e)}")