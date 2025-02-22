import re
import ollama
import os
from google import genai
import json

api_key = os.getenv("GEMINI_API_KEY")


def generate_response_from_llama_gemma(query):
    response = ollama.chat(model="gemma", messages=[{"role": "user", "content": query}])
    return response["message"]["content"]


def generate_response_from_llama_mistral(query):
    response = ollama.chat(
        model="mistral", messages=[{"role": "user", "content": query}]
    )
    return response["message"]["content"]


def generate_response_from_llama_lama2(query):
    response = ollama.chat(
        model="llama2:7b", messages=[{"role": "user", "content": query}]
    )
    return response["message"]["content"]


def generate_response_from_llama_gemma2(query):
    response = ollama.chat(
        model="gemma:2b", messages=[{"role": "user", "content": query}]
    )
    return response["message"]["content"]


def extract_skills_with_gemini(text):
    """Uses Google Gemini AI to extract skills from a given text."""
    prompt = f"Extract only technical and professional skills from this text:\n{text}"

    try:
        response = generate_response_from_llama_gemini(prompt)
        skills_text = response.text if hasattr(response, "text") else response
        skills_list = [
            skill.strip()
            for skill in re.split(r",|\n|\*", skills_text)
            if skill.strip()
        ]

        return [
            skill.lower() for skill in skills_list
        ]  # Convert to lowercase for comparison
    except Exception as e:
        print("Error:", e)
        return []


def calculate_match_score_gemini(resume_skills, job_skills):
    """
    Uses Google Gemini AI to calculate how well a resume's skills match a job description.
    Returns a match score percentage and a list of missing skills.
    """

    prompt = f"""
    You are a professional ATS (Applicant Tracking System) evaluating a resume for a job application.
    
    - Compare the following **resume skills** with the **required job skills**.
    - Calculate a **match score (0-100%)** based on the overlap.
    - List **missing skills** (skills from job description not found in resume).
    
    ### **Resume Skills:**
    {", ".join(resume_skills)}

    ### **Job Description Skills:**
    {", ".join(job_skills)}

    ### **Response Format (JSON):**
    {{
      "match_score": (percentage of job skills found in resume, rounded to 2 decimal places),
      "missing_skills": ["List missing skills here"]
    }}

    Now, analyze and return the response in the given JSON format.
    """
    try:
        response = generate_response_from_llama_gemini(prompt)
        # match_data = json.loads(response.text if hasattr(response, "text") else response)
        response = response.strip("```json").strip("```")
        match_data = json.loads(response)
        print(match_data)
        return match_data
    except Exception as e:
        print("Error:", e)
        return []

def analyze_resume_with_gemini(resume_text, job_description):
    """Send resume and job description to Gemini Flash for evaluation."""
    prompt = f"""
    You are an expert HR assistant analyzing resumes for job applications.

    **Task:** Compare the following resume with the job description and provide insights.

    ### **Resume Content:**
    {resume_text[:4000]}  # Limiting input to 4000 characters for Gemini

    ### **Job Description:**
    {job_description}

    **Analyze the resume and provide feedback:**
    1. **Skills Match Score (0-100%)**
    2. **Missing Skills** (List of skills from the job description not found in the resume)
    3. **Strengths & Weaknesses** (What is good and what can be improved?)
    4. **Suggestions for Improvement** (Actionable advice)

    **Response Format (Strict JSON):**
    {{
      "match_score": (percentage match, rounded to 2 decimal places),
      "missing_skills": ["List of missing skills"],
      "strengths": "Short description of resume strengths",
      "weaknesses": "Short description of areas to improve",
      "suggestions": ["List of improvement suggestions"]
    }}
    """

    try:
        response = generate_response_from_llama_gemini(prompt)
        # match_data = json.loads(response.text if hasattr(response, "text") else response)
        response = response.strip("```json").strip("```")
        match_data = json.loads(response)
        return match_data
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON. Raw response:", response.text)
        return {"match_score": 0, "missing_skills": [], "strengths": "", "weaknesses": "", "suggestions": []}

    except Exception as e:
        print("Error:", str(e))
        return {"match_score": 0, "missing_skills": [], "strengths": "", "weaknesses": "", "suggestions": []}
    
