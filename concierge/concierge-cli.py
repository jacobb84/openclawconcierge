#!/usr/bin/env python3
"""
OpenClaw Concierge CLI

A command-line interface for interacting with the Concierge API.
"""
import os
import sys
import json
from datetime import date
from typing import Optional, List
import typer
import httpx
from dotenv import load_dotenv

load_dotenv()

app = typer.Typer(
    name="concierge",
    help="OpenClaw Concierge CLI - Manage your personal dashboard data"
)

concerts_app = typer.Typer(help="Manage concerts")
events_app = typer.Typer(help="Manage events")
news_app = typer.Typer(help="Manage news")
careers_app = typer.Typer(help="Manage jobs and companies")

app.add_typer(concerts_app, name="concerts")
app.add_typer(events_app, name="events")
app.add_typer(news_app, name="news")
app.add_typer(careers_app, name="careers")


def get_config():
    api_url = os.environ.get("CONCIERGE_API_URL", "http://localhost:5000/api")
    api_key = os.environ.get("CONCIERGE_API_KEY")
    if not api_key:
        typer.echo("Error: CONCIERGE_API_KEY environment variable not set", err=True)
        raise typer.Exit(1)
    return api_url, api_key


def make_request(method: str, endpoint: str, data: dict = None) -> dict:
    api_url, api_key = get_config()
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    
    url = f"{api_url}{endpoint}"
    
    try:
        with httpx.Client() as client:
            if method == "GET":
                response = client.get(url, headers=headers)
            elif method == "POST":
                response = client.post(url, headers=headers, json=data)
            elif method == "PUT":
                response = client.put(url, headers=headers, json=data)
            elif method == "DELETE":
                response = client.delete(url, headers=headers)
            else:
                raise ValueError(f"Unknown method: {method}")
        
        if response.status_code == 204:
            return {"message": "No content"}
        
        if response.status_code >= 400:
            typer.echo(f"Error {response.status_code}: {response.text}", err=True)
            raise typer.Exit(1)
        
        return response.json()
    except httpx.RequestError as e:
        typer.echo(f"Request error: {e}", err=True)
        raise typer.Exit(1)


def print_json(data: dict):
    typer.echo(json.dumps(data, indent=2))


# ============== CONCERTS ==============

@concerts_app.command("add")
def add_concert(
    artists: str = typer.Option(..., "--artists", "-a", help="Comma-separated list of artists"),
    concert_date: str = typer.Option(..., "--date", "-d", help="Concert date (YYYY-MM-DD)"),
    venue: str = typer.Option(..., "--venue", "-v", help="Venue name"),
    city: str = typer.Option(..., "--city", "-c", help="City"),
    source_url: Optional[str] = typer.Option(None, "--url", "-u", help="Source URL")
):
    """Add a new concert to the dashboard."""
    data = {
        "artists": [a.strip() for a in artists.split(",")],
        "date": concert_date,
        "venue": venue,
        "city": city
    }
    if source_url:
        data["source_url"] = source_url
    
    result = make_request("POST", "/concerts", data)
    typer.echo(f"Concert added with ID: {result.get('id')}")
    print_json(result)


@concerts_app.command("prune")
def prune_concerts():
    """Delete all past concerts."""
    result = make_request("POST", "/concerts/prune")
    typer.echo(result.get("message", "Done"))


# ============== EVENTS ==============

@events_app.command("add")
def add_event(
    title: str = typer.Option(..., "--title", "-t", help="Event title"),
    event_date: str = typer.Option(..., "--date", "-d", help="Event date (YYYY-MM-DD)"),
    city: str = typer.Option(..., "--city", "-c", help="City"),
    category: Optional[str] = typer.Option(None, "--category", help="Event category"),
    summary: Optional[str] = typer.Option(None, "--summary", "-s", help="Event summary"),
    source_url: Optional[str] = typer.Option(None, "--url", "-u", help="Source URL")
):
    """Add a new event to the dashboard."""
    data = {
        "title": title,
        "date": event_date,
        "city": city
    }
    if category:
        data["category"] = category
    if summary:
        data["summary"] = summary
    if source_url:
        data["source_url"] = source_url
    
    result = make_request("POST", "/events", data)
    typer.echo(f"Event added with ID: {result.get('id')}")
    print_json(result)


@events_app.command("prune")
def prune_events():
    """Delete all past events."""
    result = make_request("POST", "/events/prune")
    typer.echo(result.get("message", "Done"))


# ============== NEWS ==============

