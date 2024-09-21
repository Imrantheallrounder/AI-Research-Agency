import sqlite3
import uuid

class SqlDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("SQLiteDatabase.db")

    def create_table(self, table_name, schema):
        """
        Creates a new table in the SQLite database based on the provided schema.

        Args:
            table_name (str): The name of the table to be created.
            schema (str): The schema definition of the table, including column names and data types.

        Example:
            schema = "id INTEGER PRIMARY KEY, name TEXT, age INTEGER"
            create_table("users", schema)
            # This will create a table named "users" with columns: id, name, and age.

        Note:
            - Ensure that the database connection (`self.conn`) is established before calling this method.
            - The method assumes that the schema string provided is correctly formatted as SQL.
        """
        try:
            self.conn.execute(
                f'''
                    Create table {table_name} (
                        {schema}
                    )
                '''
                )
            print(f"Executed Successfully! and created {table_name} table.")
        except Exception as e:
            print(f"Exception occured: {e}")

    def insert_data(self, table_name, data_dict):
        """
        Inserts data into a specified table in the database.

        Args:
            table_name (str): The name of the table where the data will be inserted.
            data_dict (dict): A dictionary containing column names as keys and the corresponding data as values.

        Example:
            data_dict = {"name": "John", "age": 30}
            insert_data("users", data_dict)
            # This will insert a new record into the "users" table with "name" as "John" and "age" as 30.

        Note:
            The method assumes that the database connection is already established (through `self.conn`) and `self.conn.commit()` is called after insertion.
        """
        try:
            self.conn.execute(
                f'''insert into {table_name} {tuple(data_dict.keys())} VALUES {tuple(data_dict.values())}'''
            )

            self.conn.commit()
            print(f"Insertion succesful! in {table_name}")
        except Exception as e:
            print(f"Error in Insertion: {e}")

    def delete(self, table_name, condition):
        """
        Deletes rows from a specified table based on a given condition.

        Args:
            table_name (str): The name of the table from which rows will be deleted.
            condition (str): The SQL condition to specify which rows to delete.
                            Example: 'Name="Chief Editor"' or 'id=5'

        Returns:
            int: The number of rows deleted from the table.

        Raises:
            Exception: If there is an error during the deletion process, the exception is caught and an error message is printed.

        Example:
            delete("employees", 'Name="John"')
            # Deletes rows where the Name is "John" in the "employees" table.
        """
        try:
            # Execute the deletion with a parameterized query
            query = f"DELETE FROM {table_name} WHERE {condition}"
            cursor = self.conn.execute(query)

            # Commit the changes to the database
            self.conn.commit()

            # Get the number of rows affected by the query
            rows_deleted = cursor.rowcount

            print(f"Deletion successful! {rows_deleted} row(s) deleted from {table_name}.")
            return rows_deleted

        except Exception as e:
            print(f"Error during deletion: {e}")
            return 0



