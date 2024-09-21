from crewai import Task

class Tasks:

  def __init__(self):
    pass

  def create_task_manage_project(self, agent, context_list=[]):
    return Task(
      description='Oversee the entire research project, ensuring all agents work in alignment and the final report meets quality standards.',
      agent=agent,  # chief_editor
      expected_output='A cohesive, accurate, and well-structured final report ready for publication.',
      context=context_list,
      )
  
  # Researcher Task
  def create_task_conduct_research(self, RESEARCH_TOPIC, agent, context_list=[]):
    return Task(
      description=f'''Conduct comprehensive research on the given research topic by accessing various data sources, both static and real-time, via the Internet. Given Research Topic: {RESEARCH_TOPIC}''',
      agent=agent,  # researcher,
      expected_output='A collection of relevant data and insights related to the research topic.',
      context=context_list,  # [task_manage_project],
      output_file="research_data.txt"
      )

  # Editor Task
  def create_task_refine_data(self, agent, context_list=[]):
    return Task(
      description='Refine and validate the gathered research data, ensuring accuracy, cohesion, and logical structure.',
      agent=agent,   # editor,
      expected_output='A refined and validated dataset, ready for review and integration into the report.',
      context=context_list,  # [task_conduct_research],
      )

  # Reviewer Task
  def create_task_review_data(self, agent, context_list=[]):
    return Task(
      description='Critically evaluate the refined research data, ensuring accuracy, depth, and relevance to the research topic.',
      agent=agent,   # reviewer,
      expected_output='A set of feedback or approved refined data that meets high research standards.',
      context=context_list,  # [task_refine_data],
      )

  # Revisor Task
  def create_task_review_draft(self, agent, context_list=[]):
    return Task(
      description='Review and enhance the readability and formatting of the draft, ensuring adherence to citation standards and overall presentation.',
      agent=agent,   # revisor,
      expected_output='A draft that is clear, well-formatted, and adheres to citation standards.',
      context=context_list,   # [task_review_data],
      # output_file="revised_draft.md"
      )

#   # Writer Task
#   def create_task_write_report(self, agent, context_list=[]):
#     return Task(
#       description='Craft a polished and coherent report based on the refined and reviewed content, ensuring it effectively communicates the research findings. Ensure that all the placeholder are filled, If not then remove that section.',
#       agent=agent,   # writer,
#       expected_output='A well-structured, polished report ready for final review and publication. Make sure to write a valid and correct markdown file',
#       context=context_list,   # [task_review_draft],
#       output_file="final_report.md"
#       )

#   # Publisher Task
#   def create_task_publish_report(self, agent, context_list=[]):
#     return Task(
#       description='Prepare the final report for dissemination, optimizing its presentation. And ensuring it is accessible in pdf format.',    #  and ensuring it is accessible in various formats.
#       agent=agent,   # publisher,
#       expected_output='The final report, optimized for presentation in PDF format.',   # and available in multiple formats (e.g., PDF, HTML).
#       context=context_list,   # [task_write_report],
#       output_file="final_report.pdf"
#       )

  # Writer Task
  def create_task_write_report(self, agent, context_list=[]):
    return Task(
      description='Craft a polished and coherent report based on the refined and reviewed content, ensuring it effectively communicates the research findings.',
      agent=agent,   # writer,
      expected_output='A well-structured, polished report ready for final review and publication. Make sure to write a valid and correct markdown file',
      context=context_list,   # [task_review_draft],
      output_file="final_report.md"
      )

  # Publisher Task
  def create_task_publish_report(self, agent, context_list=[]):
    return Task(
      description='Prepare the final report for dissemination, optimizing its presentation and ensuring it is accessible in various formats.',
      agent=agent,   # publisher,
      expected_output='The final report, optimized for presentation in PDF format.',   # and available in multiple formats (e.g., PDF, HTML).
      context=context_list,   # [task_write_report],
      output_file="published_report.pdf"
      )
