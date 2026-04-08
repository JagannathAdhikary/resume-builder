#!/usr/bin/env python3
"""Thin wrapper around python-jobspy for the resume-builder project."""

import argparse
import sys
from datetime import datetime
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Search jobs using JobSpy")
    parser.add_argument("--search-term", required=True, help="Job title or keyword")
    parser.add_argument("--location", default="", help="Location (e.g., 'Bengaluru, India')")
    parser.add_argument("--sites", default="linkedin,indeed,google",
                        help="Comma-separated job sites (linkedin,indeed,google,glassdoor,zip_recruiter)")
    parser.add_argument("--results", type=int, default=25, help="Number of results per site (default: 25)")
    parser.add_argument("--hours-old", type=int, default=72, help="Max age of postings in hours (default: 72)")
    parser.add_argument("--job-type", choices=["fulltime", "parttime", "internship", "contract"],
                        help="Filter by job type")
    parser.add_argument("--remote", action="store_true", help="Filter for remote jobs only")
    parser.add_argument("--country", default="USA", help="Country for Indeed/Glassdoor (default: USA)")
    parser.add_argument("--output-name", help="Output filename prefix (default: derived from search term)")
    parser.add_argument("--linkedin-fetch-description", action="store_true",
                        help="Fetch full descriptions from LinkedIn (slower)")

    args = parser.parse_args()

    if sys.version_info < (3, 10):
        print(f"Error: Python 3.10+ required. Found: {sys.version}", file=sys.stderr)
        print("Install via: brew install python@3.12  OR  pyenv install 3.12", file=sys.stderr)
        sys.exit(1)

    from jobspy import scrape_jobs

    kwargs = {
        "site_name": [s.strip() for s in args.sites.split(",")],
        "search_term": args.search_term,
        "results_wanted": args.results,
        "hours_old": args.hours_old,
        "description_format": "markdown",
    }
    if args.location:
        kwargs["location"] = args.location
    if args.job_type:
        kwargs["job_type"] = args.job_type
    if args.remote:
        kwargs["is_remote"] = True
    if args.country:
        kwargs["country_indeed"] = args.country
    if args.linkedin_fetch_description:
        kwargs["linkedin_fetch_description"] = True

    print(f"Searching for '{args.search_term}' on {args.sites}...")
    jobs_df = scrape_jobs(**kwargs)

    if jobs_df.empty:
        print("No jobs found. Try broadening your search or changing sites.")
        sys.exit(0)

    # Prepare output path
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    name = args.output_name or args.search_term.replace(" ", "-").lower()[:30]
    output_dir = Path(__file__).resolve().parent.parent / "searches"
    output_dir.mkdir(exist_ok=True)

    json_path = output_dir / f"{name}_{timestamp}.json"
    csv_path = output_dir / f"{name}_{timestamp}.csv"

    # Clean data for JSON serialization
    jobs_df = jobs_df.fillna("")
    for col in jobs_df.select_dtypes(include=["datetime64", "datetimetz"]).columns:
        jobs_df[col] = jobs_df[col].astype(str)

    jobs_df.to_json(json_path, orient="records", indent=2, force_ascii=False)
    jobs_df.to_csv(csv_path, index=False)

    print(f"Found {len(jobs_df)} jobs. Saved to:")
    print(f"  JSON: {json_path}")
    print(f"  CSV:  {csv_path}")


if __name__ == "__main__":
    main()