if __name__=='__main__':

    obj = SqlDatabase()

    # obj.delete("Users", 'Username="john"')

    # ************************************** Users Table creation **************************************
    table = "Users"
    user_attributes = '''
        User_Id INT AUTO_INCREMENT PRIMARY KEY,
        Username VARCHAR(50) NOT NULL,
        Password VARCHAR(255) NOT NULL,  
        Email VARCHAR(50) NOT NULL UNIQUE,
        Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    '''
    # obj.create_table(table_name=table, schema=user_attributes)

    u_id = str(uuid.uuid4())
    user_dc = {
        'User_Id': u_id,
        'Username': 'Arzoo',          # kevin, John, 
        'Password': 'arzoo#123',         #kevindevin, johnthedon
        'email': 'arzoo.cs@gmail.com'
    }
    obj.insert_data(table, user_dc)


    # ************************************** Agents Table creation **************************************
    table = "Agents"
    agent_table_attributes = '''
            Name VARCHAR(50) PRIMARY KEY,
            Role  VARCHAR(150),
            Goal VARCHAR(1024),
            LLM VARCHAR(30),
            Tool VARCHAR(100)
            '''
    # obj.create_table(table_name=table, attributes=agent_table_attributes)

    # agent_dc1 = {
    #     'Name': '''Chief Editor''',
    #     'Role': '''You are the Chief Editor. You oversee the research process, coordinate the team, and ensure that all findings are accurate, cohesive, and well-presented.''',
    #     'Goal': '''Manage the entire research process, ensuring clarity, focus, quality, and accuracy of the final report. You are the leader who keeps the project on track.''',
    #     'LLM': '''llama3-70b-8192''', # llama3-8b-8192, llama3-70b-8192
    #     'Tool': ''
    # }
    # agent_dc2 = {
    #     'Name': '''Researcher''',
    #     'Role': '''You are the Researcher. You dive deep into various data sources, both static and dynamic, to collect all necessary information for the report. You are the foundation of the research team's work.''',
    #     'Goal': '''Conduct thorough research by delving into vast knowledge sources and real-time data from the Internet, gathering and analyzing relevant information. Don't iterate unnecessarily and finish your task. Don't return None.''',
    #     'LLM': '''llama3-70b-8192''', # llama3-8b-8192, llama3-70b-8192
    #     'Tool': 'Research_tool'
    # }
    # agent_dc3 = {
    #     'Name': '''Editor''',
    #     'Role': '''You are the Editor. Your job is to collaborate with the Researcher and Reviewer to refine the gathered data, ensuring that the information is well-organized and insightful.''',
    #     'Goal': '''Refine and validate the synthesized insights, ensuring that the information is accurate, cohesive, and logically structured. Synthesized insights are stored in 'research_data.txt' file.''',
    #     'LLM': '''llama3-8b-8192''', # llama3-8b-8192, llama3-70b-8192
    #     'Tool': 'Research_tool'
    # }
    # agent_dc4 = {
    #     'Name': '''Reviewer''',
    #     'Role': '''You are the Reviewer. Your role is to critically assess the content refined by the Editor, checking for accuracy, relevance, and depth of analysis. You ensure the research is up to standard.''',
    #     'Goal': '''Critically evaluate the refined content for accuracy, depth, and relevance, ensuring that the research meets high standards.''',
    #     'LLM': '''llama3-8b-8192''', # llama3-8b-8192, llama3-70b-8192
    #     'Tool': ''
    # }
    # agent_dc5 = {
    #     'Name': '''Revisor''',
    #     'Role': '''You are the Revisor. You ensure that the final draft is not only accurate but also clear and professionally formatted. You check for citation accuracy and overall readability.''',
    #     'Goal': '''Review and enhance the readability of the draft, ensuring strict adherence to formatting, citation standards, and overall presentation.''',
    #     'LLM': '''llama3-8b-8192''', # llama3-8b-8192, llama3-70b-8192
    #     'Tool': ''
    # }
    # agent_dc6 = {
    #     'Name': '''Writer''',
    #     'Role': '''You are the Writer. Your task is to take the refined content and craft it into a polished, well-structured report that effectively communicates the research findings. And make sure that you write a valid and correct Markdown file.''',
    #     'Goal': '''Craft a polished and coherent report based on the refined content, ensuring it is well-structured and communicates the research findings effectively.''',
    #     'LLM': '''llama3-70b-8192''', # llama3-8b-8192, llama3-70b-8192
    #     'Tool': ''
    # }
    # agent_dc = {
    #     'Name': '''Publisher''',
    #     'Role': '''You are the Publisher. Your role is to finalize the report, ensuring it is well-presented and ready for dissemination. You optimize the report for accessibility.''',
    #     'Goal': '''Prepare the final report in various formats. Convert the Markdown file to a PDF document. 'final_report.md' is the markdown file name.''',
    #     'LLM': '''llama3-8b-8192''', # llama3-8b-8192, llama3-70b-8192
    #     'Tool': 'convertmarkdowntopdf'
    # }
    # obj.insert_data(table_name=table, data_dict=agent_dc)

    # ************************************** LOGs Table creation **************************************
    table = "Logs"
    logs_table_attributes = '''
            Topic_Id VARCHAR(64) PRIMARY KEY,
            Research_Topic VARCHAR(200),
            Chief_Editor_Output  VARCHAR(8000),
            Researcher_Output VARCHAR(8000),
            Editor_Output VARCHAR(8000),
            Reviewer_Output VARCHAR(8000),
            Revisor_Output VARCHAR(8000),
            Writer_Output VARCHAR(8000),
            Publisher_Output VARCHAR(8000)
            '''
    # obj.create_table(table_name=table, attributes=logs_table_attributes)

    #Insert data
    table_name = "Logs"
    data_dict = {
    "Topic_Id": "2538dfa5-332b-4010-bfb4-476f4f247a12",

    "Research_Topic": "1. AI in Healthcare",

    "Chief_Editor_Output": "**Final Report: Research Project Overview**\n\n**Executive Summary**\n\nThis comprehensive report presents the findings of a rigorous research project conducted by our team of experts. The study aimed to investigate [research topic] and provide actionable insights for [target audience]. Our research methodology combined [methods used] to gather data from [data sources]. The results indicate [key findings] and highlight [implications for the field].\n\n**Introduction**\n\n[Background information on the research topic, including context, relevance, and significance]\n\n**Literature Review**\n\n[A critical analysis of existing research on the topic, including key theories, concepts, and debates]\n\n**Methodology**\n\n[A detailed description of the research design, including data collection methods, sample selection, and data analysis procedures]\n\n**Results**\n\n[A clear and concise presentation of the research findings, including any visual aids such as tables, figures, and graphs]\n\n**Discussion**\n\n[An in-depth analysis of the results, including implications for the field, limitations of the study, and avenues for future research]\n\n**Conclusion**\n\n[A summary of the key findings and their significance, including recommendations for [target audience]\n\n**Recommendations**\n\n[Actionable suggestions for [target audience] based on the research findings]\n\n**Limitations**\n\n[A discussion of the study's limitations and potential avenues for future research]\n\n**Appendices**\n\n[Additional materials that support the research, including raw data, extra figures and tables, and detailed descriptions of methodologies]\n\n**References**\n\n[A comprehensive list of sources cited in the report, formatted according to the chosen citation style]\n\nI am confident that this final report meets the quality standards and is ready for publication.",
    
    "Researcher_Output": "**Final Report: Research Project Overview**\n\n**Executive Summary**\n\nThis comprehensive report presents the findings of a rigorous research project conducted by our team of experts. The study aimed to investigate AI in Healthcare and provide actionable insights for healthcare professionals. Our research methodology combined online research to gather data from various sources. The results indicate that AI has the potential to transform healthcare by improving efficiency, user experience, diagnosis, health monitoring, and data connection. The report highlights the benefits of AI in healthcare, including improved patient care, reduced costs, and enhanced population health.\n\n**Introduction**\n\nArtificial intelligence (AI) is transforming various industries, and healthcare is no exception. AI has the potential to revolutionize healthcare by improving patient outcomes, reducing costs, and enhancing the overall quality of care. This report provides an overview of the current state of AI in healthcare, its benefits, and its potential applications.\n\n**Literature Review**\n\nAI in healthcare is a rapidly growing field, with numerous research studies and applications emerging in recent years. According to a report by McKinsey, AI has the potential to transform healthcare by improving efficiency, reducing costs, and enhancing patient care. AI can be used in various applications, including health analytics, diagnosis, and treatment.\n\n**Methodology**\n\nThis report is based on online research, using various sources including academic journals, research studies, and industry reports. The research methodology combined online research to gather data from various sources.\n\n**Results**\n\nThe results of the research indicate that AI has the potential to transform healthcare by improving efficiency, user experience, diagnosis, health monitoring, and data connection. AI can be used in various applications, including health analytics, diagnosis, and treatment.\n\n**Discussion**\n\nThe use of AI in healthcare has numerous benefits, including improved patient care, reduced costs, and enhanced population health. However, there are also challenges and limitations to the adoption of AI in healthcare, including regulatory issues, data privacy concerns, and the need for further research.\n\n**Conclusion**\n\nIn conclusion, AI has the potential to transform healthcare by improving patient outcomes, reducing costs, and enhancing the overall quality of care. The report highlights the benefits of AI in healthcare, including improved patient care, reduced costs, and enhanced population health.\n\n**Recommendations**\n\nBased on the findings of this report, we recommend that healthcare professionals and organizations consider the adoption of AI in healthcare. However, further research is needed to address the challenges and limitations of AI in healthcare.\n\n**Limitations**\n\nThe limitations of this report include the reliance on online research and the need for further research to address the challenges and limitations of AI in healthcare.\n\n**Appendices**\n\nThis report includes an appendix that provides additional information on the sources used in the research.\n\n**References**\n\nThe references cited in this report include academic journals, research studies, and industry reports.\n\nI am confident that this final report meets the quality standards and is ready for publication.",
    
    "Editor_Output": "**Final Report: Research Project Overview**\n\n**Executive Summary**\n\nThis comprehensive report presents the findings of a rigorous research project conducted by our team of experts. The study aimed to investigate AI in Healthcare and provide actionable insights for healthcare professionals. Our research methodology combined online research to gather data from various sources. The results indicate that AI has the potential to transform healthcare by improving efficiency, user experience, diagnosis, health monitoring, and data connection. The report highlights the benefits of AI in healthcare, including improved patient care, reduced costs, and enhanced population health.\n\n**Introduction**\n\nArtificial intelligence (AI) is transforming various industries, and healthcare is no exception. AI has the potential to revolutionize healthcare by improving patient outcomes, reducing costs, and enhancing the overall quality of care. This report provides an overview of the current state of AI in healthcare, its benefits, and its potential applications.\n\n**Literature Review**\n\nAI in healthcare is a rapidly growing field, with numerous research studies and applications emerging in recent years. According to a report by McKinsey, AI has the potential to transform healthcare by improving efficiency, reducing costs, and enhancing patient care. AI can be used in various applications, including health analytics, diagnosis, and treatment.\n\n**Methodology**\n\nThis report is based on online research, using various sources including academic journals, research studies, and industry reports. The research methodology combined online research to gather data from various sources.\n\n**Results**\n\nThe results of the research indicate that AI has the potential to transform healthcare by improving efficiency, user experience, diagnosis, health monitoring, and data connection. AI can be used in various applications, including health analytics, diagnosis, and treatment.\n\n**Discussion**\n\nThe use of AI in healthcare has numerous benefits, including improved patient care, reduced costs, and enhanced population health. However, there are also challenges and limitations to the adoption of AI in healthcare, including regulatory issues, data privacy concerns, and the need for further research.\n\n**Conclusion**\n\nIn conclusion, AI has the potential to transform healthcare by improving patient outcomes, reducing costs, and enhancing the overall quality of care. The report highlights the benefits of AI in healthcare, including improved patient care, reduced costs, and enhanced population health.\n\n**Recommendations**\n\nBased on the findings of this report, we recommend that healthcare professionals and organizations consider the adoption of AI in healthcare. However, further research is needed to address the challenges and limitations of AI in healthcare.\n\n**Limitations**\n\nThe limitations of this report include the reliance on online research and the need for further research to address the challenges and limitations of AI in healthcare.\n\n**Appendices**\n\nThis report includes an appendix that provides additional information on the sources used in the research.\n\n**References**\n\nThe references cited in this report include academic journals, research studies, and industry reports.\n\nI am confident that this final report meets the quality standards and is ready for publication.",

    "Reviewer_Output": "**Feedback and Approved Refined Data**\n\nThe refined research data meets high research standards, with accurate and relevant information presented in a clear and concise manner. The report provides a comprehensive overview of AI in healthcare, highlighting its benefits, applications, and challenges.\n\n**Accuracy:**\n\nThe report accurately presents the current state of AI in healthcare, citing credible sources such as McKinsey and academic journals. The methodology is clearly described, and the results are presented in a logical and easy-to-follow manner.\n\n**Depth:**\n\nThe report provides a thorough analysis of AI in healthcare, covering its benefits, applications, and challenges. The discussion section is well-organized, addressing both the advantages and limitations of AI in healthcare.\n\n**Relevance:**\n\nThe report is highly relevant to the research topic, providing actionable insights for healthcare professionals and organizations. The recommendations section is clear and concise, outlining the next steps for the adoption of AI in healthcare.\n\n**Refined Data:**\n\nThe report includes an appendix with additional information on the sources used in the research, ensuring transparency and credibility. The references cited are credible and relevant, providing a solid foundation for the research.\n\nBased on the above assessment, I approve the refined research data for publication. The report meets high research standards, providing accurate, relevant, and in-depth information on AI in healthcare.",

    "Revisor_Output": "Feedback and Approved Refined Data\n\nThe refined research data meets high research standards, with accurate and relevant information presented in a clear and concise manner. The report provides a comprehensive overview of AI in healthcare, highlighting its benefits, applications, and challenges.\n\n**Accuracy:**\n\nThe report accurately presents the current state of AI in healthcare, citing credible sources such as McKinsey and academic journals. The methodology is clearly described, and the results are presented in a logical and easy-to-follow manner.\n\n**Depth:**\n\nThe report provides a thorough analysis of AI in healthcare, covering its benefits, applications, and challenges. The discussion section is well-organized, addressing both the advantages and limitations of AI in healthcare.\n\n**Relevance:**\n\nThe report is highly relevant to the research topic, providing actionable insights for healthcare professionals and organizations. The recommendations section is clear and concise, outlining the next steps for the adoption of AI in healthcare.\n\n**Refined Data:**\n\nThe report includes an appendix with additional information on the sources used in the research, ensuring transparency and credibility. The references cited are credible and relevant, providing a solid foundation for the research.\n\nAppendix:\n\nSources:\n\n* McKinsey & Company. (2020). AI in Healthcare: A Review of the Current State of the Art.\n* Journal of Healthcare Engineering. (2020). Artificial Intelligence in Healthcare: A Systematic Review.\n* World Health Organization. (2020). Artificial Intelligence in Healthcare: A Framework for Action.\n\nReferences:\n\n* McKinsey & Company. (2020). AI in Healthcare: A Review of the Current State of the Art.\n* Journal of Healthcare Engineering. (2020). Artificial Intelligence in Healthcare: A Systematic Review.\n* World Health Organization. (2020). Artificial Intelligence in Healthcare: A Framework for Action.\n\nI hope this meets the expect criteria and satisfies the requirements.",
    
    "Writer_Output": "**AI in Healthcare: A Comprehensive Review**\n============================================\n\n**Executive Summary**\n-------------------\n\nThis report provides a comprehensive overview of the current state of Artificial Intelligence (AI) in healthcare, highlighting its benefits, applications, and challenges. The report is based on credible sources, including McKinsey and academic journals, and provides actionable insights for healthcare professionals and organizations.\n\n**Introduction**\n---------------\n\nArtificial Intelligence (AI) has transformed various industries, and healthcare is no exception. AI has the potential to revolutionize healthcare by improving diagnosis, streamlining clinical workflows, and enhancing patient outcomes. This report provides a thorough analysis of AI in healthcare, covering its benefits, applications, and challenges.\n\n**Benefits of AI in Healthcare**\n-----------------------------\n\nAI has several benefits in healthcare, including:\n\n* **Improved Diagnosis**: AI-powered algorithms can analyze medical images and diagnose diseases more accurately and quickly than human clinicians.\n* **Enhanced Patient Outcomes**: AI can help personalize treatment plans, reducing the risk of adverse reactions and improving patient outcomes.\n* **Streamlined Clinical Workflows**: AI can automate routine tasks, freeing up clinicians to focus on high-value tasks.\n\n**Applications of AI in Healthcare**\n---------------------------------\n\nAI has numerous applications in healthcare, including:\n\n* **Medical Imaging**: AI-powered algorithms can analyze medical images, such as X-rays and MRIs, to diagnose diseases.\n* **Clinical Decision Support Systems**: AI can provide clinicians with real-time decision support, improving diagnosis and treatment.\n* **Patient Engagement**: AI-powered chatbots can engage patients in their care, improving patient outcomes and reducing costs.\n\n**Challenges of AI in Healthcare**\n---------------------------------\n\nDespite its benefits and applications, AI in healthcare faces several challenges, including:\n\n* **Data Quality**: AI algorithms require high-quality data to produce accurate results, which can be a challenge in healthcare.\n* **Regulatory Frameworks**: The regulatory framework for AI in healthcare is still evolving, creating uncertainty for healthcare organizations.\n* **Ethical Concerns**: AI raises ethical concerns, such as bias and transparency, which must be addressed.\n\n**Discussion**\n--------------\n\nThe report highlights the importance of addressing the challenges of AI in healthcare. Healthcare organizations must invest in high-quality data infrastructure and develop robust regulatory frameworks to ensure the safe and effective adoption of AI.\n\n**Recommendations**\n-----------------\n\nBased on the report's findings, we recommend that healthcare organizations:\n\n* **Invest in Data Infrastructure**: Develop robust data infrastructure to support AI adoption.\n* **Develop Regulatory Frameworks**: Establish clear regulatory frameworks for AI in healthcare.\n* **Address Ethical Concerns**: Address ethical concerns, such as bias and transparency, to ensure the safe and effective adoption of AI.\n\n**Appendix**\n-------------\n\n### Sources\n\n* McKinsey & Company. (2020). AI in Healthcare: A Review of the Current State of the Art.\n* Journal of Healthcare Engineering. (2020). Artificial Intelligence in Healthcare: A Systematic Review.\n* World Health Organization. (2020). Artificial Intelligence in Healthcare: A Framework for Action.\n\n### References\n\n* McKinsey & Company. (2020). AI in Healthcare: A Review of the Current State of the Art.\n* Journal of Healthcare Engineering. (2020). Artificial Intelligence in Healthcare: A Systematic Review.\n* World Health Organization. (2020). Artificial Intelligence in Healthcare: A Framework for Action.\n\nThis report provides a comprehensive overview of AI in healthcare, highlighting its benefits, applications, and challenges. The report is based on credible sources and provides actionable insights for healthcare professionals and organizations.",

    "Publisher_Output": "```\n**AI in Healthcare: A Comprehensive Review**\n============================================\n\n**Executive Summary**\n-------------------\n\nThis report provides a comprehensive overview of the current state of Artificial Intelligence (AI) in healthcare, highlighting its benefits, applications, and challenges. The report is based on credible sources, including McKinsey and academic journals, and provides actionable insights for healthcare professionals and organizations.\n\n**Introduction**\n---------------\n\nArtificial Intelligence (AI) has transformed various industries, and healthcare is no exception. AI has the potential to revolutionize healthcare by improving diagnosis, streamlining clinical workflows, and enhancing patient outcomes. This report provides a thorough analysis of AI in healthcare, covering its benefits, applications, and challenges.\n\n**Benefits of AI in Healthcare**\n-----------------------------\n\nAI has several benefits in healthcare, including:\n\n* **Improved Diagnosis**: AI-powered algorithms can analyze medical images and diagnose diseases more accurately and quickly than human clinicians.\n* **Enhanced Patient Outcomes**: AI can help personalize treatment plans, reducing the risk of adverse reactions and improving patient outcomes.\n* **Streamlined Clinical Workflows**: AI can automate routine tasks, freeing up clinicians to focus on high-value tasks.\n\n**Applications of AI in Healthcare**\n---------------------------------\n\nAI has numerous applications in healthcare, including:\n\n* **Medical Imaging**: AI-powered algorithms can analyze medical images, such as X-rays and MRIs, to diagnose diseases.\n* **Clinical Decision Support Systems**: AI can provide clinicians with real-time decision support, improving diagnosis and treatment.\n* **Patient Engagement**: AI-powered chatbots can engage patients in their care, improving patient outcomes and reducing costs.\n\n**Challenges of AI in Healthcare**\n---------------------------------\n\nDespite its benefits and applications, AI in healthcare faces several challenges, including:\n\n* **Data Quality**: AI algorithms require high-quality data to produce accurate results, which can be a challenge in healthcare.\n* **Regulatory Frameworks**: The regulatory framework for AI in healthcare is still evolving, creating uncertainty for healthcare organizations.\n* **Ethical Concerns**: AI raises ethical concerns, such as bias and transparency, which must be addressed.\n\n**Discussion**\n--------------\n\nThe report highlights the importance of addressing the challenges of AI in healthcare. Healthcare organizations must invest in high-quality data infrastructure and develop robust regulatory frameworks to ensure the safe and effective adoption of AI.\n\n**Recommendations**\n-----------------\n\nBased on the report's findings, we recommend that healthcare organizations:\n\n* **Invest in Data Infrastructure**: Develop robust data infrastructure to support AI adoption.\n* **Develop Regulatory Frameworks**: Establish clear regulatory frameworks for AI in healthcare.\n* **Address Ethical Concerns**: Address ethical concerns, such as bias and transparency, to ensure the safe and effective adoption of AI.\n\n**Appendix**\n-------------\n\n### Sources\n\n* McKinsey & Company. (2020). AI in Healthcare: A Review of the Current State of the Art.\n* Journal of Healthcare Engineering. (2020). Artificial Intelligence in Healthcare: A Systematic Review.\n* World Health Organization. (2020). Artificial Intelligence in Healthcare: A Framework for Action.\n\n### References\n\n* McKinsey & Company. (2020). AI in Healthcare: A Review of the Current State of the Art.\n* Journal of Healthcare Engineering. (2020). Artificial Intelligence in Healthcare: A Systematic Review.\n* World Health Organization. (2020). Artificial Intelligence in Healthcare: A Framework for Action.\n```\nHere is the final report in PDF format:\n\n[final_report.pdf](https://raw.githubusercontent.com/Publisher/final_report/main/final_report.pdf)",
    }
    # obj.insert_data(table_name, data_dict)

    # EXperiment
    

    obj.conn.close()