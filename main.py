import asyncio
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

import gemini_driver
from models.gemini_agent import GeminiAgent


def runAgent(prompt: str, model: str = 'gemini-1.5-flash') -> str:
    client = genai.Client(api_key = os.getenv('GOOGLE_API_KEY'), http_options = types.HttpOptions(api_version = 'v1alpha'))
    
    response = client.models.generate_content(
        model = model,
        contents = prompt,
    )
    
    if not response:
        print('Response is empty')
        return None
    else:
        print(f'Response: {response}')
        print(f'Response text: {response.text}')
        return response.text


def main():
    load_dotenv()

    all_resume_exp = []
    with open('all_resume_exp.txt', 'r') as file:
        all_resume_exp = file.readlines()

    print(all_resume_exp)

    # initialize gemini agent
    font_size = 10  # font size in points
    latex_page_margins = [1.5, 1.5, 2.2, 0]  # left, right, top, bottom in cm
    systemInstructions = (
        'You are a resume expert who is able to parse through job descriptions and Latex-created resumes to craft a new one-page resume in Latex that matches the experience from the job description as best as possible. '
        'You will be given a job description, a list of resume experience in Latex, and you will return a new one-page resume in Latex that matches the job description as best as possible. '
        f'The font size is {font_size}pt. '
        f'The Latex margins are as follows: {latex_page_margins[0]}cm on the left, {latex_page_margins[1]}cm on the right, {latex_page_margins[2]}cm on the top, and {latex_page_margins[3]}cm on the bottom.'
        'Make sure you try to fill the page up as much as possible, but you should never return a resume that is longer than one page in Latex. '
        'You should also never return a bullet or a fact that is not in the original resume experience. You will not add any new facts or experiences that are not in the original resume experience. '
    )
    geminiAgent = GeminiAgent(system_instruction = systemInstructions)

    # ingest all resume experience
    geminiAgent.sendMessage(
        f'Here is a list of resume experience: {all_resume_exp} '
        'You need to ignore all Latex formatting, newlines, tabs, but make sure you understand the relevant information at each line. '
        'Typically, lines *beginning* with \\textbf mark the beginning of a new experience, and subsequent lines are the details of that experience. '
        'Keep your response to a single line, simply confirming that you understand the resume experience provided. '
    )
    # geminiAgent.sendMessage(
    #     "Here is a bit of background about myself: "
    #     "I work at Oracle as a UI/UX Engineer. My current salary is $150,000 per year. "
    #     "I have experience with React, JavaScript, and Python. I have worked on several projects involving user interface design and user experience optimization. "
    #     "I have a Bachelor's degree in Computer Science. I am looking for a new job that pays at least $160,000 per year and involves similar technologies and responsibilities. "
    #     "Keep your response to a single line, simply confirming that you understand the background provided. "
    # )

    while True:
        # get message from user
        prompt = input("Ask me questions about the resume experience or job description, or type 'exit' to quit: ")
        if prompt.lower() == 'exit':
            break
        geminiAgent.sendMessage(prompt)

    print("\nConversation History:")
    for i, message in enumerate(geminiAgent.get_conversation_history()):
        print(f"{i+1}. {message}")

    # get job url and fetch job description with subagent
    # job_url = input("Enter the LinkedIn job URL: ")
    # job_description = asyncio.run(gemini_driver.driver(url = job_url)) 


if __name__ == "__main__":
    main()