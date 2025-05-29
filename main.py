import asyncio
from dotenv import load_dotenv
from google.genai.types import (
    GenerateContentConfig,
    GenerateContentResponse,
)
import json
import pprint

import gemini_driver
from models.gemini_agent import GeminiAgent


def main():
    load_dotenv()

    all_resume_exp = []
    with open('all_resume_exp.txt', 'r') as file:
        all_resume_exp = file.readlines()

    # model (from https://ai.google.dev/gemini-api/docs/models)
    model = 'gemini-1.5-flash'

    # initialize gemini agent
    numEstExperiencesTotal = 7
    numEstBulletsTotal = 17
    font_size = 10  # font size in points
    latex_page_margins = [1.5, 1.5, 2.2, 0]  # left, right, top, bottom in cm
    space_between_bullets = -1
    systemInstructions = (
        'You are a resume expert who is able to parse through job descriptions and Latex-created resumes to craft a new one-page resume in Latex that matches the experience from the job description as best as possible. '
        'You will be given a job description, a list of resume experience in Latex, and you will return a new one-page resume in Latex that matches the job description as best as possible. '
    )
    geminiAgent = GeminiAgent(model = model, system_instruction = systemInstructions)

    # ingest all resume experience
    response: GenerateContentResponse = geminiAgent.sendMessage(
        f'Here is a list of resume experience: {all_resume_exp} '
        'You need to ignore all Latex formatting, newlines, tabs, but make sure you understand the relevant information at each line. '
        'Typically, lines *beginning* with \\textbf mark the beginning of a new experience, and subsequent lines are the details of that experience. '
        'You should only respond with \'Resume experience parsed...\' without the quotes. '
    )
    print(f'{response.text}')

    # get job url and fetch job description with subagent
    # job_url = input("Enter the LinkedIn job URL: ")
    # job_description = asyncio.run(gemini_driver.driver(model = model, url = job_url))
    # print('Job description: ', job_description)

    # %============= FAKE JOB DESCRIPTION FOR TESTING ==============%
    # job_description = "If you're an engineer who thrives on ownership, fast feedback loops, and building features that directly impact users \u2014 this is the role for you. At our fast-growing, Y Combinator-backed startup, we're transforming how teams communicate data by automating the creation of tools and reports that drive high-stakes decisions.\n\nIn this role, you won\u2019t just write code \u2014 you'll shape a product that\u2019s changing the way modern organizations operate. You\u2019ll design and build powerful features like AI-driven insights and automated reporting workflows, all aimed at eliminating tedious work and helping teams focus on what matters. Expect to work closely with users, iterate quickly, and see the real-world impact of your work in days, not months.\n\nJoin a high-performing, remote-first team where your contributions aren\u2019t just valued \u2014 they\u2019re essential to our success. This is your chance to grow with a mission-driven company from the ground up.\n\n**Job Title: Software Engineer (TypeScript)**\n\n**Work Location: Remote \u2013 East Coast Preferred**\n\n**Terms: Direct Hire, Salaried + Equity**\n\n**Key Responsibilities**\n\n* Build scalable features for automated document and presentation generation.\n* Enhance core systems to improve speed, reliability, and performance.\n* Work directly with end-users to understand pain points and ship valuable solutions quickly.\n* Collaborate with a team of thoughtful, highly technical engineers focused on delivering high-quality software.\n\n**Who We're Looking For**\n\n* 2\u20136 years of professional experience in software engineering.\n* At least 1 year of hands-on experience with TypeScript and Node.js.\n* Understand core computer science principles, including algorithms and data structures.\n* Someone who enjoys working closely with product managers, designers, and users to shape and refine products.\n\n**Why You'll Love This Role**\n\n* Work on a meaningful product that helps teams worldwide save time and make better decisions.\n* Join a team of experienced professionals from top-tier tech backgrounds.\n* Enjoy the flexibility of a remote-first workplace.\n* Be part of a product-driven culture with low bureaucracy and high ownership.\n* Participate in bi-annual team offsites to exciting locations.\n* Receive competitive compensation and equity in a high-growth company."
    job_description = "**Application Close Date**Applications will be accepted on an ongoing basis until the requisition is closed.\n\nAt Blue Origin, we envision millions of people living and working in space for the benefit of Earth. We’re working to develop reusable, safe, and low-cost space vehicles and systems within a culture of safety, collaboration, and inclusion. Join our team of problem solvers as we add new chapters to the history of spaceflight! \n\nThis role is part of Blue Origin Operations, which is comprised of Integrated Supply Chain, Facilities, and Security, and Safety, Quality, and Mission Assurance. This includes Manufacturing and Supply Chain support across all Blue Origin facilities. \n\nWe are a diverse team of collaborators, doers, and problem-solvers who are relentlessly committed to a culture of safety. This position will directly impact the history of space exploration and will require your commitment and detailed attention towards safe and repeatable space flight. Join us in lowering the cost of access to space and enabling Blue Origin's vision of millions of people living and working in space to benefit Earth. \n\nWe are seeking a Software Engineer - II who can apply their technical expertise, leadership skills, and commitment to quality to positively impact safe human spaceflight. Passion for our mission and vision is required! \n\nThis role is on the Supply Chain Technology team, where we're creating digital infrastructure for the entire Operations organization. Our primary focus is on building scalable solutions that automate our business processes. You will bring your perspective to aerospace applications for Manufacturing and Supply Chain support across all Blue Origin's facilities. The ideal candidate will be hands-on and ready to dive in. \n\n**Special Mentions**\n\n* Relocation provided\n* Interviews will include a technical assessment\n* Multiple positions available\n**Responsibilities Include But Are Not Limited To**\n\n* Write efficient and maintainable code in languages like Java, Python, and Javascript\n* Craft and build web interfaces in frameworks such as React and Angular\n* Work with cloud platforms and services, such as AWS, Azure, and Google Cloud\n* Implement containerization and orchestration technologies via services like git, Docker, and Kubernetes\n* Maintain comprehensive documentation of tools, processes, and experiments\n**Minimum Qualifications**\n\n* Bachelor's degree in Computer Science, Software Engineering, or a related field\n* 2+ years of proven experience writing software and deploying it to a production environment\n* Working proficiency in coding languages such as Python and Java\n* Experience with cloud computing platforms such as AWS, Azure, or Google Cloud\n* Strong written and verbal communication skills for clear documentation and cross-team collaboration\n* Ability to earn trust, maintain positive and professional relationships, and contribute to a culture of inclusion\n* Must be a U.S. citizen or national, U.S. permanent resident (current Green Card holder), or lawfully admitted into the U.S. as a refugee or granted asylum\n**Preferred Qualifications**\n\n* Demonstrated understanding of deploying web interfaces using React or similar frameworks\n**Compensation Range For**CA applicants is $121,323.00-$169,852.20;WA applicants is $121,323.00-$169,852.20\n\n**Other Site Ranges May Differ****Culture Statement**Don’t meet all desired requirements? Studies have shown that some people are less likely to apply to jobs unless they meet every single desired qualification. At Blue Origin, we are dedicated to building an authentic workplace, so if you’re excited about this role but your past experience doesn’t align perfectly with every desired qualification in the job description, we encourage you to apply anyway. You may be just the right candidate for this or other roles.\n\n**Export Control Regulations**Applicants for employment at Blue Origin must be a U.S. citizen or national, U.S. permanent resident (i.e. current Green Card holder), or lawfully admitted into the U.S. as a refugee or granted asylum.\n\n**Background Check**\n\n* Required for all positions: Blue’s Standard Background Check\n* Required for Certain Job Profiles: Defense Biometric Identification System (DBIDS) background check if at any time the role requires one to be on a military installation\n* Required for Certain Job Profiles: Drivers who operate Commercial Motor Vehicles with a Gross Vehicle Weight (GVW), Gross Vehicle Weight Rating (GVWR) or combination of power unit and trailer that meets or exceeds 10,001 lbs. and/or transports placardable amounts of hazardous materials by ground in any vehicle on a public road while in commerce, may be subject to additional Federal Motor Carrier Safety Regulations including: Driver Qualification Files, Medical Certification, Road Test, Hours of Service, Drug and Alcohol Testing (CDL drivers only), vehicle inspection requirements, CDL requirements (if applicable) and hazardous materials transportation/shipping training.\n**Benefits**\n\n* Benefits include: Medical, dental, vision, basic and supplemental life insurance, paid parental leave, short and long-term disability, 401(k) with a company match of up to 5%, and an Education Support Program.\n* Paid Time Off: Up to four (4) weeks per year based on weekly scheduled hours, and up to 14 company-paid holidays.\n* Discretionary bonus: Bonuses are designed to reward individual contributions as well as allow employees to share in company results.\n* Eligibility for benefits varies by role type, please check with your recruiter for a comprehensive list of the benefits available for this role.\n**Equal Employment Opportunity**Blue Origin is proud to be an Equal Opportunity/Affirmative Action Employer and is committed to attracting, retaining, and developing a highly qualified, diverse, and dedicated work force. Blue Origin hires and promotes people on the basis of their qualifications, performance, and abilities. We support the establishment and maintenance of a workplace that fosters trust, equality, and teamwork, in which all employees recognize and appreciate the diversity of individual team members. We provide all qualified applicants for employment and employees with equal opportunities for hire, promotion, and other terms and conditions of employment, regardless of their race, color, religion, gender, sexual orientation, gender identity, national origin/ethnicity, age, physical or mental disability, genetic factors, military/veteran status, or any other status or characteristic protected by federal, state, and/or local law. Blue Origin will consider for employment qualified applicants with criminal histories in a manner consistent with applicable federal, state, and local laws, including the Washington Fair Chance Act, the California Fair Chance Act, the Los Angeles Fair Chance in Hiring Ordinance, and other applicable laws. For more information on “EEO Is the Law,” please see here. \n\n**Affirmative Action and Disability Accommodation**Applicants wishing to receive information on Blue Origin’s Affirmative Action Plans, or applicants requiring a reasonable accommodation in order to participate in the application and/or interview process, please contact us at EEOCompliance@blueorigin.com. \n\n**California Applicant Privacy Notice**If you are a California resident, please reference the CA Applicant Privacy Notice here."
    # %============= FAKE JOB DESCRIPTION FOR TESTING ==============%


    # ingest job description and output final resume
    config = GenerateContentConfig(
        response_mime_type = 'application/json',
        response_schema = {
            'required': [
                'final_resume',
                'bullet_justifications',
            ],
            'properties': {
                'final_resume': {'type': 'STRING'},
                'bullet_justifications': {
                    'type': 'ARRAY',
                    'minItems': 3,
                    'maxItems': 3,
                    'items': {
                        'type': 'OBJECT',
                        'required': [
                            'bullet_from_resume',
                            'job_desc_sentences',
                            'reasoning',
                        ],
                        'properties': {
                            'bullet_from_resume': {'type': 'STRING'},
                            'job_desc_sentences': {'type': 'STRING'},
                            'reasoning': {'type': 'STRING'},
                        },
                    }
                },
            },
            'type': 'OBJECT',
        }
    )
    message = f'Here is the job description: {job_description}. ' + \
        'Now, with this job description and my resume experience, you need to generate a new one-page resume in Latex that matches the job description as best as possible. ' + \
        f'The font size is {font_size}pt. ' + \
        f'The Latex margins are as follows: {latex_page_margins[0]}cm on the left, {latex_page_margins[1]}cm on the right, {latex_page_margins[2]}cm on the top, and {latex_page_margins[3]}cm on the bottom. ' + \
        'The Latex formatting, font size, latex margins, and bolding should be EXACTLY EXACTLY EXACTLY the same as the resume I gave you. ' + \
        'Do not exclude headers. So, if a work or project experience is listed under a "Work Experience" or "Project Work" section, it should be included in that section in the final resume. ' + \
        'Your only task is to swap out some work experiences and bullet points from the old resume with the ones that match closest to ones in the job description. ' + \
        'Do not add words to any of the bullet points or facts that are not in the original resume experience. ' + \
        'Do NOT add any "\\t" sequences at the beginning of any "\\item", "\\begin", or "\\vspace" sequences if it does not exist in the original resume. ' + \
        'For any bullet points or experiences you include, you should include a justification as to WHY you are including that experience. This should be in a short paragraph (2-3 sentences at most) but it should NOT be part of the final resume. ' + \
        'Additionally, each bullet justification should include the sentence or sentences you\'ve referenced from the job description. These sentences should be stripped of any new lines or unicode characters and should read as plain English. ' + \
        'Rather, your response should be in the following JSON format: {"final_resume": "final_resume", "bullet_justifications": [{"bullet_from_resume": "bullet_from_resume", "job_desc_sentences": "job_desc_sentences", "reasoning": "reasoning"}]}". ' + \
        'Bullets that are included in the final resume, but have no relevance to the job description MUST BE INCLUDED in the bullet_justifications array, but should have a job_desc_sentences and reasoning of "None". ' + \
        'Make sure you try to fill the page up as much as possible, but you should never return a resume that is longer than one page in Latex. Keep the resume to one page in Latex. ' + \
        f'With the resume experience, one page should be around {numEstExperiencesTotal} work and project experiences total, and {numEstBulletsTotal} bullet points total. The number of bullets should never be less than {numEstBulletsTotal} and should never exceed {numEstBulletsTotal + 4}. ' + \
        'Also, ensure you do not exclude the Education and Skills section. The Education and Skills section must be included at all costs'
    if space_between_bullets != None: 
        message += f'In between each bullet point you include, there should be a \\vspace{space_between_bullets}mm command. '
    firstResponse: GenerateContentResponse = geminiAgent.sendMessage(message = message, config = config)

    message = "Here is the first iteration of the resume: " + firstResponse.text + "\n" + \
        "Run the previous command to verify the number of bullets/formatting/etc. are correct, but execute it 2 times to refine each iteration so it matches each part of the original request perfectly"
    response: GenerateContentResponse = geminiAgent.sendMessage(message = message, config = config)

    print('response', response)
    print('response text', response.text)
    data = json.loads(response.text)
    print(data['final_resume'])
    pprint.pprint(data['bullet_justifications'])



if __name__ == "__main__":
    main()