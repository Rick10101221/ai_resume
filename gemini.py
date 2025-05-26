import asyncio
import sys

from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, BrowserSession, Controller
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import List

class Job(BaseModel):
    job_description: str


async def main():
    load_dotenv()
    
    controller = Controller(output_model=Job)

    browserSession = BrowserSession(
        executable_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        user_data_dir = 'C:\\Users\\ricke\\.config\\browseruse\\profiles\\default',
    )

    llm = ChatGoogleGenerativeAI(model = "gemini-1.5-flash")

    url = "https://www.linkedin.com/jobs/search/?alertAction=viewjobs&currentJobId=4089515367&origin=JOBS_HOME_JOB_ALERTS&originToLandingJobPostings=4237375978%2C4235035483%2C4237198917&savedSearchId=7835374842"

    agent = Agent(
        #task = f"Navigate to the LinkedIn URL and extract the entire job description. This should be the text under the 'About the job' header. The URL is: {url}",
        task = "Open Google.com and wait for 5 seconds. Then, quit",
        llm = llm,
        browser_session = browserSession,
        controller = controller,
    )

    result = await agent.run()
    data = result.final_result()

    print(data)
    if data:
        parsed: Job = Job.model_validate_json(data)
        print("JOB DESCRIPTION: ", parsed.job_description)
    
    await agent.close()
    await browserSession.close()

if __name__ == "__main__":
    asyncio.run(main())