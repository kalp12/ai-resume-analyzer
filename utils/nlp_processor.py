import ollama
import os
from google import genai
import json

api_key = os.getenv("GEMINI_API_KEY")


def generate_response_from_llama_gemma(query):
    response = ollama.chat(
        model="gemma",
        messages=[{"role": "user", "content": query}]
    )
    return response["message"]["content"]

def generate_response_from_llama_mistral(query):
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": query}]
    )
    return response["message"]["content"] 

def generate_response_from_llama_lama2(query):
    response = ollama.chat(
        model="llama2:7b",
        messages=[{"role": "user", "content": query}]
    )
    return response["message"]["content"]

def generate_response_from_llama_gemma2(query):
    response = ollama.chat(
        model="gemma:2b",
        messages=[{"role": "user", "content": query}]
    )
    return response["message"]["content"]

def generate_response_from_llama_gemini(query):
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=query
    )
    return response.text
    # print(response)

def analyze_resume_gemini(text,links):
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

    response = generate_response_from_llama_gemini(prompt)
    # response = generate_response_from_llama_gemma(prompt)        
#     response = """json
# {
#   "Full Name": "Trupesh Gohil",
#   "Contact Information": {
#     "Phone": "+91 8104013404",
#     "Email": "trupeshgohil10@gmail.com",
#     "LinkedIn": "http://www.linkedin.com/in/trupesh-gohil-49193a147",
#     "Github": "https://github.com/Evolution38"
#   },
#   "Resume Summary": "To secure a challenging position where I can effectively contribute my skills and grow with the organization in terms of role, responsibility, and knowledge.",
#   "Job Titles": [
#     "Software Engineer",
#     "Flutter App Developer Intern"
#   ],
#   "Work Experience": [
#     {
#       "years": "July 2022 - Present",
#       "company": "LTIMindtree",
#       "role": "Software Engineer",
#       "description": "Creating dashboard for the logs data and represent that in different graphical representation on the website. Also giving insights from logs data and making it useful for users to understand. Developed APIs for the Dashboard to fetch the data from the database and send response in required format. Integrated APIs with the dashboard so the live data will get displayed also added filters for the dashboard. Tech Stack: Vue.js, Java Spring Boot, Python (NLP), PostgreSQL."
#     },
#     {
#       "years": "Nov 2021 – Jan 2022",
#       "company": "StudyLeague IT Solutions LLP (SLITS)",
#       "role": "Flutter App Developer Intern",
#       "description": "Served as a developer and mentor at the company, responsible for training new hires and contributing to application development. Guided and managed new employees, and successfully developed and deployed two cross-platform applications on the Play Store and App Store. Tech Stack: Flutter, Firebase."
#     },
#     {
#       "years": "Sep 2020 - Nov 2020",
#       "company": "WiseCreator.",
#       "role": "Flutter App Developer Intern",
#       "description": "I was developer intern in the company and my role was to research and development on applications UI for Android TV. With R&D I was responsible for developing the front-end UI for the Android TV in Flutter. Tech Stack: Flutter."
#     }
#   ],
#   "Skills": [
#     "Spring Boot",
#     "Vue.js",
#     "JavaScript",
#     "Python",
#     "Java",
#     "Flutter",
#     "MySQL",
#     "PostgreSQL",
#     "Firebase",
#     "Git",
#     "Kubernetes",
#     "Docker",
#     "Android Studio"
#   ],
#   "Education": [],
#   "Certifications": [],
#   "Projects": [
#     {
#       "Title": "Garage Project",
#       "Link": null,
#       "description": "Making proofs of concept for use cases, business case studies, and assigned tech cases. Additionally, focusing on the specified use case solution design. Adding business logic to current products to improve their functionality and performance. Tech Stack: Python, Apache Guacamole"
#     },
#     {
#       "Title": "Canvas AIOPs: iSOP",
#       "Link": null,
#       "description": "This project is focused on analyzing and processing video data to auto-generate digital SOPs from multiple sources, resulting in a streamlined single video output with streaming capabilities. Developed an interface to display insightful analytics and data visualizations in graph view, enhancing user understanding and application of video insights. Tech Stack: Spring boot, Vue.js, LLM Model, Flask, PostgreSQL"
#     },
#     {
#       "Title": "B.E. Final Project: IBackPack (An AR Tour Guide App)",
#       "Link": null,
#       "description": "Developed an augmented reality travel app using Unity, enabling users to access location data, street maps, ratings, and nearby points of interest in real-time during their travels. Tech Stack: Flutter, Unity, Firebase"
#     },
#     {
#       "Title": "Diploma Final Project: Bus Occupancy",
#       "Link": null,
#       "description": "Developed a Bus Occupancy Application to streamline public transport operations, offering real-time bus occupancy data, online ticket booking, and estimated arrival times to enhance passenger experience and support paperless transactions. Leveraged GPS data and user-friendly interfaces to provide travelers with up-to-date bus locations and passenger counts, significantly reducing workload for public transport staff. Tech Stack: Android Studio, Java. Firebase, Arduino."
#     },
#     {
#       "Title": "Smart India Hackathon 2018: Secure Digital Ticket Passing",
#       "Link": null,
#       "description": "Developed a secure digital train ticketing application for SIH 2018, featuring online booking, QR code generation encrypted with SHA1 and SHA256, and a 13-digit ticket number system. Implemented a USSD-based simulation for ticket booking and integrated a decryption tool for ticket checkers to verify journey details. Tech Stack: Android Studio, Java, Firebase."
#     }
#   ],
#   "Training Experience": []
# }
# """
    response = response.strip("```json").strip("```")
    response = json.loads(response)
    return response


