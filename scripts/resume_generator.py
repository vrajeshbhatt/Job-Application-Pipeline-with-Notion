"""
Resume Generator Module - Tailored Application Package Creation

Generates customized resume and cover letter for each job application.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict
from datetime import datetime


# Candidate profile (customize this with your details)
CANDIDATE_PROFILE = {
    "name": "Vrajesh Bhatt",
    "email": "vrajesh.bhatt@outlook.com",
    "phone": "[Your Phone Number]",
    "location": "Halifax, Nova Scotia",
    "linkedin": "linkedin.com/in/vrajeshbhatt",
    "github": "github.com/vrajeshbhatt",
    
    "summary": (
        "Results-driven Computer Engineering graduate with expertise in AI/Data Science. "
        "Recognized as Employee of the Quarter at Moah Appliances and finalist at Gujarat "
        "Industrial Hackathon. Proficient in Python, SQL, Power BI, and data analysis. "
        "Seeking entry-level Data Analyst role to leverage technical skills."
    ),
    
    "skills": [
        "Python", "SQL", "Power BI", "Tableau", "Excel", 
        "Data Analysis", "Machine Learning", "RPA", "n8n",
        "Statistical Analysis", "Data Visualization", "Process Automation"
    ],
    
    "experience": [
        {
            "title": "Data Analyst",
            "company": "Moah Appliances",
            "location": "[Location]",
            "dates": "[Dates]",
            "achievements": [
                "Analyzed operational data to identify efficiency improvements",
                "Developed automated dashboards using Power BI for executive reporting",
                "Created Python scripts for data processing and validation",
                "Recognized as Employee of the Quarter for data-driven insights"
            ]
        }
    ],
    
    "education": {
        "degree": "Bachelor of Computer Engineering",
        "specialization": "AI & Data Science",
        "school": "[University Name]",
        "graduation": "[Year]"
    },
    
    "achievements": [
        "Employee of the Quarter - Moah Appliances",
        "Finalist - Gujarat Industrial Hackathon",
        "Academic Excellence in Data Structures & Algorithms"
    ]
}


def load_template(template_path: str) -> str:
    """Load HTML template from file."""
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def customize_resume(template: str, job: Dict, profile: Dict) -> str:
    """
    Customize resume template for specific job.
    
    Args:
        template: Base HTML resume template
        job: Job dictionary with title, company, description
        profile: Candidate profile dictionary
        
    Returns:
        Customized HTML resume
    """
    customized = template
    
    # Basic substitutions
    customized = customized.replace("{{name}}", profile["name"])
    customized = customized.replace("{{email}}", profile["email"])
    customized = customized.replace("{{phone}}", profile["phone"])
    customized = customized.replace("{{location}}", profile["location"])
    customized = customized.replace("{{linkedin}}", profile["linkedin"])
    
    # Customize summary for job
    job_title = job.get("title", "Data Analyst")
    company = job.get("company", "the company")
    
    tailored_summary = (
        f"{profile['summary']} "
        f"Passionate about applying analytical skills to {job_title.lower()} roles "
        f"and contributing to {company}'s data-driven decision making."
    )
    customized = customized.replace("{{summary}}", tailored_summary)
    
    # Highlight relevant skills based on job description
    job_desc = job.get("description", "").lower()
    relevant_skills = []
    
    skill_keywords = {
        "python": ["python", "pandas", "numpy"],
        "sql": ["sql", "database", "mysql", "postgresql"],
        "power bi": ["power bi", "powerbi", "tableau", "visualization"],
        "excel": ["excel", "spreadsheet"],
        "rpa": ["automation", "rpa", "workflow"],
        "machine learning": ["machine learning", "ml", "ai"]
    }
    
    for skill, keywords in skill_keywords.items():
        if any(kw in job_desc for kw in keywords):
            relevant_skills.append(skill.title())
    
    # Add remaining skills
    for skill in profile["skills"]:
        if skill.lower() not in [s.lower() for s in relevant_skills]:
            relevant_skills.append(skill)
    
    skills_html = " • ".join(relevant_skills[:10])  # Top 10 skills
    customized = customized.replace("{{skills}}", skills_html)
    
    return customized


def customize_cover_letter(template: str, job: Dict, profile: Dict) -> str:
    """
    Customize cover letter template for specific job.
    
    Args:
        template: Base HTML cover letter template
        job: Job dictionary with title, company, description
        profile: Candidate profile dictionary
        
    Returns:
        Customized HTML cover letter
    """
    customized = template
    
    # Basic substitutions
    customized = customized.replace("{{candidate_name}}", profile["name"])
    customized = customized.replace("{{email}}", profile["email"])
    customized = customized.replace("{{phone}}", profile["phone"])
    customized = customized.replace("{{location}}", profile["location"])
    customized = customized.replace("{{linkedin}}", profile["linkedin"])
    
    # Job-specific substitutions
    customized = customized.replace("{{job_title}}", job.get("title", "Data Analyst"))
    customized = customized.replace("{{company_name}}", job.get("company", "the company"))
    customized = customized.replace("{{company_location}}", job.get("location", "Halifax, NS"))
    
    # Date
    today = datetime.now().strftime("%B %d, %Y")
    customized = customized.replace("{{date}}", today)
    
    # Customize opening paragraph
    job_desc = job.get("description", "").lower()
    
    # Extract key requirements
    key_skills = []
    if "python" in job_desc:
        key_skills.append("Python programming")
    if "sql" in job_desc:
        key_skills.append("SQL database management")
    if "power bi" in job_desc or "tableau" in job_desc:
        key_skills.append("data visualization")
    if "statistics" in job_desc or "statistical" in job_desc:
        key_skills.append("statistical analysis")
    
    skills_mention = ", ".join(key_skills[:3]) if key_skills else "data analysis and visualization"
    
    opening = (
        f"I am writing to express my strong interest in the {job.get('title', 'Data Analyst')} "
        f"position at {job.get('company', 'your company')}. As a Computer Engineering graduate "
        f"with expertise in {skills_mention}, I am excited about the opportunity to contribute "
        f"to your data-driven initiatives."
    )
    customized = customized.replace("{{opening_paragraph}}", opening)
    
    # Company-specific paragraph
    company_para = (
        f"What draws me to {job.get('company', 'your organization')} is your commitment to "
        f"leveraging data for informed decision-making. I am particularly impressed by "
        f"your innovative approach and would welcome the opportunity to contribute my "
        f"skills in {skills_mention} to support your team's goals."
    )
    customized = customized.replace("{{company_paragraph}}", company_para)
    
    return customized


def generate_application_package(job: Dict, template_dir: str, output_dir: str) -> str:
    """
    Generate complete application package for a job.
    
    Args:
        job: Job dictionary
        template_dir: Directory containing templates
        output_dir: Directory to save generated files
        
    Returns:
        Path to generated package directory
    """
    # Create safe directory name
    company = re.sub(r'[^\w\s-]', '', job.get("company", "Unknown")).strip()
    role = re.sub(r'[^\w\s-]', '', job.get("title", "Role")).strip()[:30]
    
    package_name = f"{company}_{role}".replace(" ", "_").replace("-", "_")
    package_dir = os.path.join(output_dir, package_name)
    
    # Create directory
    Path(package_dir).mkdir(parents=True, exist_ok=True)
    
    # Load templates
    resume_template = load_template(os.path.join(template_dir, "resume_template.html"))
    cover_template = load_template(os.path.join(template_dir, "cover_letter_template.html"))
    
    # Generate customized versions
    customized_resume = customize_resume(resume_template, job, CANDIDATE_PROFILE)
    customized_cover = customize_cover_letter(cover_template, job, CANDIDATE_PROFILE)
    
    # Save files
    resume_path = os.path.join(package_dir, "resume.html")
    cover_path = os.path.join(package_dir, "cover_letter.html")
    
    with open(resume_path, 'w', encoding='utf-8') as f:
        f.write(customized_resume)
    
    with open(cover_path, 'w', encoding='utf-8') as f:
        f.write(customized_cover)
    
    # Save job details
    details = {
        "company": job.get("company", "Unknown"),
        "role": job.get("title", "Unknown"),
        "location": job.get("location", "Unknown"),
        "url": job.get("url", ""),
        "match_score": job.get("match_score", 0),
        "generated_at": datetime.now().isoformat()
    }
    
    details_path = os.path.join(package_dir, "job_details.json")
    with open(details_path, 'w') as f:
        json.dump(details, f, indent=2)
    
    print(f"  ✅ Generated: {package_name}/")
    return package_dir


if __name__ == "__main__":
    # Test generation
    test_job = {
        "title": "Data Analyst",
        "company": "Test Company",
        "location": "Halifax, NS",
        "description": "Looking for Python and SQL skills. Power BI experience preferred.",
        "url": "https://example.com/job",
        "match_score": 85
    }
    
    result = generate_application_package(
        job=test_job,
        template_dir="../templates",
        output_dir="../applications"
    )
    print(f"Generated package at: {result}")
