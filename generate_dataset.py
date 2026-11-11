import os


OUTPUT_DIR = "resumes"


candidates = [
    {
        "name": "Alex Johnson",
        "role": "Senior Python Developer",
        "years": 7,
        "skills": ["Python", "FastAPI", "Django", "SQL", "AWS", "Docker", "Git", "CI/CD"],
        "company": "CloudTech Solutions",
        "education": "Bachelor of Technology in Computer Science"
    },
    {
        "name": "Emma Davis",
        "role": "Python Backend Developer",
        "years": 5,
        "skills": ["Python", "FastAPI", "Flask", "SQL", "AWS", "Docker", "Git"],
        "company": "Digital Systems",
        "education": "Bachelor of Science in Computer Science"
    },
    {
        "name": "Liam Anderson",
        "role": "Java Developer",
        "years": 6,
        "skills": ["Java", "Spring Boot", "SQL", "AWS", "Docker", "Git"],
        "company": "Enterprise Apps",
        "education": "Bachelor of Engineering in Information Technology"
    },
    {
        "name": "Olivia Thomas",
        "role": "Machine Learning Engineer",
        "years": 6,
        "skills": ["Python", "Machine Learning", "TensorFlow", "PyTorch", "SQL", "AWS", "Docker"],
        "company": "AI Innovations",
        "education": "Master of Science in Artificial Intelligence"
    },
    {
        "name": "Noah Jackson",
        "role": "DevOps Engineer",
        "years": 8,
        "skills": ["AWS", "Docker", "Kubernetes", "Terraform", "Linux", "Git", "CI/CD", "Python"],
        "company": "Cloud Infrastructure Ltd",
        "education": "Bachelor of Technology in Information Technology"
    },
    {
        "name": "Ava White",
        "role": "Data Scientist",
        "years": 5,
        "skills": ["Python", "SQL", "Machine Learning", "Pandas", "TensorFlow", "AWS"],
        "company": "Data Analytics Corp",
        "education": "Master of Science in Data Science"
    },
    {
        "name": "William Harris",
        "role": "Data Engineer",
        "years": 7,
        "skills": ["Python", "SQL", "AWS", "Docker", "Spark", "ETL", "Git"],
        "company": "Big Data Systems",
        "education": "Bachelor of Engineering in Computer Science"
    },
    {
        "name": "Sophia Martin",
        "role": "Frontend Developer",
        "years": 4,
        "skills": ["JavaScript", "React", "HTML", "CSS", "Git"],
        "company": "Web Experiences",
        "education": "Bachelor of Science in Computer Science"
    },
    {
        "name": "James Thompson",
        "role": "Backend Developer",
        "years": 6,
        "skills": ["Python", "Django", "SQL", "Docker", "AWS", "Git"],
        "company": "Backend Systems",
        "education": "Bachelor of Technology in Computer Science"
    },
    {
        "name": "Isabella Garcia",
        "role": "Full Stack Developer",
        "years": 5,
        "skills": ["Python", "JavaScript", "React", "Django", "SQL", "Docker", "AWS"],
        "company": "FullStack Labs",
        "education": "Bachelor of Engineering in Software Engineering"
    },
    {
        "name": "Benjamin Martinez",
        "role": "Cloud Engineer",
        "years": 7,
        "skills": ["AWS", "Azure", "Docker", "Kubernetes", "Terraform", "Python", "Linux"],
        "company": "Cloud Services Inc",
        "education": "Bachelor of Technology in Information Technology"
    },
    {
        "name": "Mia Robinson",
        "role": "QA Automation Engineer",
        "years": 5,
        "skills": ["Python", "Selenium", "PyTest", "Git", "CI/CD", "SQL"],
        "company": "Quality Systems",
        "education": "Bachelor of Science in Computer Science"
    },
    {
        "name": "Lucas Clark",
        "role": "Java Backend Developer",
        "years": 7,
        "skills": ["Java", "Spring Boot", "SQL", "Docker", "Kubernetes", "AWS"],
        "company": "Enterprise Software",
        "education": "Bachelor of Engineering in Computer Science"
    },
    {
        "name": "Charlotte Rodriguez",
        "role": "Business Analyst",
        "years": 6,
        "skills": ["SQL", "Excel", "Power BI", "Agile", "Jira"],
        "company": "Business Consulting Group",
        "education": "Master of Business Administration"
    },
    {
        "name": "Henry Lewis",
        "role": "Cybersecurity Engineer",
        "years": 8,
        "skills": ["Python", "Linux", "AWS", "Network Security", "SIEM", "Git"],
        "company": "Secure Systems",
        "education": "Bachelor of Science in Cybersecurity"
    },
    {
        "name": "Amelia Lee",
        "role": "Database Engineer",
        "years": 6,
        "skills": ["SQL", "PostgreSQL", "MySQL", "AWS", "Python", "Linux"],
        "company": "Database Solutions",
        "education": "Bachelor of Technology in Computer Science"
    },
    {
        "name": "Alexander Walker",
        "role": "Python Developer",
        "years": 4,
        "skills": ["Python", "FastAPI", "SQL", "Docker", "Git"],
        "company": "Software Works",
        "education": "Bachelor of Science in Information Technology"
    },
    {
        "name": "Harper Hall",
        "role": "Machine Learning Engineer",
        "years": 7,
        "skills": ["Python", "Machine Learning", "PyTorch", "TensorFlow", "AWS", "Docker", "SQL"],
        "company": "Machine Intelligence Labs",
        "education": "Master of Science in Machine Learning"
    },
    {
        "name": "Daniel Allen",
        "role": "DevOps Engineer",
        "years": 6,
        "skills": ["AWS", "Docker", "Kubernetes", "CI/CD", "Terraform", "Python", "Git"],
        "company": "DevOps Systems",
        "education": "Bachelor of Engineering in Information Technology"
    },
    {
        "name": "Evelyn Young",
        "role": "Data Analyst",
        "years": 4,
        "skills": ["Python", "SQL", "Pandas", "Power BI", "Excel"],
        "company": "Analytics Solutions",
        "education": "Bachelor of Science in Statistics"
    },
    {
        "name": "Matthew Hernandez",
        "role": "Senior Python Developer",
        "years": 9,
        "skills": ["Python", "FastAPI", "Django", "SQL", "AWS", "Docker", "Kubernetes", "Git"],
        "company": "Platform Engineering",
        "education": "Bachelor of Engineering in Computer Science"
    },
    {
        "name": "Abigail King",
        "role": "Cloud Developer",
        "years": 5,
        "skills": ["Python", "AWS", "Docker", "SQL", "Git", "Terraform"],
        "company": "Cloud Applications",
        "education": "Bachelor of Technology in Computer Science"
    },
    {
        "name": "Sebastian Wright",
        "role": "Software Engineer",
        "years": 3,
        "skills": ["Python", "Flask", "SQL", "Git", "Docker"],
        "company": "Software Factory",
        "education": "Bachelor of Science in Computer Science"
    },
    {
        "name": "Emily Lopez",
        "role": "AI Engineer",
        "years": 6,
        "skills": ["Python", "Machine Learning", "TensorFlow", "FastAPI", "Docker", "AWS"],
        "company": "AI Systems",
        "education": "Master of Science in Artificial Intelligence"
    },
    {
        "name": "Jack Hill",
        "role": "Platform Engineer",
        "years": 7,
        "skills": ["Python", "AWS", "Docker", "Kubernetes", "Linux", "CI/CD", "Git"],
        "company": "Platform Cloud",
        "education": "Bachelor of Technology in Information Technology"
    },
]


def create_resume(candidate):
    skills_text = "\n".join(candidate["skills"])

    start_year = 2026 - candidate["years"]

    return f"""{candidate["name"]}

PROFESSIONAL SUMMARY
{candidate["role"]} with {candidate["years"]} years of experience delivering software and technology solutions.

SKILLS
{skills_text}

EXPERIENCE

{candidate["role"]}
{candidate["company"]}
{start_year} - Present

Worked on production projects as a {candidate["role"]}.
Designed and implemented solutions using {", ".join(candidate["skills"][:4])}.
Collaborated with engineering teams to deliver reliable software.
Applied {", ".join(candidate["skills"][4:])} in project environments.

EDUCATION

{candidate["education"]}
Example University
{start_year - 4} - {start_year}
"""


def filename_from_name(name):
    return name.lower().replace(" ", "_") + ".txt"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for candidate in candidates:
        filename = filename_from_name(candidate["name"])
        filepath = os.path.join(OUTPUT_DIR, filename)

        resume_text = create_resume(candidate)

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(resume_text)

        print(f"Created: {filepath}")

    print()
    print(f"Generated {len(candidates)} synthetic resumes.")


if __name__ == "__main__":
    main()