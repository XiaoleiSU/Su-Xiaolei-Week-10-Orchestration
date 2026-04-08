import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
deepseek_api_base = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
deepseek_model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

if deepseek_api_key:
    os.environ["DEEPSEEK_API_KEY"] = deepseek_api_key
    os.environ["OPENAI_API_KEY"] = deepseek_api_key
os.environ["DEEPSEEK_BASE_URL"] = deepseek_api_base
os.environ["OPENAI_BASE_URL"] = deepseek_api_base

llm = LLM(
    model=f"deepseek/{deepseek_model}",
    base_url=deepseek_api_base,
    api_key=deepseek_api_key,
)

# --- Research Crew ---
researcher = Agent(
    role="Researcher",
    goal="Produce a detailed and well-structured research report for the given topic.",
    backstory=(
        "You are an experienced researcher who gathers reliable information, "
        "organizes key facts clearly, and writes thorough plain-text reports."
    ),
    llm=llm,
    verbose=True,
)

research_task = Task(
    description=(
        "Conduct research on the topic: {topic}. Use web search or knowledge synthesis "
        "to collect relevant background, important concepts, current context, and useful details. "
        "Then produce a detailed research report in pure text only."
    ),
    expected_output=(
        "A detailed plain-text research report about the given topic, including background, "
        "main findings, notable considerations, and a clear overall summary."
    ),
    agent=researcher,
)

research_crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    process=Process.sequential,
    verbose=True,
)

# --- Analysis Crew ---
analyst = Agent(
    role="Analyst",
    goal="Summarize key points, assess risks, and provide actionable feasibility advice.",
    backstory=(
        "You are a careful analyst who reviews research findings, extracts the most important "
        "insights, evaluates potential risks, and provides practical recommendations."
    ),
    llm=llm,
    verbose=True,
)

analysis_task = Task(
    description=(
        "Review the following research report from the previous stage:\n\n"
        "{previous_result}\n\n"
        "Create an analysis that includes: \n"
        "1. A summary of the key points.\n"
        "2. A risk assessment.\n"
        "3. Feasibility suggestions and practical recommendations.\n"
        "Output the final result as a Markdown list."
    ),
    expected_output=(
        "A Markdown list containing key-point summaries, risk assessment items, and feasibility "
        "recommendations based on the previous research report."
    ),
    agent=analyst,
)

analysis_crew = Crew(
    agents=[analyst],
    tasks=[analysis_task],
    process=Process.sequential,
    verbose=True,
)


def get_crews():
    return [research_crew, analysis_crew]
