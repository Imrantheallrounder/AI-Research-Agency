from langchain.tools import tool
from crewai_tools.tools import FileReadTool
import os, requests, re, mdpdf, subprocess
from tavily import TavilyClient

from dotenv import load_dotenv
load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


class Tools:

  def __init__(self):
    pass

  @tool
  def Research_tool(topic):
    """
    This tool is used for researching topic on internet

    Args:
        topic: This is the research topic.

    Returns:
        str: Research topic content collected from internet.
    """
    # TAVILY_API_KEY = "put your key"
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    response = tavily_client.search(topic, include_images=True)
    return str(response)


  @tool
  def convertmarkdowntopdf(markdownfile_name: str) -> str:
    """
    Converts a Markdown file to a PDF document using the mdpdf command line application.

    Args:
        markdownfile_name: Name of the input Markdown file.
    """
    output_file = os.path.splitext(markdownfile_name)[0] + '.pdf'

    # Command to convert markdown to PDF using mdpdf
    cmd = ['mdpdf', '--output', output_file, markdownfile_name]

    # Execute the command
    subprocess.run(cmd, check=True)

    return output_file

  @tool
  def file_read_tool(file_name: str):
    """
    A tool to read file.

    Args:
      file_path: Name of the file that needs to be acessed.
    """
    with open(file_name) as f:
      content = f.read()

    return content

  # Read file tool
  # file_read_tool = FileReadTool(
  #   file_path='research_data.txt',
  #   description='A tool to read the reaserch data file and understand the expected output format.'
  # )