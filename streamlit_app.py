import streamlit as st
import os
from crewai import Agent, Task, Crew, Process

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

# Define a single agent for simplicity
agent = Agent(
    role="Marketing Strategist",
    goal="Create a comprehensive marketing strategy",
    backstory="You are an experienced marketing strategist with a track record of successful campaigns.",
    verbose=True
)

# Define a single task
task = Task(
    description=f"Create a marketing strategy for {customer_domain}. Project details: {project_description}",
    agent=agent
)

# Create Crew
crew = Crew(
    agents=[agent],
    tasks=[task],
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
