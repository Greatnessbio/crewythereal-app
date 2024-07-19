import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from langchain.tools import DuckDuckGoSearchRun
from langchain.llms import OpenAI

# Set page config
st.set_page_config(page_title="CrewAI Marketing Strategy Generator", page_icon="🚀", layout="wide")

# Streamlit UI
st.title("🚀 CrewAI Marketing Strategy Generator")

# Sidebar for API key
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

# Initialize tools
search_tool = DuckDuckGoSearchRun()

# Define agents
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
    "Conduct comprehensive analysis of products and competitors, providing in-depth insights to guide marketing strategies.",
    "You are the Lead Market Analyst at a premier digital marketing firm, specializing in dissecting online business landscapes."
)

chief_marketing_strategist = create_agent(
    "Chief Marketing Strategist",
    "Synthesize market insights to formulate innovative and effective marketing strategies.",
    "You are the Chief Marketing Strategist at a leading digital marketing agency, known for crafting bespoke strategies that drive success."
)

creative_content_creator = create_agent(
    "Creative Content Creator",
    "Develop compelling and innovative content for marketing campaigns, with a focus on creating high-impact ad copies.",
    "As a Creative Content Creator at a top-tier digital marketing agency, you excel in crafting narratives that resonate with diverse audiences."
)

# Define tasks
def create_task(description, agent):
    return Task(
        description=description,
        agent=agent
    )

research_task = create_task(
    f"Conduct thorough research on {customer_domain} and its competitors. Analyze the market landscape, target audience, and current trends relevant to: {project_description}",
    lead_market_analyst
)

strategy_task = create_task(
    f"Develop a comprehensive marketing strategy for {customer_domain} based on the research insights. The strategy should address: {project_description}",
    chief_marketing_strategist
)

content_task = create_task(
    f"Create compelling marketing content and campaign ideas for {customer_domain} that align with the developed strategy. Focus on: {project_description}",
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
    if not openai_api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
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
