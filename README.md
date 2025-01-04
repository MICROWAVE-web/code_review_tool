# Code Analysis Tool
![image](https://github.com/user-attachments/assets/977380d1-cec5-4763-ae26-e09665009880)

## Description
A web application for automated program code analysis, designed to optimize the code review process in large companies.

![image](https://github.com/user-attachments/assets/ac4cf7ea-0035-44d9-8b9b-86220d59bbc8)

## Features
- Upload code through a text field
- Upload individual code files
- Upload code archives
- Support for GitHub repository links
- Generate PDF reports with code analysis

## Installation
1. Clone the repository  
2. Create a virtual environment  
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```

3. Install dependencies  
```bash
pip install -r requirements.txt
```

4. Run migrations  
```bash
python manage.py migrate
```

5. Start the server  
```bash
python manage.py runserver
```

## Technologies
- Django  
- Markdown  
- ReportLab  
- PyGithub  
