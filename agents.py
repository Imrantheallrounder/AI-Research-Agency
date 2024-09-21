from crewai import Agent
from langchain_openai import ChatOpenAI
import os
import csv

import streamlit as st
import json
from typing import Union, List, Tuple, Dict
from langchain_core.agents import AgentFinish

from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class Agents:

  def __init__(self, RESEARCH_TOPIC, GROQ_API_KEY=GROQ_API_KEY):

    self.RESEARCH_TOPIC = RESEARCH_TOPIC
    self.response_dc = {"Research_Topic": RESEARCH_TOPIC}

    os.environ["GROQ_API_KEY"] = GROQ_API_KEY
    self.llm_llama_8b = ChatOpenAI(
      openai_api_base="https://api.groq.com/openai/v1",
      openai_api_key=os.getenv("GROQ_API_KEY"),
      model_name="llama3-8b-8192"
    )
    self.llm_llama_70b = ChatOpenAI(
      openai_api_base="https://api.groq.com/openai/v1",
      openai_api_key=os.getenv("GROQ_API_KEY"),
      model_name="llama3-70b-8192"
    )

    # File path for logging
    # self.log_file = 'agent_log.csv'

    # Create the CSV if it does not exist
    # if not os.path.exists(self.log_file):
    #   with open(self.log_file, mode='w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(['agent_name', 'action', 'observation'])  # Headers

  def step_callback(
    self,
    agent_output: Union[str, List[Tuple[Dict, str]], AgentFinish],
    agent_name,
    *args,
  ):
    with st.chat_message("AI"):
      # Try to parse the output if it is a JSON string
      if isinstance(agent_output, str):
        try:
          agent_output = json.loads(agent_output)
        except json.JSONDecodeError:
          pass

      action_dc = {}
      if isinstance(agent_output, list) and all(
        isinstance(item, tuple) for item in agent_output
      ):
        
        for action, description in agent_output:
          # Print attributes based on assumed structure
          st.write(f"Agent Name: {agent_name}")
          st.write(f"Tool used: {getattr(action, 'tool', 'Unknown')}")
          st.write(f"Tool input: {getattr(action, 'tool_input', 'Unknown')}")
          st.write(f"{getattr(action, 'log', 'Unknown')}")
          with st.expander("Show observation"):
            st.markdown(f"Observation\n\n{description}")
          
          if getattr(action, 'log', 'Unknown') != '':
            action_dc['action'] = getattr(action, 'log', 'Unknown')
          # Log to CSV
          # with open(self.log_file, mode='a', newline='') as file:
          #   writer = csv.writer(file)
          #   writer.writerow([agent_name, getattr(action, 'tool', 'Unknown'), description])

      elif isinstance(agent_output, AgentFinish):
        st.write(f"Agent Name: {agent_name}")
        output = agent_output.return_values
        st.write(f"I finished my task:\n{output['output']}")
        
        if output!= "":
          self.response_dc[f"{agent_name}_Output"] = output["output"]
          print("###########################################################")
          print(output["output"])
          if action_dc!={}:
            self.response_dc[f"{agent_name}_Output"]['Action'] = action_dc['action']

        # # Log to CSV
        # with open(self.log_file, mode='a', newline='') as file:
        #   writer = csv.writer(file)
        #   writer.writerow([agent_name, 'Task Finished', output['output']])

      else:
        st.write(type(agent_output))
        st.write(agent_output)



  def create_chief_editor(self, tools_list=[]):
    return Agent(
      role='Chief Editor',
      goal='Manage the entire research process, ensuring clarity, focus, quality, and accuracy of the final report. You are the leader who keeps the project on track.',
      backstory="You are the Chief Editor. You oversee the research process, coordinate the team, and ensure that all findings are accurate, cohesive, and well-presented.",
      verbose=True,
      llm=self.llm_llama_70b,
      tools=tools_list,
      allow_delegation=False,
      step_callback=lambda step: self.step_callback(step, "Chief_Editor"),
      )

  def create_researcher(self, tools_list=[]):
    return Agent(
      role='Researcher',
      goal="Conduct thorough research by delving into vast knowledge sources and real-time data from the Internet, gathering and analyzing relevant information. Don't iterate unnecessarily and finish your task. Don't return None.",
      backstory="You are the Researcher. You dive deep into various data sources, both static and dynamic, to collect all necessary information for the report. You are the foundation of the research team's work.",
      verbose=True,
      llm=self.llm_llama_70b,
      tools=tools_list,  # [Research_tool]
      allow_delegation=False,
      step_callback=lambda step: self.step_callback(step, "Researcher"),
      )

  def create_editor(self, tools_list=[]):
    return Agent(
      role='Editor',
      goal="Refine and validate the synthesized insights, ensuring that the information is accurate, cohesive, and logically structured. Synthesized insights are stored in 'research_data.txt' file.",
      backstory="You are the Editor. Your job is to collaborate with the Researcher and Reviewer to refine the gathered data, ensuring that the information is well-organized and insightful.",
      verbose=True,
      llm=self.llm_llama_8b,
      tools=tools_list,  # [file_read_tool]
      allow_delegation=False,
      step_callback=lambda step: self.step_callback(step, "Editor"),
      )

  def create_reviewer(self, tools_list=[]):
    return Agent(
      role='Reviewer',
      goal="Critically evaluate the refined content for accuracy, depth, and relevance, ensuring that the research meets high standards.",
      backstory="You are the Reviewer. Your role is to critically assess the content refined by the Editor, checking for accuracy, relevance, and depth of analysis. You ensure the research is up to standard.",
      verbose=True,
      llm=self.llm_llama_8b,
      tools=tools_list,  # Replace with actual tool names
      allow_delegation=False,
      step_callback=lambda step: self.step_callback(step, "Reviewer"),
      )

  def create_revisor(self, tools_list=[]):
    return Agent(
      role='Revisor',
      goal="Review and enhance the readability of the draft, ensuring strict adherence to formatting, citation standards, and overall presentation.",
      backstory="You are the Revisor. You ensure that the final draft is not only accurate but also clear and professionally formatted. You check for citation accuracy and overall readability.",
      verbose=True,
      llm=self.llm_llama_8b,
      tools=tools_list,    # ["grammar_check_tool", "citation_management_tool"],  # Replace with actual tool names
      allow_delegation=False,
      step_callback=lambda step: self.step_callback(step, "Revisor"),
      )

  def create_writer(self, tools_list=[]):
    return Agent(
      role='Writer',
      goal="Craft a polished and coherent report based on the refined content, ensuring it is well-structured and communicates the research findings effectively.",
      backstory="You are the Writer. Your task is to take the refined content and craft it into a polished, well-structured report that effectively communicates the research findings. And make sure that you write a valid and correct Markdown file.",
      verbose=True,
      llm=self.llm_llama_70b,
      tools=tools_list,  # Replace with actual tool names
      allow_delegation=False,
      step_callback=lambda step: self.step_callback(step, "Writer"),
      )

  def create_publisher(self, tools_list=[]):
    return Agent(
      role='Publisher',
      goal="Prepare the final report in various formats. Convert the Markdown file to a PDF document. 'final_report.md' is the markdown file name.",
      backstory="You are the Publisher. Your role is to finalize the report, ensuring it is well-presented and ready for dissemination. You optimize the report for accessibility.",  # across different formats
      verbose=True,
      llm=self.llm_llama_8b,
      tools=tools_list,  # [convertmarkdowntopdf]
      allow_delegation=False,
      step_callback=lambda step: self.step_callback(step, "Publisher"),
      )