if __name__ == "__main__":
    analyze_resume_gemini("KALP MOTA\nMumbai, India | +91 9821625551 | LinkedIn | Email | Github\nBrief Introduction\nA highly skilled software engineer with 2+ years of experience specializing in Python, SQL, AWS, and platform\nintegration. Expertise in designing and developing solutions, working with APIs, and leveraging large language models\n(LLM) for innovative applications. Proven ability to streamline processes by automating workflows and integrating third-\nparty platforms using AWS, ServiceNow and Boto3. Seeking to apply technical expertise in a dynamic role to drive\ninnovation and efficiency.\nEducation College Graduation Year Percentage\nB.E. in Electronics and K.C. College of Engineering Management Studies June 2022 8.09 CGPA\nTelecommunication and Research\nDiploma in Computer Technology Shah and Anchor Kutchhi Polytechnic June 2019 76.59%\nSkills\n• Languages/Technologies: Python, SQL, AWS (Lambda, EC2, S3), Boto3, RESTful APIs, Docker, Flask, FastAPI, Django\n• Tools/Platforms: AWS CloudFormation, Git, Jenkins, PostgreSQL, MySQL, Informatica\n• Machine Learning: LLM (Large Language Models), TensorFlow, Keras, GPT\nProfessional Experience\nProduct Engineer\nLTIMindtree, Internal Project - Aspect | September 2022 – April 2023\n• Contributed to the internal Aspect project, developing innovative AI-driven solutions for document processing, including\ntext processors, named entity recognizers, image classification, and table extraction.\n• Worked on building models for City National Bank and Simon-Kucher & Partners, customizing NLP and machine learning\nsolutions to meet client requirements.\n• Trained, deployed, and demonstrated models tailored to client needs, utilizing Python and AWS to automate workflows and\nintegrate solutions.\n• Worked on features like document splitting, knowledge nugget extraction, sentiment analysis, and object identification for\nreal-time analysis.\nPython Developer\nTravelers (Client) - LTIMindtree | May 2023 – September 2023\n• Developed custom scripts to automate the conversion of insurance form data from Excel to JSON, streamlining form\nprocessing for various insurance types.\n• Utilized Python to automate the population of PDFs with client data, saving manual input time and increasing accuracy.\n• Collaborated with the team to integrate API solutions for automated data dumping into the client’s database, ensuring\nseamless data flow and synchronization.\n• Enhanced workflow efficiency by automating data extraction, reducing processing time and improving the accuracy of\ninsurance document handling.\nPython Backend Developer\nLTIMindtree (Aspect Project) | September 2023 – September 2024\n• Designed and developed backend solutions for the Aspect platform using Python, FastAPI, and Flask to create scalable,\nhigh-performance APIs.\n• Integrated LLM (Large Language Models), enhancing the platform’s capabilities with features like OCR, regex-based\nextraction, and document post-processing using Camelot for tabular data.\n• Implemented third-party app integration using async operations, improving platform functionality and responsiveness.\n• Implemented custom functionalities, including duplicate annotation detection and LLM model fine-tuning for text\nprocessing.\n• Contributed to the optimization of machine learning models, particularly for GPT and other language model applications,\nimproving accuracy.\n• Developed custom scripts to interact with REST APIs, retrieving only the client-required data while filtering out unnecessary\ninformation, improving data handling efficiency.\nPython Developer\nZendesk | October 2024 – Present\n• Working as a Python Developer responsible for backend systems and API development to improve customer service\nsolutions.\n• Developing scalable solutions using Python, Flask, and FastAPI while integrating third-party applications to extend product\nfunctionalities.\n• Leveraging AWS and SQL databases to enhance the architecture and implement efficient cloud solutions for data processing\nand storage.\n• Collaborating with cross-functional teams to continuously improve system performance, maintain code quality, and solve\ncomplex backend challenges.\nTraining Experience\nLTI (Training Period) | July 2022 - September 2022 (3 months)\n● Underwent 3 months of extensive training on Informatica to gain hands-on experience in data integration, transformation,\nand ETL processes.\n● Developed strong proficiency in data management and migration strategies, optimizing data flow across various systems.\n● Received training and completed assignments in multiple programming languages, including SQL, Python, and Java.\nProjects:\n➢ IBackPack (An AR Tour Guide App): My bachelor’s Final Year project that was developed for visitors to find exciting\nonline information during their travels. Unity was integrated for the augmented reality to interact with the user’s views. The\napp will display information such as location, street map, ratings, and key nearby locations related to. Users will have\nconsistent information about their target location.\nLink to Project: Final Year Project\n➢ Telegram Bot with Weather Forecast (Python): Developed a Telegram bot using the python-telegram-bot library,\nintegrated with OpenWeatherMap API for weather forecasting. The bot allows users to interact through various commands,\nincluding /start, message echoing, inline keyboard options, and sharing their location. Upon receiving the user’s location, the\nbot fetches weather data using the OWM API and returns detailed forecasts, such as temperature, status, and conditions for\nthe next few hours. This project showcases skills in bot development, API integration, and user interaction via a chatbot\ninterface.\nLink to Project: Project Link\n➢ Data Science Jupyter Notebook (Python, Pandas): A data analysis project where I performed various data science tasks\nusing 911.csv and USA Housing.csv datasets. The project involved data cleaning, exploratory data analysis (EDA), and\nvisualization using Pandas and Matplotlib to uncover insights from the data. Key tasks included handling missing values,\ndata transformations, and statistical analysis.\nLink to Project: Project Link\n➢ WhatsApp Bot (Flask, Twilio, MongoDB): Developed a WhatsApp-based chatbot for a bakery using Flask, Twilio API,\nand MongoDB to handle customer interactions. The bot allows users to place orders, check the bakery's working hours, and\nget contact details. Customers can choose from a list of cakes, provide their address, and receive a confirmation of their order.\nThe system also stores user interactions in a MongoDB database for future reference and order tracking. This project\ndemonstrates skills in building chatbots, integrating with WhatsApp using Twilio, and managing data with MongoDB.\nLink to Project: Project Link\n➢ GSM-based Wireless E-Noticeboard: My diploma final year project that aimed to create a wireless noticeboard system for\ndisplaying messages remotely. The project utilized Arduino UNO for controlling the process, a GSM module to receive SMS\nmessages from a mobile phone, and an LCD to display the content. The system automatically parsed SMS messages and\nextracted the main notice, which was then displayed on the board, providing an efficient way to update notices from any\nlocation.\nCertificates\n• Multidisciplinary Conference on Engineering Science & Technology (MCEST 2022) – Presented Ibackpack: An AR Tour\nGuide App.\n• Python certifications\n• Generative AI certifications\n• Internship and Training certificates\nFor a complete list of certifications, please visit: Link",
    [
    "https://www.linkedin.com/in/kalp-mota-357514148/",
    "mailto:kalpmota2000@gmail.com",
    "https://github.com/kalp12",
    "https://drive.google.com/drive/folders/1htCDvPKy_fM1bEyvUsXCrAxOCl9da8YR?usp=sharing",
    "https://github.com/kalp12/telegram_bot_python",
    "https://github.com/kalp12/Data_science_jupyternotebook/",
    "https://github.com/kalp12/automate-whatsapp",
    "https://drive.google.com/drive/folders/1kXpMRaRJBQnnH9iSDYo-2GQx5HiR5p34?usp=sharing"
  ]
)