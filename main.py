import streamlit as st
from crewai import Crew
from tools import Tools
from agents import Agents
from tasks import Tasks
import json
import uuid

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
        
        agents.response_dc["Topic_Id"] = str(uuid.uuid4())
        write_json_to_file("intermediate_responses.json", agents.response_dc)
        tools.log_data_in_db("Logs", agents.response_dc)

        # add Topic_Id
        
        return output

    def report_generation(self):
        if st.session_state.generating:
            with st.spinner("🔍 Our AI team is hard at work generating your research report..."):
                st.session_state.report = self.run_research_agency(
                    st.session_state.RESEARCH_TOPIC
                )

        if st.session_state.report and st.session_state.report != "":
            st.balloons()
            st.success("🎉 Research report generated successfully!")
            
            with st.container():
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.subheader("📊 Your Research Report is Ready!")
                    st.markdown(
                        """
                        <div style='background-color: #e6f3ff; padding: 20px; border-radius: 10px;'>
                            <h4>What's Inside:</h4>
                            <ul>
                                <li>Comprehensive analysis of your topic</li>
                                <li>Latest research findings and trends</li>
                                <li>Expert insights and recommendations</li>
                                <li>Visual data representations</li>
                            </ul>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                with col2:
                    st.markdown(
                        """
                        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;'>
                            <h4>Download Your Report</h4>
                            <p>Get your comprehensive PDF report now!</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    pdf_file_path = "final_report.pdf"
                    with open(pdf_file_path, "rb") as pdf_file:
                        pdf_data = pdf_file.read()
                    
                    generated_file_name = str(st.session_state.RESEARCH_TOPIC)

                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_data,
                        file_name=f"{generated_file_name}.pdf",
                        mime="application/pdf",
                        key="download_report",
                    )
            
            st.session_state.generating = False

    def sidebar(self):
        with st.sidebar:
            st.title("📡 AI RESEARCH AGENCY")

            st.markdown(
                """
                <div style='text-align: center; padding: 10px; background-color: #f0f2f6; border-radius: 10px;'>
                    <h3>Generate Your Research Report</h3>
                    <p>Enter a topic below and let our AI team create a comprehensive report for you!</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.text_input("Research Topic", key="RESEARCH_TOPIC", placeholder="E.g., Artificial Intelligence in Healthcare")

            if st.button("⚙️ Generate Report", type="primary"):  #🚀 
                st.session_state.generating = True

    def render(self):
        st.set_page_config(page_title="AI Research Agency", page_icon="📡", layout="wide")

        if "topic" not in st.session_state:
            st.session_state.topic = ""

        if "report" not in st.session_state:
            st.session_state.report = ""

        if "generating" not in st.session_state:
            st.session_state.generating = False

        self.sidebar()

        st.title("📡 Welcome to AI Research Agency")
        st.markdown(
            """
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
                <h3>Unlock the Power of AI-Driven Research</h3>
                <p>Generate comprehensive research reports on any topic with the combined expertise of our AI agents. 
                From literature reviews to trend analysis, we've got you covered!</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### 🚀 Fast")
            st.write("Generate reports in minutes, not days.")
        with col2:
            st.markdown("### 🧠 Intelligent")
            st.write("Powered by cutting-edge AI technology.")
        with col3:
            st.markdown("### 📊 Comprehensive")
            st.write("Get in-depth analysis and insights.")

        st.markdown("---")

        self.report_generation()


if __name__ == "__main__":
    AiResearchAgency().render()