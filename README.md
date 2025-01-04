# Code Analysis Tool

## Description
A web application for automated program code analysis, designed to optimize the code review process in large companies.

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
