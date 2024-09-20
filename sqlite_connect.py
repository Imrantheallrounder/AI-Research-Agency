import sqlite3

class SqlDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("SQLiteDatabase.db")

    # Create table with fully customised query
    def create_table(self, query):
        try:
            self.conn.execute(f'''{query}''')
            print("Executed Successfully!")
        except Exception as e:
            print(f"Exception occured: {e}")
    
    def create_table(self, table_name, attributes):
        try:
            self.conn.execute(
                f'''
                    Create table {table_name} (
                        {attributes}
                    )
                '''
                )
            print(f"Executed Successfully! and created {table_name} table.")
        except Exception as e:
            print(f"Exception occured: {e}")

    # Insert data with fully customised query
    def insert_data(self, query):
        try:
            self.conn.execute(f'''{query}''')
            self.conn.commit()
            print("Insertion succesful!")
        except Exception as e:
            print(f"Error in Insertion: {e}")

    def insert_data(self, table_name, data_dict):
        try:
            self.conn.execute(
                f'''insert into {table_name} {tuple(data_dict.keys())} VALUES {tuple(data_dict.values())}'''
            )

            self.conn.commit()
            print(f"Insertion succesful! in {table_name}")
        except Exception as e:
            print(f"Error in Insertion: {e}")

    def delete(self, table_name):
        """
        Delete rows
        """
        obj.conn.execute(f'''Delete from {table_name} Where Name="Chief Editor"''')
        obj.conn.commit()


if __name__=='__main__':
    obj = SqlDatabase()

    # ************************************** Users Table creation **************************************
    table = "Users"
    # table_creation_query = '''
    #                 Create table Users (
    #                     User_Id INT AUTO_INCREMENT PRIMARY KEY,
    #                     Username  VARCHAR(50),
    #                     Password VARCHAR(50),
    #                     Email VARCHAR(50)
    #                 )
    #         '''
    # obj.create_table(query=table_creation_query)

    # insertion_query = '''
    # insert into Users (Username, Password, email) VALUES ('Imran', '123456789', 'imran@gmail.com')
    # '''
    # obj.insert_data(query=insertion_query)



    # ************************************** Agents Table creation **************************************
    table = "Agents"
    # agent_table_attributes = '''
    #         Name VARCHAR(50) PRIMARY KEY,
    #         Role  VARCHAR(150),
    #         Goal VARCHAR(1024),
    #         LLM VARCHAR(30),
    #         Tool VARCHAR(100)
    #         '''
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

    # ************************************** LOG Table creation **************************************
    table = "Logs"
    agent_table_attributes = '''
            research_topic VARCHAR(200) PRIMARY KEY,
            'Chief Editor output'  VARCHAR(8000),
            'Researcher output' VARCHAR(8000),
            'Editor output' VARCHAR(8000),
            'Reviewer output' VARCHAR(8000)
            'Revisor output' VARCHAR(8000),
            'Writer output' VARCHAR(8000),
            'Publisher output' VARCHAR(8000),
            '''
    obj.create_table(table_name=table, attributes=agent_table_attributes)

    # EXperiment

    

    obj.conn.close()