def analyze_resume_format(resume_text,links):
    """Uses Gemini AI to check ATS compliance & formatting issues."""
    prompt = f"""
    You are an expert ATS resume analyzer. 
    Review the following resume text and detect ATS and formatting issues.

    **Resume Text:**
    {resume_text}  
    
    **Resume Links:**
    {links}  

    **Analysis Checklist:**
    - Is the resume **ATS-compatible**? (Can ATS parse it properly?)
    - Does it contain **tables, images, or multiple columns**? (These break ATS parsing)
    - Are **headers formatted correctly** (Education, Experience, Skills, etc.)?
    - Is the text **readable and spaced well**?
    - Does it use a **standard font** like Arial/Calibri?
    - Are bullet points correctly formatted?

    **Return JSON Response with:**
    {{
      "ats_compliant": (true/false),
      "format_issues": ["List of detected issues"],
      "missing_sections": ["List of missing sections"],
      "readability_score": (percentage from 0-100%),
      "suggestions": ["List of resume improvement tips"]
    }}
    """

    try:
        response = generate_response_from_llama_gemini(prompt)
        # if not response or not response.text:
        #     raise ValueError("Empty response from AI")
        response = response.strip("```json").strip("```")
        ats_data = json.loads(response)
        return ats_data

    except json.JSONDecodeError:
        print("Error: Failed to parse JSON. Raw response:", response.text)
        return {"ats_compliant": False, "format_issues": [], "missing_sections": [], "readability_score": 0, "suggestions": []}

def generate_ats_friendly_resume(resume_text,links):
    """Send resume text to Gemini AI for ATS optimization."""
    prompt =f"""
        Optimize the following resume to be **ATS-friendly** , **well-formatted** and **standout**.:
        - Ensure proper formatting while keeping the same Markdown structure.
        - Give proper space and alignment to the text as per the standard resume format.
        - Use similar ats friendly fonts and bullet points
        - Add missing sections if necessary (like Skills, Summary)
        - Improve readability for ATS scanners
        - Keep structure clean and concise
        - Match links with text: If a platform like GitHub, LinkedIn, or email is mentioned in the resume, use the corresponding link from the provided links.
        - Make sure it is well-structured and matches the standard resume format.
                
        Resume text:
        ```markdown
        {resume_text}
        
        Links:
        {links}
        
        Key improvements and explanations:
        .Provide a list of key improvements made to the resume.
        .Explain why these changes improve ATS compatibility and readability.
    """
    response = generate_response_from_llama_gemini(prompt)
    print(response)
    print(type(response))
    
    parts = response.replace("```markdown", "").split("---")
    markdown_resume = parts[0]
    explanation = parts[1]
    return markdown_resume, explanation
    


def generate_response_from_llama_gemini(query):
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model="gemini-2.0-flash", contents=query)
    return response.text
    # print(response)


