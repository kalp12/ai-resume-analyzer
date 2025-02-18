import spacy
import re

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Predefined list of skills
SKILLS_DB = {"python", "java", "sql", "machine learning", "deep learning", "tensorflow",
             "pandas", "numpy", "django", "flask", "javascript", "react", "angular"}

# Common job titles
JOB_TITLES = {"software engineer", "data scientist", "project manager",
              "web developer", "backend developer", "frontend developer"}

def extract_skills(text):
    """Extract skills from resume text."""
    doc = nlp(text.lower())  
    return list({token.text for token in doc if token.text in SKILLS_DB})

def extract_experience(text):
    """Extract experience and job titles."""
    experience = []

    # Regex to detect years of experience
    exp_patterns = [r"(\d{1,2})\s*years?\s*experience", r"(\d{1,2})\s*yrs?\s*experience"]
    for pattern in exp_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            experience.append(f"{match.group(1)} years experience")

    # Extract job titles
    doc = nlp(text.lower())
    job_titles = list({token.text for token in doc if token.text in JOB_TITLES})

    return {"experience": experience, "job_titles": job_titles}

import ollama


def generate_response_from_llama(query):
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": query}]
        # ,
        # options={
        #     "num_predict": 100,  # Limit response length (faster)
        #     "top_k": 50,  # Sampling to make generation faster
        #     "top_p": 0.9,  # Nucleus sampling for better speed
        # },
    )
    # print(response)
    return response["message"]["content"]


# def analyze_resume(text):
#     """Analyze resume text for skills, experience, and job titles."""
#     return {
#         "skills": extract_skills(text),
#         "experience": extract_experience(text)["experience"],
#         "job_titles": extract_experience(text)["job_titles"]
#     }

import ollama

def generate_response_from_llama_gemma(query):
    response = ollama.chat(
        model="gemma",
        messages=[{"role": "user", "content": query}]
    )
    return response["message"]["content"]

def analyze_resume_gemma(text,links):
    """Analyze resume text for skills, experience, and job titles."""
    prompt = f"""
    Extract the following details from the resume:
    - Full Name
    - Contact Information (Phone, Email)
    - Job Titles
    - Work Experience (years, company, role)
    - Skills
    - Education
    
    Resume Text:
    {text}

    Links:
    {links}
    Format the output as JSON.
    """

    response = generate_response_from_llama(prompt)
    print(response)
    return response  # Return the structured JSON response

########################################################


def generate_response_from_llama_mistral(query):
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": query}]
    )
    return response["message"]["content"]

def analyze_resume_mistral(text,links):
    """Analyze resume text for skills, experience, and job titles."""
    prompt = f"""
    Extract the following details from the resume:
    - Full Name
    - Contact Information (Phone, Email, LinkedIn, Github)
    - Resume Summary
    - Job Titles
    - Work Experience (years, company, role ,short description)
    - Skills (e.g., Python, Java, etc.)
    - Education (Degree, Institution, Year)
    - Certifications
    - Projects (Title, Link,short description)
    - Training Experience (Company, Duration)
    
    Resume Text:
    {text}
    
    Links:
    {links}

    Format the output as JSON.
    """

    response = generate_response_from_llama_mistral(prompt)
    print(response)
    return response 

def generate_response_from_llama_lama2(query):
    response = ollama.chat(
        model="llama2:7b",
        messages=[{"role": "user", "content": query}]
    )
    return response["message"]["content"]

def analyze_resume_lama2(text,links):
    """Analyze resume text for skills, experience, and job titles."""
    prompt = f"""
    Extract the following details from the resume:
    - Full Name
    - Contact Information (Phone, Email, LinkedIn, Github)
    - Resume Summary
    - Job Titles
    - Work Experience (years, company, role ,short description)
    - Skills (e.g., Python, Java, etc.)
    - Education (Degree, Institution, Year)
    - Certifications
    - Projects (Title, Link,short description)
    - Training Experience (Company, Duration)
    
    Resume Text:
    {text}
    
    Links:
    {links}

    Format the output as JSON.
    """

    response = generate_response_from_llama_lama2(prompt)
    print(response)
    return response 

