"""
Seed script to populate the database with test data.
Run this after setting up the admin user.

Usage: python seed_data.py
"""
from datetime import date, timedelta
import random
from app import create_app
from models import db, Concert, Event, News, Company, Job


def seed_concerts():
    concerts = [
        {
            "artists": ["Kamelot", "Visions of Atlantis", "Frozen Crown"],
            "date": date(2026, 9, 25),
            "venue": "The Palladium",
            "city": "Worcester, MA",
            "source_url": "https://www.thepalladium.net/events",
            "sent": date(2026, 3, 11)
        },
        {
            "artists": ["Nightwish", "Beast in Black"],
            "date": date(2026, 10, 15),
            "venue": "Madison Square Garden",
            "city": "New York, NY",
            "source_url": "https://www.msg.com/events",
            "sent": None
        },
        {
            "artists": ["Epica", "Apocalyptica"],
            "date": date(2026, 11, 3),
            "venue": "House of Blues",
            "city": "Boston, MA",
            "source_url": "https://www.houseofblues.com/boston",
            "sent": None
        },
        {
            "artists": ["Sabaton", "Babymetal"],
            "date": date(2026, 8, 20),
            "venue": "Mohegan Sun Arena",
            "city": "Uncasville, CT",
            "source_url": "https://mohegansun.com/events",
            "sent": date(2026, 3, 15)
        },
        {
            "artists": ["Within Temptation", "Evanescence"],
            "date": date(2026, 12, 5),
            "venue": "TD Garden",
            "city": "Boston, MA",
            "source_url": "https://www.tdgarden.com/events",
            "sent": None
        },
    ]
    
    for data in concerts:
        concert = Concert(**data)
        db.session.add(concert)
    
    print(f"Added {len(concerts)} concerts")


def seed_events():
    events = [
        {
            "title": "Mattatuck Museum - Art of Feeding Community",
            "category": "exhibition",
            "summary": "An exploration of food culture and community through art. Features works from local and international artists examining how food brings people together.",
            "date": date(2026, 4, 15),
            "city": "Waterbury, CT",
            "source_url": "https://www.mattatuckmuseum.org/exhibitions",
            "sent": date(2026, 3, 11)
        },
        {
            "title": "New Haven Food Truck Festival",
            "category": "festival",
            "summary": "Annual gathering of the region's best food trucks. Live music, craft vendors, and over 50 food trucks serving cuisines from around the world.",
            "date": date(2026, 5, 22),
            "city": "New Haven, CT",
            "source_url": "https://www.nhfoodtruckfest.com",
            "sent": None
        },
        {
            "title": "Hartford Comic Con 2026",
            "category": "convention",
            "summary": "Connecticut's largest comic and pop culture convention. Celebrity guests, artist alley, cosplay contests, and panels.",
            "date": date(2026, 6, 14),
            "city": "Hartford, CT",
            "source_url": "https://www.hartfordcomiccon.com",
            "sent": None
        },
        {
            "title": "Yale Art Gallery - Modern Masters",
            "category": "exhibition",
            "summary": "A comprehensive look at 20th century modern art featuring works by Picasso, Warhol, and Basquiat from private collections.",
            "date": date(2026, 4, 1),
            "city": "New Haven, CT",
            "source_url": "https://artgallery.yale.edu",
            "sent": date(2026, 3, 10)
        },
        {
            "title": "Stamford Tech Summit",
            "category": "conference",
            "summary": "Annual technology conference bringing together startups, investors, and tech leaders from the tri-state area.",
            "date": date(2026, 7, 8),
            "city": "Stamford, CT",
            "source_url": "https://www.stamfordtechsummit.com",
            "sent": None
        },
    ]
    
    for data in events:
        event = Event(**data)
        db.session.add(event)
    
    print(f"Added {len(events)} events")