@news_app.command("add")
def add_news(
    title: str = typer.Option(..., "--title", "-t", help="Article title"),
    news_date: Optional[str] = typer.Option(None, "--date", "-d", help="Article date (YYYY-MM-DD)"),
    category: Optional[str] = typer.Option(None, "--category", help="News category"),
    summary: Optional[str] = typer.Option(None, "--summary", "-s", help="Article summary"),
    source_url: Optional[str] = typer.Option(None, "--url", "-u", help="Source URL"),
    confirmed: bool = typer.Option(False, "--confirmed", help="Mark as fact-checked"),
    tags: Optional[str] = typer.Option(None, "--tags", help="Comma-separated tags")
):
    """Add a new news article to the dashboard."""
    data = {
        "title": title,
        "date": news_date or date.today().isoformat(),
        "confirmed": confirmed
    }
    if category:
        data["category"] = category
    if summary:
        data["summary"] = summary
    if source_url:
        data["source_url"] = source_url
    if tags:
        data["tags"] = [t.strip() for t in tags.split(",")]
    
    result = make_request("POST", "/news", data)
    typer.echo(f"News added with ID: {result.get('id')}")
    print_json(result)


@news_app.command("pop")
def pop_news():
    """Get and mark the next unsent news article as sent."""
    result = make_request("POST", "/news/pop")
    if result.get("message") == "No content":
        typer.echo("No unsent news available")
    else:
        print_json(result)


@news_app.command("prune")
def prune_news():
    """Mark all unsent news as sent."""
    result = make_request("POST", "/news/prune")
    typer.echo(result.get("message", "Done"))


# ============== CAREERS ==============

@careers_app.command("add-job")
def add_job(
    title: str = typer.Option(..., "--title", "-t", help="Job title"),
    company: str = typer.Option(..., "--company", "-c", help="Company name"),
    location: Optional[str] = typer.Option(None, "--location", "-l", help="Job location"),
    salary_min: Optional[float] = typer.Option(None, "--salary-min", help="Minimum salary"),
    salary_max: Optional[float] = typer.Option(None, "--salary-max", help="Maximum salary"),
    job_url: Optional[str] = typer.Option(None, "--url", "-u", help="Job listing URL"),
    site: Optional[str] = typer.Option(None, "--site", help="Job site (linkedin, indeed, etc.)"),
    posted_date: Optional[str] = typer.Option(None, "--date", "-d", help="Date posted (YYYY-MM-DD)"),
    remote: bool = typer.Option(False, "--remote", "-r", help="Is remote job"),
    summary: Optional[str] = typer.Option(None, "--summary", "-s", help="Job summary")
):
    """Add a new job listing to the dashboard."""
    data = {
        "title": title,
        "company": company,
        "is_remote": remote
    }
    if location:
        data["location"] = location
    if salary_min:
        data["salary_min"] = salary_min
    if salary_max:
        data["salary_max"] = salary_max
    if job_url:
        data["job_url"] = job_url
    if site:
        data["site"] = site
    if posted_date:
        data["date_posted"] = posted_date
    if summary:
        data["summary"] = summary
    
    result = make_request("POST", "/careers/jobs", data)
    typer.echo(f"Job added with ID: {result.get('id')}")
    print_json(result)


@careers_app.command("add-company")
def add_company(
    title: str = typer.Option(..., "--title", "-t", help="Company name"),
    location: Optional[str] = typer.Option(None, "--location", "-l", help="Company location"),
    url: Optional[str] = typer.Option(None, "--url", "-u", help="Company website"),
    research_date: Optional[str] = typer.Option(None, "--date", "-d", help="Research date (YYYY-MM-DD)"),
    research: Optional[str] = typer.Option(None, "--research", "-r", help="Research notes (markdown)")
):
    """Add company research to the dashboard."""
    data = {
        "title": title
    }
    if location:
        data["location"] = location
    if url:
        data["url"] = url
    if research_date:
        data["research_date"] = research_date
    if research:
        data["research"] = research
    
    result = make_request("POST", "/careers/companies", data)
    typer.echo(f"Company added with ID: {result.get('id')}")
    print_json(result)


@careers_app.command("pop-job")
def pop_job():
    """Get and mark the next unsent job as sent."""
    result = make_request("POST", "/careers/jobs/pop")
    if result.get("message") == "No content":
        typer.echo("No unsent jobs available")
    else:
        print_json(result)


# ============== MAIN ==============

@app.callback()
def main():
    """OpenClaw Concierge CLI - Manage your personal dashboard data."""
    pass


if __name__ == "__main__":
    app()