def generate_response_from_llama_gemma2(query):
    response = ollama.chat(
        model="gemma:2b",
        messages=[{"role": "user", "content": query}]
    )
    return response["message"]["content"]

def analyze_resume_gemma2(text,links):
    """Analyze resume text for skills, experience, and job titles."""
    prompt = f"""
    Extract the following details from the resume:
    - Full Name
    - Contact Information (Phone, Email, LinkedIn, Github)
    - Resume Summary
    - Job Titles
    - Work Experience (years, company, role ,short description)
    - Skills (e.g., Python, Java, etc.)
    - Education (Degree, Institution, Year)
    - Certifications
    - Projects (Title, Link,short description)
    - Training Experience (Company, Duration)
    
    Resume Text:
    {text}
    
    Links:
    {links}

    Format the output as JSON.
    """

    response = generate_response_from_llama_gemma2(prompt)
    print(response)
    return response 


if __name__ == "__main__":
    analyze_resume_gemma2("KALP MOTA\nMumbai, India | +91 9821625551 | LinkedIn | Email | Github\nBrief Introduction\nA highly skilled software engineer with 2+ years of experience specializing in Python, SQL, AWS, and platform\nintegration. Expertise in designing and developing solutions, working with APIs, and leveraging large language models\n(LLM) for innovative applications. Proven ability to streamline processes by automating workflows and integrating third-\nparty platforms using AWS, ServiceNow and Boto3. Seeking to apply technical expertise in a dynamic role to drive\ninnovation and efficiency.\nEducation College Graduation Year Percentage\nB.E. in Electronics and K.C. College of Engineering Management Studies June 2022 8.09 CGPA\nTelecommunication and Research\nDiploma in Computer Technology Shah and Anchor Kutchhi Polytechnic June 2019 76.59%\nSkills\n• Languages/Technologies: Python, SQL, AWS (Lambda, EC2, S3), Boto3, RESTful APIs, Docker, Flask, FastAPI, Django\n• Tools/Platforms: AWS CloudFormation, Git, Jenkins, PostgreSQL, MySQL, Informatica\n• Machine Learning: LLM (Large Language Models), TensorFlow, Keras, GPT\nProfessional Experience\nProduct Engineer\nLTIMindtree, Internal Project - Aspect | September 2022 – April 2023\n• Contributed to the internal Aspect project, developing innovative AI-driven solutions for document processing, including\ntext processors, named entity recognizers, image classification, and table extraction.\n• Worked on building models for City National Bank and Simon-Kucher & Partners, customizing NLP and machine learning\nsolutions to meet client requirements.\n• Trained, deployed, and demonstrated models tailored to client needs, utilizing Python and AWS to automate workflows and\nintegrate solutions.\n• Worked on features like document splitting, knowledge nugget extraction, sentiment analysis, and object identification for\nreal-time analysis.\nPython Developer\nTravelers (Client) - LTIMindtree | May 2023 – September 2023\n• Developed custom scripts to automate the conversion of insurance form data from Excel to JSON, streamlining form\nprocessing for various insurance types.\n• Utilized Python to automate the population of PDFs with client data, saving manual input time and increasing accuracy.\n• Collaborated with the team to integrate API solutions for automated data dumping into the client’s database, ensuring\nseamless data flow and synchronization.\n• Enhanced workflow efficiency by automating data extraction, reducing processing time and improving the accuracy of\ninsurance document handling.\nPython Backend Developer\nLTIMindtree (Aspect Project) | September 2023 – September 2024\n• Designed and developed backend solutions for the Aspect platform using Python, FastAPI, and Flask to create scalable,\nhigh-performance APIs.\n• Integrated LLM (Large Language Models), enhancing the platform’s capabilities with features like OCR, regex-based\nextraction, and document post-processing using Camelot for tabular data.\n• Implemented third-party app integration using async operations, improving platform functionality and responsiveness.\n• Implemented custom functionalities, including duplicate annotation detection and LLM model fine-tuning for text\nprocessing.\n• Contributed to the optimization of machine learning models, particularly for GPT and other language model applications,\nimproving accuracy.\n• Developed custom scripts to interact with REST APIs, retrieving only the client-required data while filtering out unnecessary\ninformation, improving data handling efficiency.\nPython Developer\nZendesk | October 2024 – Present\n• Working as a Python Developer responsible for backend systems and API development to improve customer service\nsolutions.\n• Developing scalable solutions using Python, Flask, and FastAPI while integrating third-party applications to extend product\nfunctionalities.\n• Leveraging AWS and SQL databases to enhance the architecture and implement efficient cloud solutions for data processing\nand storage.\n• Collaborating with cross-functional teams to continuously improve system performance, maintain code quality, and solve\ncomplex backend challenges.\nTraining Experience\nLTI (Training Period) | July 2022 - September 2022 (3 months)\n● Underwent 3 months of extensive training on Informatica to gain hands-on experience in data integration, transformation,\nand ETL processes.\n● Developed strong proficiency in data management and migration strategies, optimizing data flow across various systems.\n● Received training and completed assignments in multiple programming languages, including SQL, Python, and Java.\nProjects:\n➢ IBackPack (An AR Tour Guide App): My bachelor’s Final Year project that was developed for visitors to find exciting\nonline information during their travels. Unity was integrated for the augmented reality to interact with the user’s views. The\napp will display information such as location, street map, ratings, and key nearby locations related to. Users will have\nconsistent information about their target location.\nLink to Project: Final Year Project\n➢ Telegram Bot with Weather Forecast (Python): Developed a Telegram bot using the python-telegram-bot library,\nintegrated with OpenWeatherMap API for weather forecasting. The bot allows users to interact through various commands,\nincluding /start, message echoing, inline keyboard options, and sharing their location. Upon receiving the user’s location, the\nbot fetches weather data using the OWM API and returns detailed forecasts, such as temperature, status, and conditions for\nthe next few hours. This project showcases skills in bot development, API integration, and user interaction via a chatbot\ninterface.\nLink to Project: Project Link\n➢ Data Science Jupyter Notebook (Python, Pandas): A data analysis project where I performed various data science tasks\nusing 911.csv and USA Housing.csv datasets. The project involved data cleaning, exploratory data analysis (EDA), and\nvisualization using Pandas and Matplotlib to uncover insights from the data. Key tasks included handling missing values,\ndata transformations, and statistical analysis.\nLink to Project: Project Link\n➢ WhatsApp Bot (Flask, Twilio, MongoDB): Developed a WhatsApp-based chatbot for a bakery using Flask, Twilio API,\nand MongoDB to handle customer interactions. The bot allows users to place orders, check the bakery's working hours, and\nget contact details. Customers can choose from a list of cakes, provide their address, and receive a confirmation of their order.\nThe system also stores user interactions in a MongoDB database for future reference and order tracking. This project\ndemonstrates skills in building chatbots, integrating with WhatsApp using Twilio, and managing data with MongoDB.\nLink to Project: Project Link\n➢ GSM-based Wireless E-Noticeboard: My diploma final year project that aimed to create a wireless noticeboard system for\ndisplaying messages remotely. The project utilized Arduino UNO for controlling the process, a GSM module to receive SMS\nmessages from a mobile phone, and an LCD to display the content. The system automatically parsed SMS messages and\nextracted the main notice, which was then displayed on the board, providing an efficient way to update notices from any\nlocation.\nCertificates\n• Multidisciplinary Conference on Engineering Science & Technology (MCEST 2022) – Presented Ibackpack: An AR Tour\nGuide App.\n• Python certifications\n• Generative AI certifications\n• Internship and Training certificates\nFor a complete list of certifications, please visit: Link",
    [
    "https://www.linkedin.com/in/kalp-mota-357514148/",
    "mailto:kalpmota2000@gmail.com",
    "https://github.com/kalp12",
    "https://drive.google.com/drive/folders/1htCDvPKy_fM1bEyvUsXCrAxOCl9da8YR?usp=sharing",
    "https://github.com/kalp12/telegram_bot_python",
    "https://github.com/kalp12/Data_science_jupyternotebook/",
    "https://github.com/kalp12/automate-whatsapp",
    "https://drive.google.com/drive/folders/1kXpMRaRJBQnnH9iSDYo-2GQx5HiR5p34?usp=sharing"
  ])
    