def seed_news():
    news_items = [
        {
            "title": "Pew Survey: Americans Are Using AI but Don't Trust It",
            "category": "AI & Tech",
            "date": date(2026, 3, 16),
            "sent": date(2026, 3, 16),
            "summary": "A new Pew Research survey reveals that while AI adoption is growing rapidly among Americans, trust in the technology remains low. The study found that 67% of respondents have used AI tools, but only 23% trust AI systems to make important decisions.",
            "source_url": "https://www.pewresearch.org/ai-trust-survey-2026",
            "confirmed": True,
            "tags": ["ai", "public-opinion", "pew-research", "trust", "survey"]
        },
        {
            "title": "OpenAI Announces GPT-5 with Enhanced Reasoning",
            "category": "AI & Tech",
            "date": date(2026, 3, 14),
            "sent": None,
            "summary": "OpenAI has unveiled GPT-5, featuring significantly improved reasoning capabilities and reduced hallucinations. The new model demonstrates near-human performance on complex logical tasks.",
            "source_url": "https://openai.com/blog/gpt-5",
            "confirmed": True,
            "tags": ["openai", "gpt-5", "ai", "llm", "reasoning"]
        },
        {
            "title": "Remote Work Trends Continue to Reshape Office Real Estate",
            "category": "Business",
            "date": date(2026, 3, 12),
            "sent": None,
            "summary": "Commercial real estate markets continue to adjust as hybrid work becomes the norm. Major cities report office vacancy rates above 20%, while suburban co-working spaces see increased demand.",
            "source_url": "https://www.wsj.com/real-estate/remote-work-office",
            "confirmed": True,
            "tags": ["remote-work", "real-estate", "business", "hybrid-work"]
        },
        {
            "title": "Connecticut Launches New Tech Innovation Hub",
            "category": "Local",
            "date": date(2026, 3, 10),
            "sent": None,
            "summary": "Governor announces $50 million investment in new technology innovation center in Hartford. The hub will focus on AI, biotech, and clean energy startups.",
            "source_url": "https://portal.ct.gov/tech-hub-announcement",
            "confirmed": True,
            "tags": ["connecticut", "tech", "startups", "investment", "local"]
        },
        {
            "title": "Study: Code Assistants Boost Developer Productivity by 40%",
            "category": "AI & Tech",
            "date": date(2026, 3, 8),
            "sent": None,
            "summary": "New research from MIT shows that developers using AI code assistants complete tasks 40% faster on average. The study also found improved code quality and reduced bugs.",
            "source_url": "https://news.mit.edu/code-assistant-study",
            "confirmed": False,
            "tags": ["ai", "coding", "productivity", "research", "developers"]
        },
        {
            "title": "Cybersecurity Threats Evolve with AI-Powered Attacks",
            "category": "Security",
            "date": date(2026, 3, 5),
            "sent": None,
            "summary": "Security researchers warn of increasing sophistication in cyber attacks leveraging AI. Phishing emails generated by AI are becoming nearly indistinguishable from legitimate communications.",
            "source_url": "https://www.wired.com/ai-cybersecurity-threats",
            "confirmed": True,
            "tags": ["cybersecurity", "ai", "phishing", "security", "threats"]
        },
    ]
    
    for data in news_items:
        news = News(**data)
        db.session.add(news)
    
    print(f"Added {len(news_items)} news articles")


