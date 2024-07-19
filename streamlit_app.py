import streamlit as st
import os

st.set_page_config(page_title="CrewAI Marketing Strategy Generator", page_icon="🚀", layout="wide")

st.title("🚀 CrewAI Marketing Strategy Generator")

# Check for dependencies
try:
    from crewai import Agent, Task, Crew, Process
    from crewai_tools import SerperDevTool, ScrapeWebsiteTool
except ImportError as e:
    st.error(f"Failed to import required modules. Error: {e}")
    st.stop()

# Sidebar for API keys
with st.sidebar:
    st.header("API Configuration")
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    serper_api_key = st.text_input("Serper API Key", type="password")
    
    if openai_api_key and serper_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key
        os.environ["SERPER_API_KEY"] = serper_api_key
    else:
        st.warning("Please enter your API keys to proceed.")

# Main content
customer_domain = st.text_input("Customer Domain", placeholder="e.g., crewai.com")
project_description = st.text_area("Project Description", placeholder="Describe your marketing project...")

# Agent configurations
agents_config = {
    'lead_market_analyst': {
        'role': 'Lead Market Analyst',
        'goal': 'Conduct amazing analysis of the products and competitors, providing in-depth insights to guide marketing strategies.',
        'backstory': 'As the Lead Market Analyst at a premier digital marketing firm, you specialize in dissecting online business landscapes.'
    },
    'chief_marketing_strategist': {
        'role': 'Chief Marketing Strategist',
        'goal': 'Synthesize amazing insights from product analysis to formulate incredible marketing strategies.',
        'backstory': 'You are the Chief Marketing Strategist at a leading digital marketing agency, known for crafting bespoke strategies that drive success.'
    },
    'creative_content_creator': {
        'role': 'Creative Content Creator',
        'goal': 'Develop compelling and innovative content for social media campaigns, with a focus on creating high-impact ad copies.',
        'backstory': 'As a Creative Content Creator at a top-tier digital marketing agency, you excel in crafting narratives that resonate with audiences.'
    }
}

# Task configurations
tasks_config = {
    'research_task': {
        'description': 'Conduct a thorough research about the customer and competitors in the context of {customer_domain}. Make sure you find any interesting and relevant information given the current year is 2024. We are working with them on the following project: {project_description}.'
    },
    'project_understanding_task': {
        'description': 'Understand the project details and the target audience for {project_description}. Review any provided materials and gather additional information as needed.'
    },
    'marketing_strategy_task': {
        'description': 'Formulate a comprehensive marketing strategy for the project {project_description} of the customer {customer_domain}. Use the insights from the research task and the project understanding task to create a high-quality strategy.'
    },
    'campaign_idea_task': {
        'description': 'Develop creative marketing campaign ideas for {project_description}. Ensure the ideas are innovative, engaging, and aligned with the overall marketing strategy.'
    },
    'copy_creation_task': {
        'description': 'Create marketing copies based on the approved campaign ideas for {project_description}. Ensure the copies are compelling, clear, and tailored to the target audience.'
    }
}

# Function to create agents
def create_agent(config):
    return Agent(
        role=config['role'],
        goal=config['goal'],
        backstory=config['backstory'],
        verbose=True,
        allow_delegation=False,
        tools=[SerperDevTool(), ScrapeWebsiteTool()]
    )

# Function to create tasks
def create_task(config, agent, context=None):
    task = Task(
        description=config['description'].format(
            customer_domain=customer_domain,
            project_description=project_description
        ),
        agent=agent
    )
    if context:
        task.context = context
    return task

if st.button("Generate Marketing Strategy"):
    if not openai_api_key or not serper_api_key:
        st.error("Please enter your API keys in the sidebar.")
    elif not customer_domain or not project_description:
        st.error("Please fill in all the required fields.")
    else:
        try:
            # Create agents
            lead_market_analyst = create_agent(agents_config['lead_market_analyst'])
            chief_marketing_strategist = create_agent(agents_config['chief_marketing_strategist'])
            creative_content_creator = create_agent(agents_config['creative_content_creator'])

            # Create tasks
            research_task = create_task(tasks_config['research_task'], lead_market_analyst)
            project_understanding_task = create_task(tasks_config['project_understanding_task'], chief_marketing_strategist)
            marketing_strategy_task = create_task(tasks_config['marketing_strategy_task'], chief_marketing_strategist)
            campaign_idea_task = create_task(tasks_config['campaign_idea_task'], creative_content_creator)
            copy_creation_task = create_task(tasks_config['copy_creation_task'], creative_content_creator, 
                                            context=[marketing_strategy_task, campaign_idea_task])

            # Create crew
            crew = Crew(
                agents=[lead_market_analyst, chief_marketing_strategist, creative_content_creator],
                tasks=[research_task, project_understanding_task, marketing_strategy_task, campaign_idea_task, copy_creation_task],
                verbose=2,
                process=Process.sequential
            )

            with st.spinner("Generating marketing strategy... This may take a few minutes."):
                result = crew.kickoff()
                st.success("Marketing strategy generated successfully!")
                st.write(result)
        except Exception as e:
            st.error(f"An error occurred while generating the marketing strategy: {str(e)}")

st.markdown("---")
st.markdown("Built with ❤️ using CrewAI and Streamlit")
