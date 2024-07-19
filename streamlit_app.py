import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="CrewAI Marketing Strategy Generator", page_icon="🚀", layout="wide")

st.title("🚀 CrewAI Marketing Strategy Generator")

# Check for dependencies
try:
    from crewai import Agent, Task, Crew
    from langchain.agents import Tool
    from langchain.chains import LLMChain
    from langchain.llms import OpenAI
    from langchain.prompts import PromptTemplate
    from duckduckgo_search import DDGS
except ImportError as e:
    st.error(f"Failed to import required modules. Error: {e}")
    st.stop()

# Sidebar for API keys
with st.sidebar:
    st.header("API Configuration")
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    
    if openai_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key
    else:
        st.warning("Please enter your OpenAI API key to proceed.")

# Main content
customer_domain = st.text_input("Customer Domain", placeholder="e.g., crewai.com")
project_description = st.text_area("Project Description", placeholder="Describe your marketing project...")

# DuckDuckGo search tool
def web_search(query):
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=5)]
    return results

search_tool = Tool(
    name="Web Search",
    func=web_search,
    description="Useful for searching the web for information."
)

# Agent configurations
def create_agent(role, goal, backstory):
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        verbose=True,
        allow_delegation=False,
        tools=[search_tool]
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

# Task configurations
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

project_understanding_task = create_task(
    "Understand the project details and the target audience for {project_description}. "
    "Review any provided materials and gather additional information as needed.",
    chief_marketing_strategist
)

marketing_strategy_task = create_task(
    "Formulate a comprehensive marketing strategy for the project {project_description} of the customer {customer_domain}. "
    "Use the insights from the research task and the project understanding task to create a high-quality strategy.",
    chief_marketing_strategist
)

campaign_idea_task = create_task(
    "Develop creative marketing campaign ideas for {project_description}. "
    "Ensure the ideas are innovative, engaging, and aligned with the overall marketing strategy.",
    creative_content_creator
)

copy_creation_task = create_task(
    "Create marketing copies based on the approved campaign ideas for {project_description}. "
    "Ensure the copies are compelling, clear, and tailored to the target audience.",
    creative_content_creator
)

if st.button("Generate Marketing Strategy"):
    if not openai_api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
    elif not customer_domain or not project_description:
        st.error("Please fill in all the required fields.")
    else:
        try:
            # Create crew
            crew = Crew(
                agents=[lead_market_analyst, chief_marketing_strategist, creative_content_creator],
                tasks=[research_task, project_understanding_task, marketing_strategy_task, campaign_idea_task, copy_creation_task],
                verbose=2
            )

            with st.spinner("Generating marketing strategy... This may take a few minutes."):
                result = crew.kickoff()
                st.success("Marketing strategy generated successfully!")
                st.write(result)
        except Exception as e:
            st.error(f"An error occurred while generating the marketing strategy: {str(e)}")

st.markdown("---")
st.markdown("Built with ❤️ using CrewAI and Streamlit")