def seed_companies():
    companies = [
        {
            "title": "Citrin Cooperman Advisors LLC",
            "location": "Stamford, CT, US",
            "research_date": date(2026, 3, 16),
            "url": "https://www.citrincooperman.com/",
            "research": """# Citrin Cooperman Advisors LLC

## Company Overview
Citrin Cooperman is a top 25 accounting and consulting firm providing a full range of audit, tax, and business advisory services.

## Key Facts
- **Founded**: 1979
- **Headquarters**: New York, NY
- **Employees**: 1,500+
- **Revenue**: $500M+ (estimated)

## Services
- Audit & Assurance
- Tax Services
- Business Advisory
- Technology Consulting
- Risk Advisory

## Culture & Values
The firm emphasizes work-life balance and professional development. Known for collaborative environment and mentorship programs.

## Recent News
- Expanded cloud consulting practice in 2025
- Opened new office in Stamford, CT
- Named one of "Best Places to Work" by Accounting Today

## Interview Process
1. Initial phone screen with HR
2. Technical interview with team lead
3. Case study presentation
4. Final interview with partners

## Glassdoor Rating
4.2/5 stars based on 200+ reviews
"""
        },
        {
            "title": "Synchrony Financial",
            "location": "Stamford, CT, US",
            "research_date": date(2026, 3, 14),
            "url": "https://www.synchrony.com/",
            "research": """# Synchrony Financial

## Company Overview
Synchrony is a premier consumer financial services company delivering customized financing programs across key industries.

## Key Facts
- **Founded**: 2003 (spun off from GE Capital in 2014)
- **Headquarters**: Stamford, CT
- **Employees**: 18,000+
- **Revenue**: $15B+ annually

## Business Lines
- Retail Card (store credit cards)
- Payment Solutions
- CareCredit (healthcare financing)
- Synchrony HOME

## Technology Stack
- AWS cloud infrastructure
- Kubernetes for container orchestration
- React/Node.js for web applications
- Python/Scala for data engineering

## Engineering Culture
- Agile/Scrum methodology
- Strong focus on automation and CI/CD
- Innovation labs and hackathons
- Remote-friendly policies

## Benefits
- Competitive salary + bonus
- 401k with 6% match
- Generous PTO
- Tuition reimbursement
"""
        },
        {
            "title": "Indeed",
            "location": "Stamford, CT, US",
            "research_date": date(2026, 3, 12),
            "url": "https://www.indeed.com/",
            "research": """# Indeed

## Company Overview
Indeed is the world's #1 job site, helping people find jobs and employers find great candidates.

## Key Facts
- **Founded**: 2004
- **Parent Company**: Recruit Holdings (acquired 2012)
- **Headquarters**: Austin, TX (with offices in Stamford, CT)
- **Employees**: 12,000+ globally

## Products
- Job Search Platform
- Indeed Resume
- Indeed Hiring Platform
- Indeed Assessments
- Indeed Interview

## Technology
- Massive scale: 250M+ unique visitors/month
- Machine learning for job matching
- Real-time data processing
- Microservices architecture

## Stamford Office
The Stamford office focuses on:
- Sales and account management
- Customer success
- Some engineering teams

## Interview Process
1. Recruiter screen
2. Technical phone interview
3. Virtual onsite (4-5 rounds)
4. Team matching
"""
        },
    ]
    
    for data in companies:
        company = Company(**data)
        db.session.add(company)
    
    db.session.flush()  # Get IDs for jobs
    print(f"Added {len(companies)} companies")
    return {c.title: c.id for c in Company.query.all()}


