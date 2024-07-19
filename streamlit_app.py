import streamlit as st
import os
from langchain.agents import Tool
from langchain.utilities import SerpAPIWrapper
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# Set page config
st.set_page_config(page_title="AI Marketing Strategy Generator", page_icon="🚀", layout="wide")

# Streamlit UI
st.title("🚀 AI Marketing Strategy Generator")

# Sidebar for API keys
with st.sidebar:
    st.header("API Configuration")
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    serpapi_api_key = st.text_input("SerpAPI Key", type="password")
    
    if openai_api_key and serpapi_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key
        os.environ["SERPAPI_API_KEY"] = serpapi_api_key
    else:
        st.warning("Please enter your API keys to proceed.")

# Main content
customer_domain = st.text_input("Customer Domain", placeholder="e.g., crewai.com")
project_description = st.text_area("Project Description", placeholder="Describe your marketing project...")

# Initialize tools
search = SerpAPIWrapper()
search_tool = Tool(
    name="Search",
    func=search.run,
    description="useful for when you need to answer questions about current events or the current state of the world"
)

# Custom Agent class
class Agent:
    def __init__(self, role, goal, backstory):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.llm = ChatOpenAI(temperature=0.7)

    def run(self, task):
        messages = [
            SystemMessage(content=f"You are a {self.role}. Your goal is to {self.goal}. Backstory: {self.backstory}"),
            HumanMessage(content=f"Task: {task}")
        ]
        response = self.llm(messages)
        return response.content

# Custom Task class
class Task:
    def __init__(self, description, agent):
        self.description = description
        self.agent = agent

    def execute(self):
        return self.agent.run(self.description)

# Custom Crew class
class Crew:
    def __init__(self, agents, tasks):
        self.agents = agents
        self.tasks = tasks

    def run(self):
        results = []
        for task in self.tasks:
            results.append(task.execute())
        return "\n\n".join(results)

# Define agents
lead_market_analyst = Agent(
    "Lead Market Analyst",
    "Conduct comprehensive analysis of products and competitors, providing in-depth insights to guide marketing strategies.",
    "You are the Lead Market Analyst at a premier digital marketing firm, specializing in dissecting online business landscapes."
)

chief_marketing_strategist = Agent(
    "Chief Marketing Strategist",
    "Synthesize market insights to formulate innovative and effective marketing strategies.",
    "You are the Chief Marketing Strategist at a leading digital marketing agency, known for crafting bespoke strategies that drive success."
)

creative_content_creator = Agent(
    "Creative Content Creator",
    "Develop compelling and innovative content for marketing campaigns, with a focus on creating high-impact ad copies.",
    "As a Creative Content Creator at a top-tier digital marketing agency, you excel in crafting narratives that resonate with diverse audiences."
)

# Define tasks
research_task = Task(
    f"Conduct thorough research on {customer_domain} and its competitors. Analyze the market landscape, target audience, and current trends relevant to: {project_description}",
    lead_market_analyst
)

strategy_task = Task(
    f"Develop a comprehensive marketing strategy for {customer_domain} based on the research insights. The strategy should address: {project_description}",
    chief_marketing_strategist
)

content_task = Task(
    f"Create compelling marketing content and campaign ideas for {customer_domain} that align with the developed strategy. Focus on: {project_description}",
    creative_content_creator
)

# Create Crew
crew = Crew(
    agents=[lead_market_analyst, chief_marketing_strategist, creative_content_creator],
    tasks=[research_task, strategy_task, content_task]
)

if st.button("Generate Marketing Strategy"):
    if not openai_api_key or not serpapi_api_key:
        st.error("Please enter your API keys in the sidebar.")
    elif not customer_domain or not project_description:
        st.error("Please fill in all the required fields.")
    else:
        try:
            with st.spinner("Generating marketing strategy... This may take a few minutes."):
                result = crew.run()
                st.success("Marketing strategy generated successfully!")
                st.write(result)
        except Exception as e:
            st.error(f"An error occurred while generating the marketing strategy: {str(e)}")

st.markdown("---")
st.markdown("Built with ❤️ using AI and Streamlit")