def analyze_resume_gemini(text, links):
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
    # analyze_resume_gemini(
    #     "KALP MOTA\nMumbai, India | +91 9821625551 | LinkedIn | Email | Github\nBrief Introduction\nA highly skilled software engineer with 2+ years of experience specializing in Python, SQL, AWS, and platform\nintegration. Expertise in designing and developing solutions, working with APIs, and leveraging large language models\n(LLM) for innovative applications. Proven ability to streamline processes by automating workflows and integrating third-\nparty platforms using AWS, ServiceNow and Boto3. Seeking to apply technical expertise in a dynamic role to drive\ninnovation and efficiency.\nEducation College Graduation Year Percentage\nB.E. in Electronics and K.C. College of Engineering Management Studies June 2022 8.09 CGPA\nTelecommunication and Research\nDiploma in Computer Technology Shah and Anchor Kutchhi Polytechnic June 2019 76.59%\nSkills\n• Languages/Technologies: Python, SQL, AWS (Lambda, EC2, S3), Boto3, RESTful APIs, Docker, Flask, FastAPI, Django\n• Tools/Platforms: AWS CloudFormation, Git, Jenkins, PostgreSQL, MySQL, Informatica\n• Machine Learning: LLM (Large Language Models), TensorFlow, Keras, GPT\nProfessional Experience\nProduct Engineer\nLTIMindtree, Internal Project - Aspect | September 2022 – April 2023\n• Contributed to the internal Aspect project, developing innovative AI-driven solutions for document processing, including\ntext processors, named entity recognizers, image classification, and table extraction.\n• Worked on building models for City National Bank and Simon-Kucher & Partners, customizing NLP and machine learning\nsolutions to meet client requirements.\n• Trained, deployed, and demonstrated models tailored to client needs, utilizing Python and AWS to automate workflows and\nintegrate solutions.\n• Worked on features like document splitting, knowledge nugget extraction, sentiment analysis, and object identification for\nreal-time analysis.\nPython Developer\nTravelers (Client) - LTIMindtree | May 2023 – September 2023\n• Developed custom scripts to automate the conversion of insurance form data from Excel to JSON, streamlining form\nprocessing for various insurance types.\n• Utilized Python to automate the population of PDFs with client data, saving manual input time and increasing accuracy.\n• Collaborated with the team to integrate API solutions for automated data dumping into the client’s database, ensuring\nseamless data flow and synchronization.\n• Enhanced workflow efficiency by automating data extraction, reducing processing time and improving the accuracy of\ninsurance document handling.\nPython Backend Developer\nLTIMindtree (Aspect Project) | September 2023 – September 2024\n• Designed and developed backend solutions for the Aspect platform using Python, FastAPI, and Flask to create scalable,\nhigh-performance APIs.\n• Integrated LLM (Large Language Models), enhancing the platform’s capabilities with features like OCR, regex-based\nextraction, and document post-processing using Camelot for tabular data.\n• Implemented third-party app integration using async operations, improving platform functionality and responsiveness.\n• Implemented custom functionalities, including duplicate annotation detection and LLM model fine-tuning for text\nprocessing.\n• Contributed to the optimization of machine learning models, particularly for GPT and other language model applications,\nimproving accuracy.\n• Developed custom scripts to interact with REST APIs, retrieving only the client-required data while filtering out unnecessary\ninformation, improving data handling efficiency.\nPython Developer\nZendesk | October 2024 – Present\n• Working as a Python Developer responsible for backend systems and API development to improve customer service\nsolutions.\n• Developing scalable solutions using Python, Flask, and FastAPI while integrating third-party applications to extend product\nfunctionalities.\n• Leveraging AWS and SQL databases to enhance the architecture and implement efficient cloud solutions for data processing\nand storage.\n• Collaborating with cross-functional teams to continuously improve system performance, maintain code quality, and solve\ncomplex backend challenges.\nTraining Experience\nLTI (Training Period) | July 2022 - September 2022 (3 months)\n● Underwent 3 months of extensive training on Informatica to gain hands-on experience in data integration, transformation,\nand ETL processes.\n● Developed strong proficiency in data management and migration strategies, optimizing data flow across various systems.\n● Received training and completed assignments in multiple programming languages, including SQL, Python, and Java.\nProjects:\n➢ IBackPack (An AR Tour Guide App): My bachelor’s Final Year project that was developed for visitors to find exciting\nonline information during their travels. Unity was integrated for the augmented reality to interact with the user’s views. The\napp will display information such as location, street map, ratings, and key nearby locations related to. Users will have\nconsistent information about their target location.\nLink to Project: Final Year Project\n➢ Telegram Bot with Weather Forecast (Python): Developed a Telegram bot using the python-telegram-bot library,\nintegrated with OpenWeatherMap API for weather forecasting. The bot allows users to interact through various commands,\nincluding /start, message echoing, inline keyboard options, and sharing their location. Upon receiving the user’s location, the\nbot fetches weather data using the OWM API and returns detailed forecasts, such as temperature, status, and conditions for\nthe next few hours. This project showcases skills in bot development, API integration, and user interaction via a chatbot\ninterface.\nLink to Project: Project Link\n➢ Data Science Jupyter Notebook (Python, Pandas): A data analysis project where I performed various data science tasks\nusing 911.csv and USA Housing.csv datasets. The project involved data cleaning, exploratory data analysis (EDA), and\nvisualization using Pandas and Matplotlib to uncover insights from the data. Key tasks included handling missing values,\ndata transformations, and statistical analysis.\nLink to Project: Project Link\n➢ WhatsApp Bot (Flask, Twilio, MongoDB): Developed a WhatsApp-based chatbot for a bakery using Flask, Twilio API,\nand MongoDB to handle customer interactions. The bot allows users to place orders, check the bakery's working hours, and\nget contact details. Customers can choose from a list of cakes, provide their address, and receive a confirmation of their order.\nThe system also stores user interactions in a MongoDB database for future reference and order tracking. This project\ndemonstrates skills in building chatbots, integrating with WhatsApp using Twilio, and managing data with MongoDB.\nLink to Project: Project Link\n➢ GSM-based Wireless E-Noticeboard: My diploma final year project that aimed to create a wireless noticeboard system for\ndisplaying messages remotely. The project utilized Arduino UNO for controlling the process, a GSM module to receive SMS\nmessages from a mobile phone, and an LCD to display the content. The system automatically parsed SMS messages and\nextracted the main notice, which was then displayed on the board, providing an efficient way to update notices from any\nlocation.\nCertificates\n• Multidisciplinary Conference on Engineering Science & Technology (MCEST 2022) – Presented Ibackpack: An AR Tour\nGuide App.\n• Python certifications\n• Generative AI certifications\n• Internship and Training certificates\nFor a complete list of certifications, please visit: Link",
    #     [
    #         "https://www.linkedin.com/in/kalp-mota-357514148/",
    #         "mailto:kalpmota2000@gmail.com",
    #         "https://github.com/kalp12",
    #         "https://drive.google.com/drive/folders/1htCDvPKy_fM1bEyvUsXCrAxOCl9da8YR?usp=sharing",
    #         "https://github.com/kalp12/telegram_bot_python",
    #         "https://github.com/kalp12/Data_science_jupyternotebook/",
    #         "https://github.com/kalp12/automate-whatsapp",
    #         "https://drive.google.com/drive/folders/1kXpMRaRJBQnnH9iSDYo-2GQx5HiR5p34?usp=sharing",
    #     ],
    # )
    resume_text ="""
```markdown
**KALP MOTA**
Mumbai, India | +91 9821625551 | [LinkedIn](https://www.linkedin.com/in/kalp-mota-357514148/) | [kalpmota2000@gmail.com](mailto:kalpmota2000@gmail.com) | [GitHub](https://github.com/kalp12)

**Summary**

Highly skilled and motivated Software Engineer with 2+ years of experience in Python development, specializing in AWS, SQL, and platform integration. Proven ability to design, develop, and implement innovative solutions leveraging APIs and large language models (LLMs). Adept at automating workflows and integrating third-party platforms to streamline processes and enhance efficiency. Seeking a challenging role to apply technical expertise and drive innovation.

**Skills**

*   **Languages:** Python, SQL
*   **Cloud Technologies:** AWS (Lambda, EC2, S3, CloudFormation), Boto3
*   **Frameworks/Libraries:** Flask, FastAPI, Django, TensorFlow, Keras, GPT
*   **Databases:** PostgreSQL, MySQL
*   **Tools:** Git, Jenkins, Docker, Informatica
*   **Concepts/Practices:** RESTful APIs, LLM (Large Language Models), Machine Learning, OCR, Data Extraction, Sentiment Analysis, Asynchronous Operations

**Experience**

**Zendesk | Python Developer | October 2024 – Present**

*   Develop backend systems and APIs using Python, Flask, and FastAPI to improve customer service solutions.
*   Develop scalable solutions while integrating third-party applications to extend product functionalities.
*   Leverage AWS and SQL databases to enhance the architecture and implement efficient cloud solutions for data processing and storage.
*   Collaborate with cross-functional teams to continuously improve system performance, maintain code quality, and solve complex backend challenges.

**LTIMindtree (Aspect Project) | Python Backend Developer | September 2023 – September 2024**

*   Designed and developed backend solutions for the Aspect platform using Python, FastAPI, and Flask to create scalable, high-performance APIs.
*   Integrated LLM (Large Language Models), enhancing platform capabilities with features like OCR, regex-based extraction, and document post-processing using Camelot for tabular data.
*   Implemented third-party app integration using async operations, improving platform functionality and responsiveness.
*   Implemented custom functionalities, including duplicate annotation detection and LLM model fine-tuning for text processing.
*   Contributed to the optimization of machine learning models, particularly for GPT and other language model applications, improving accuracy.
*   Developed custom scripts to interact with REST APIs, retrieving only the client-required data while filtering out unnecessary information, improving data handling efficiency.

**LTIMindtree | Python Developer (Travelers Client) | May 2023 – September 2023**

*   Developed custom scripts to automate the conversion of insurance form data from Excel to JSON, streamlining form processing for various insurance types.
*   Utilized Python to automate the population of PDFs with client data, saving manual input time and increasing accuracy.
*   Collaborated with the team to integrate API solutions for automated data dumping into the client’s database, ensuring seamless data flow and synchronization.
*   Enhanced workflow efficiency by automating data extraction, reducing processing time and improving the accuracy of insurance document handling.

**LTIMindtree (Internal Project - Aspect) | Product Engineer | September 2022 – April 2023**

*   Contributed to the internal Aspect project, developing AI-driven solutions for document processing, including text processors, named entity recognizers, image classification, and table extraction.
*   Worked on building models for City National Bank and Simon-Kucher & Partners, customizing NLP and machine learning solutions to meet client requirements.
*   Trained, deployed, and demonstrated models tailored to client needs, utilizing Python and AWS to automate workflows and integrate solutions.
*   Worked on features like document splitting, knowledge nugget extraction, sentiment analysis, and object identification for real-time analysis.

**LTI (Training Period) | Trainee | July 2022 - September 2022 (3 months)**

*   Underwent 3 months of extensive training on Informatica to gain hands-on experience in data integration, transformation, and ETL processes.
*   Developed strong proficiency in data management and migration strategies, optimizing data flow across various systems.
*   Received training and completed assignments in multiple programming languages, including SQL, Python, and Java.

**Projects**

*   **IBackPack (An AR Tour Guide *   **WhatsApp Bot (Flask, Twilio, MongoDB):** Developed a WhatsApp-based chatbot for a bakery using Flask, Twilio API, and MongoDB to handle customer interactions. [Project Link](https://github.com/kalp12/automate-whatsapp)
*   **GSM-based Wireless E-Noticeboard:** Diploma final year project creating a wireless noticeboard system using Arduino UNO, GSM module, and LCD.

**Education**

**K.C. College of Engineering Management Studies and Research | B.E. in Electronics and Telecommunication | June 2022 | 8.09 CGPA**

**Shah and Anchor Kutchhi Polytechnic | Diploma in Computer Technology | June 2019 | 76.59%**

**Certifications**

*   Multidisciplinary Conference on Engineering Science & Technology (MCEST 2022) – Presented Ibackpack: An AR Tour Guide App
*   Python Certifications
*   Generative AI Certifications
*   Internship and Training Certificates
    [Complete List](https://drive.google.com/drive/folders/1kXpMRaRJBQnnH9iSDYo-2GQx5HiR5p34?usp=sharing)
```

Key improvements and explanations:

*   **ATS-Friendly Formatting:**  Uses standard section headings, bullet points, and a clean, simple structure that ATS systems can easily parse.  No tables or complex formatting.
*   **Simple Font:**  This is a Markdown format.  When converting this to a PDF or other formats, use a standard, easily readable font like Arial, Calibri, or Times New Roman.  Avoid fancy or script fonts.
*   **Contact Information:**  Clear and easy to find at the top.  Made the links clickable.
*   **Summary:** A concise summary highlighting key skills and experience, tailored to catch the recruiter's attention. This section is crucial for quickly conveying value to both ATS and human readers.
*   **Skills Section:** Added a separate and comprehensive skills section.  This is essential for ATS to identify relevant keywords.  Categorized skills for better readability.
*   **Experience Section:** Used action verbs at the beginning of each bullet point to describe accomplishments. Quantified achievements whenever possible (e.g., "saving manual input time and increasing accuracy").  Focused on results and impact.  Consistent formatting for each role.
*   **Projects Section:** Moved projects to their own section to highlight your practical experience. Included clear descriptions and links.  This shows initiative and real-world application of skills.
*   **Education Section:** Clear and concise information about your degrees and certifications.
*   **Certifications Section:** Added a certifications section to highlight all certifications.
*   **Keywords:** Incorporated relevant keywords throughout the resume based on the job description and your experience.
*   **Conciseness:**  Removed unnecessary words and phrases to keep the resume focused and easy to read.
*   **Links:** Made all provided URLs clickable.
*   **Chronological Order:** Maintained reverse chronological order (most recent first) in the Experience section, which is standard practice.
*   **No Pronouns:** Removed pronouns ("I," "me," "my") to create a more concise and professional tone.
*   **Format:** Save the resume as a `.docx` or `.pdf` for submitting to most employers.
*   **File Naming Convention:** Save it as `"FirstName_LastName_Resume.pdf"` or `"FirstName_LastName_Resume.docx"`.

This revised resume is much more likely to pass through an ATS successfully and make a positive impression on a human recruiter. Remember to tailor it further for each specific job application to maximize its effectiveness.
"""
    parts = resume_text.split("```")
    markdown_resume = parts[1].strip() # The resume is between the first and second set of triple backticks
    markdown_resume = markdown_resume.replace("markdown", "") # Remove any remaining backticks
    explanation = parts[2].strip()
    print("=== Markdown Resume ===")
    print(markdown_resume)

    print("\n=== Explanation ===")
    print(explanation)