def seed_jobs(company_ids):
    jobs = [
        {
            "id": "abf9a49a-a8c8-4ec9-8b80-f56bbfb664a6",
            "title": "VP, Cloud Agile Lead",
            "company": "Citrin Cooperman Advisors LLC",
            "company_id": company_ids.get("Citrin Cooperman Advisors LLC"),
            "location": "Stamford, CT, US",
            "salary_min": 110000.0,
            "salary_max": 185000.0,
            "job_url": "https://www.indeed.com/viewjob?jk=24591f15286009a5",
            "site": "indeed",
            "date_posted": date(2026, 3, 16),
            "is_remote": True,
            "description": "The VP, Engineering Cloud Agile Lead will be responsible for coordination of multiple agile Scrum/Kanban Teams and Testing resources executing on Cloud migration initiatives.",
            "summary": "Lead cloud migration initiatives coordinating multiple agile teams.",
            "sent": date(2026, 3, 11)
        },
        {
            "id": "b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e",
            "title": "Senior Software Engineer - Python",
            "company": "Synchrony Financial",
            "company_id": company_ids.get("Synchrony Financial"),
            "location": "Stamford, CT, US",
            "salary_min": 130000.0,
            "salary_max": 170000.0,
            "job_url": "https://www.indeed.com/viewjob?jk=example123",
            "site": "indeed",
            "date_posted": date(2026, 3, 15),
            "is_remote": True,
            "description": "Join our data engineering team building scalable data pipelines and ML infrastructure. Work with Python, Spark, and AWS services.",
            "summary": "Data engineering role focused on Python, Spark, and AWS.",
            "sent": None
        },
        {
            "id": "c3d4e5f6-a7b8-9c0d-1e2f-3a4b5c6d7e8f",
            "title": "Frontend Developer - React",
            "company": "Indeed",
            "company_id": company_ids.get("Indeed"),
            "location": "Stamford, CT, US",
            "salary_min": 120000.0,
            "salary_max": 160000.0,
            "job_url": "https://www.indeed.com/viewjob?jk=example456",
            "site": "indeed",
            "date_posted": date(2026, 3, 14),
            "is_remote": False,
            "description": "Build user-facing features for the world's largest job site. Work with React, TypeScript, and modern frontend tooling.",
            "summary": "Frontend role building features for Indeed's job platform.",
            "sent": None
        },
        {
            "id": "d4e5f6a7-b8c9-0d1e-2f3a-4b5c6d7e8f9a",
            "title": "DevOps Engineer",
            "company": "Synchrony Financial",
            "company_id": company_ids.get("Synchrony Financial"),
            "location": "Remote, US",
            "salary_min": 125000.0,
            "salary_max": 165000.0,
            "job_url": "https://www.linkedin.com/jobs/view/example789",
            "site": "linkedin",
            "date_posted": date(2026, 3, 13),
            "is_remote": True,
            "description": "Manage and improve CI/CD pipelines, Kubernetes clusters, and cloud infrastructure. Experience with AWS, Terraform, and GitOps required.",
            "summary": "DevOps role managing cloud infrastructure and CI/CD.",
            "sent": None
        },
        {
            "id": "e5f6a7b8-c9d0-1e2f-3a4b-5c6d7e8f9a0b",
            "title": "Product Manager - AI Features",
            "company": "Indeed",
            "company_id": company_ids.get("Indeed"),
            "location": "Austin, TX / Remote",
            "salary_min": 140000.0,
            "salary_max": 190000.0,
            "job_url": "https://www.indeed.com/viewjob?jk=exampleabc",
            "site": "indeed",
            "date_posted": date(2026, 3, 10),
            "is_remote": True,
            "description": "Lead product strategy for AI-powered job matching features. Work closely with ML engineers and UX designers to improve job seeker experience.",
            "summary": "PM role leading AI feature development for job matching.",
            "sent": None
        },
    ]
    
    for data in jobs:
        job = Job(**data)
        db.session.add(job)
    
    print(f"Added {len(jobs)} jobs")


def main():
    app = create_app()
    
    with app.app_context():
        print("\n=== Seeding OpenClaw Concierge Database ===\n")
        
        # Check for existing data
        if Concert.query.count() > 0:
            response = input("Database already has data. Clear and reseed? (y/n): ").strip().lower()
            if response != 'y':
                print("Seed cancelled.")
                return
            
            # Clear existing data
            Job.query.delete()
            Company.query.delete()
            News.query.delete()
            Event.query.delete()
            Concert.query.delete()
            db.session.commit()
            print("Cleared existing data.\n")
        
        seed_concerts()
        seed_events()
        seed_news()
        company_ids = seed_companies()
        seed_jobs(company_ids)
        
        db.session.commit()
        print("\n=== Seeding complete! ===\n")


if __name__ == '__main__':
    main()
