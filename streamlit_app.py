import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from langchain.tools import DuckDuckGoSearchRun

# Set page config
st.set_page_config(page_title="CrewAI Marketing Strategy Generator", page_icon="🚀", layout="wide")

# Streamlit UI
st.title("🚀 CrewAI Marketing Strategy Generator")

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

# Initialize tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
duck_search_tool = DuckDuckGoSearchRun()

# Define agents
def create_agent(role, goal, backstory):
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        verbose=True,
        allow_delegation=False,
        tools=[search_tool, scrape_tool, duck_search_tool]
    )

lead_market_analyst = create_agent(
    "Lead Market Analyst",
    "Conduct amazing analysis of the products and competitors, providing in-depth insights to guide marketing strategies.",
    "As the Lead Market Analyst at a premier digital marketing firm, you specialize in dissecting online business landscapes."
)

chief_marketing_strategist = create_agent(
    "Chief Marketing Strategist",
    "Synthesize amazing insights from product analysis to formulate incredible marketing strategies.",
    "You are the Chief Marketing Strategist at a leading digital marketing agency, known for crafting bespoke strategies that drive success."
)

creative_content_creator = create_agent(
    "Creative Content Creator",
    "Develop compelling and innovative content for social media campaigns, with a focus on creating high-impact ad copies.",
    "As a Creative Content Creator at a top-tier digital marketing agency, you excel in crafting narratives that resonate with audiences."
)

# Define tasks
def create_task(description, agent):
    return Task(
        description=description.format(
            customer_domain=customer_domain,
            project_description=project_description
        ),
        agent=agent
    )

research_task = create_task(
    "Conduct a thorough research about the customer and competitors in the context of {customer_domain}. "
    "Make sure you find any interesting and relevant information given the current year is 2024. "
    "We are working with them on the following project: {project_description}.",
    lead_market_analyst
)

strategy_task = create_task(
    "Formulate a comprehensive marketing strategy for the project {project_description} of the customer {customer_domain}. "
    "Use the insights from the research task to create a high-quality strategy.",
    chief_marketing_strategist
)

content_task = create_task(
    "Create compelling marketing content and campaign ideas for {customer_domain} that align with the developed strategy. "
    "Ensure the ideas are innovative, engaging, and tailored to the target audience. Focus on: {project_description}",
    creative_content_creator
)

# Create Crew
crew = Crew(
    agents=[lead_market_analyst, chief_marketing_strategist, creative_content_creator],
    tasks=[research_task, strategy_task, content_task],
    verbose=2,
    process=Process.sequential
)

if st.button("Generate Marketing Strategy"):
    if not openai_api_key or not serper_api_key:
        st.error("Please enter your API keys in the sidebar.")
    elif not customer_domain or not project_description:
        st.error("Please fill in all the required fields.")
    else:
        try:
            with st.spinner("Generating marketing strategy... This may take a few minutes."):
                result = crew.kickoff()
                st.success("Marketing strategy generated successfully!")
                st.write(result)
        except Exception as e:
            st.error(f"An error occurred while generating the marketing strategy: {str(e)}")

st.markdown("---")
st.markdown("Built with ❤️ using CrewAI and Streamlit")
