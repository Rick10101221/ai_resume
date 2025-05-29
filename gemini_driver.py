import asyncio
from browser_use import Agent, BrowserSession, Controller
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel


class _Job(BaseModel):
    job_description: str


async def getJobDescriptionFromURL(model: str, url: str) -> _Job:
    '''
    Spins up a new browser-use subagent with the provided model and URL to extract a job description.

    Args:
        model (str): The model to use for the agent.
        url (str): The URL of the job posting to extract the description from.
    Returns:
        _Job: A _Job model instance containing the job description.
    '''
    controller = Controller(output_model = _Job)  # fits agent output to _Job model

    # browser session for browser-use
    browserSession = BrowserSession(
        executable_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        user_data_dir = 'C:\\Users\\ricke\\.config\\browseruse\\profiles\\default',
    )

    llm = ChatGoogleGenerativeAI(model = model)

    agent = Agent(
        task = f"Navigate to the LinkedIn URL and extract the entire job description. This should be the text under the 'About the job' header. The URL is: {url}",
        llm = llm,
        browser_session = browserSession,
        controller = controller,
    )

    result = await agent.run()
    data = result.final_result()
    await agent.close()
    await browserSession.close()

    if not data:
        raise RuntimeError("Failed to extract job description from the provided URL.")
    
    parsed: _Job = _Job.model_validate_json(data)
    return parsed


async def driver(model: str, url: str) -> None:
    try:
        job: _Job = await getJobDescriptionFromURL(model = model, url = url)
        # print(f"Job Description: {job.job_description}")
        return job.job_description
    except:
        print("Failed to extract job description. Please check the URL or model.")
        

if __name__ == "__main__":
    asyncio.run(driver())