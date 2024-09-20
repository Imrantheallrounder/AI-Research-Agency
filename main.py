import streamlit as st

from crewai import Crew
from textwrap import dedent

from tools import Tools
from agents import Agents
from tasks import Tasks

import json

class AiResearchAgency:

    def run_research_agency(self, RESEARCH_TOPIC):
        tools = Tools()
        agents = Agents(RESEARCH_TOPIC)
        tasks = Tasks()

        chief_editor = agents.create_chief_editor()
        researcher = agents.create_researcher([tools.Research_tool])
        editor = agents.create_editor([tools.file_read_tool])
        reviewer = agents.create_reviewer()
        revisor = agents.create_revisor()
        writer = agents.create_writer()
        publisher = agents.create_publisher([tools.convertmarkdowntopdf])

        task_manage_project = tasks.create_task_manage_project(agent=chief_editor)
        task_conduct_research = tasks.create_task_conduct_research(RESEARCH_TOPIC=RESEARCH_TOPIC, agent=researcher, context_list=[task_manage_project])
        task_refine_data = tasks.create_task_refine_data(agent=editor, context_list=[task_conduct_research])
        task_review_data = tasks.create_task_review_data(agent=reviewer, context_list=[task_refine_data])
        task_review_draft = tasks.create_task_review_draft(agent=revisor, context_list=[task_review_data])
        task_write_report = tasks.create_task_write_report(agent=writer, context_list=[task_review_draft])
        task_publish_report = tasks.create_task_publish_report(agent=publisher, context_list=[task_write_report])

        crew = Crew(
        agents=[
            chief_editor,
            researcher,
            editor,
            reviewer,
            revisor,
            writer,
            publisher,
        ],
        tasks=[
            task_manage_project,
            task_conduct_research,
            task_refine_data,
            task_review_data,
            task_review_draft,
            task_write_report,
            task_publish_report,
        ],
        verbose=True,
        )
        output = crew.kickoff()

        def write_json_to_file(file_name, content):
            # Open the file in write mode
            with open(file_name, 'w') as file:
                # Dump the content to the file as JSON
                json.dump(content, file, indent=4)
                print("Saved intemediate responses in Json file: intermediate_responses.json")
        
        write_json_to_file("intermediate_responses.json", agents.response_dc)
        
        return output
        

    def report_generation(self):

        if st.session_state.generating:
            st.session_state.report = self.run_research_agency(
                st.session_state.RESEARCH_TOPIC
            )

        if st.session_state.report and st.session_state.report != "":
            with st.container():
                st.write("Research report generated successfully!")
                # st.download_button(
                #     label="Download Report file",
                #     data=st.session_state.report,
                #     file_name="final_report.pdf",
                #     mime="application/pdf",
                #     #mime="text/html",
                # )
            st.session_state.generating = False

    def sidebar(self):
        with st.sidebar:
            st.title("AI RESEARCH AGENCY")

            st.write(
                """
                To generate a research report, enter a topic. \n
                Your team of AI agents will generate a report for you!
                """
            )

            st.text_input("Topic", key="RESEARCH_TOPIC", placeholder="Enter a research topic")

            if st.button("Generate Report"):
                st.session_state.generating = True

    def render(self):
        st.set_page_config(page_title="AI Research Agency", page_icon="🤖")   # 📧

        if "topic" not in st.session_state:
            st.session_state.topic = ""

        if "report" not in st.session_state:
            st.session_state.report = ""

        if "generating" not in st.session_state:
            st.session_state.generating = False

        self.sidebar()

        self.report_generation()


if __name__ == "__main__":
    AiResearchAgency().render()