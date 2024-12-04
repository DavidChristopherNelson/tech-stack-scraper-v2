import openai
import json
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
openai.api_key = os.getenv("OPEN_AI_PASSWORD")

results = {}
results['https://www.workatastartup.com/jobs/68519'] = """Companies & jobs\nEvents\nInbox\nMy profile\nBobby\nCompanies\n/\nInfisical (W23)\n/\nJobs\nFull Stack Engineer (Remote) at Infisical (W23)\n$50K - $150K  •  0.10% - 0.50%\nOpen-source secrets manager for developers\nRemote\nFull-time\n1+ years\nApply\nSave\nAbout Infisical\nInfisical is the #1 open source secret management platform – used by tens of thousands of developers.\nWe raised $3M from Y Combinator, Gradient Ventures (Google's VC fund), and awesome angel investors like Elad Gil, Arash Ferdowsi (founder/ex-CTO of Dropbox), Paul Copplestone (founder/CEO of Supabase), James Hawkins (founder/CEO of PostHog), Andrew Miklas (founder/ex-CTO of PagerDuty), Diana Hu (GP at Y Combinator), and more.\nWe are default alive, and have signed many customers ranging from fastest growing startups to post-IPO enterprises.\nAbout the role\nSkills: Go, Node.js, React, TypeScript, Docker, Amazon Web Services (AWS)\nAbout Infisical\nInfisical is the #1 open source secret management platform for developers. In other words, we help organizations manage API-keys, DB access tokens, certificates, and other credentials across all parts of their infra! In fact, we process over 2B of such secrets per month.\nOur customers already include some of the largest public enterprises and some of the fastest-growing startups. Developers love us and every day our community is growing stronger! Join us on a mission to make security easier for all developers – starting from secret management.\nAbout this role\nInfisical is looking for a full stack engineer to help us build, optimize, and create the foundations of the product. You will be working closely with our CTO and the rest of the engineering team on:\nmaking Infisical usable across a wide range of tech stacks;\nmaintaining our infrastructure;\nensuring our customers have a great experience;\nimplementing and advancing functionality like automatic secret rotation;\nexperimenting with new approaches for secret management in the AI world.\nOverall, you’re going to be one of the defining pieces of our team as we scale to thousands of customers over the next 18 months.\nAbout you\nThis job will require you to be a Swiss army knife of an engineer. Overall, this role demands the following pivotal skills:\nstrong proficiency in Node.js development using TypeScript\nfull-stack development, with strong expertise in both backend and frontend\nreact and Tailwind CSS for frontend development\nunderstanding of cloud-native architecture and infrastructure management with tools such as Docker\nOn any given day, you may be:\ndeveloping new features that will be used by tens of thousands of developers.\nworking on resiliency and stability of the Infisical platform.\nimproving security and cryptography practices.\nsquashing bugs as well as talking to our community and enterprise customers.\nhyper-polishing Infisical's UI/UX/DX.\npresenting your work (e.g., new features/learnings) through blogs or videos to our community. or all of the above!\nHow you will grow?\nWith this role, you play the defining role in building out Infisical, choosing the right technologies, setting up all the necessary processes from the start, solving scalability issues, as well as making sure that our community and customer base keeps growing.\nAs our team grows and you get more experience on the team, you'll also have the opportunity to fully own particular parts of the platform end-to-end.\nTeam, Values & Benefits\nOur team has worked across transformative tech companies, from Figma to AWS to Red Hat.\nWe have an office in San Francisco, but we are mostly a remote team. We try to get together as often as possible – whether it's for an off-site, conferences, or just get-togethers. This is a full-time role open to anyone in North/South American and European time zones.\nAt Infisical, we will treat you well with a competitive salary and equity offer. Depending on your risk tolerance, we would love to talk more with you about the range of options available between the two. For some other benefits (including lunch stipend, work setup budget, etc), please check out our careers page: https://infisical.com/careers.\nOther jobs at Infisical\nFull Stack Engineer (SF)\nFulltimeSan Francisco, CA, USFull Stack$140K - $200K0.10% - 0.50%3+ Years\nView Job\nEnterprise Account Executive\nFulltimeSan Francisco, CA, US / Remote (US; GB; DE; FR; ES; NL; BE; CA; AT; CH; SE)$90K - $180K0.10% - 0.50%Any (New Grads Ok)\nView Job\nBiz Ops (Business Operations)\nFulltimeSan Francisco, CA, US / Remote$50K - $120K0.05% - 0.25%Any (New Grads Ok)\nView Job\nCustomer Success Engineer\nFulltimeSan Francisco, CA, US / Remote (US; CA)Full Stack$90K - $150K0.10% - 0.50%1+ Years\nView Job\nFull Stack Engineer (Remote)\nFulltimeRemoteFull Stack$50K - $150K0.10% - 0.50%1+ Years\nView Job\nAbout\nFAQ\nContact\nPress\nLegal"""

response = openai.ChatCompletion.create(
    model="gpt-4",  # Use "gpt-3.5-turbo" for ChatGPT 3.5
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": 
         f"""Your response should be a python dictionary with three keys. First 
         key is "average_salary". First key's value is a single number that is 
         the average between the lower salary range limit and the higher 
         salary range limit contained in the following job description. If no 
         salary range is provided than the first key's value should be "NA". 
         The second key is "tech_stack". The second key's value is a list of 
         strings. These strings are the names of any technologies or skills 
         that are mentioned in the job description. Examples of strings 
         include Torch, PyTorch, Python, TypeScriptnext.js, nest.js, python, 
         aws, gcp, azure, kubernetes, Typescript, Javascript, Golang, API, 
         Django, React Native, Webflow, React Web, CSS, HTML, JS, Python 3.0, 
         Nginx, Wireless, XML, SMTP, Scrapy, Five 9s of availability, 
         multithreading, Git, SMTP, IMAP, SMS, MMS, and the like. Here is 
         the job description. {results['https://www.workatastartup.com/jobs/68519']}"""}
    ],
    temperature=0.7,
    max_tokens=100
)

print("------------------------------------- response -------------------------------------")
print(response)

print("------------------------------------- response_text -------------------------------------")
response_text = response['choices'][0]['message']['content']
print(response_text)

print("------------------------------------- try to turn into json -------------------------------------")
try:
    response_dict = json.loads(response_text)
    print(response_dict)
except json.JSONDecodeError as e:
    print(f"Failed to parse JSON: {e}")
    print(f"Response text was: {response_text}")

print("end of program")
