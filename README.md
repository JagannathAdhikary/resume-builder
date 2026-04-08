# Resume Builder

An AI-powered resume tailoring and job search system. Tailor ATS-optimized resumes for specific job descriptions, search for jobs across multiple job boards, and match them against your profile — all powered by [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

## How It Works

1. You provide your career data in a structured YAML file (or import it from an existing resume)
2. You paste a job description — or search for jobs directly from LinkedIn, Indeed, and Google
3. Claude analyzes the JD, matches it against your experience, and generates a tailored one-page LaTeX resume optimized for ATS systems

The system mirrors exact JD keywords, reorders skills by relevance, rewrites bullets to emphasize matching experience, and verifies skill gaps with you before adding anything new.

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI installed and configured
- Python 3.10+ (for job search feature only)

## Quick Start

```bash
# Clone the repo
git clone git@github.com:JagannathAdhikary/resume-builder.git
cd resume-builder

# Set up your career data
# Option A: Import your existing resume
#   Open Claude Code and say: "Import resume"
#   Then provide your resume PDF path or paste the text
#
# Option B: Manual setup
cp master-resume.sample.yaml master-resume.yaml
# Edit master-resume.yaml with your details (follow the annotated comments)

# (Optional) Set up job search
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Then open Claude Code in this directory and start with any command below.

## Commands

| Command | What it does |
|---|---|
| `Tailor for [JD]` | Full tailoring workflow — analyze JD, match, verify skills, generate .tex |
| `Import resume` | Parse a PDF or text resume into `master-resume.yaml` |
| `Just the keywords` | Analyze a JD without generating a resume |
| `Update master` | Add new info to `master-resume.yaml` |
| `Regenerate` | Re-run generation with adjusted parameters |
| `Compare` | Side-by-side of original vs tailored bullets |
| `Search jobs` | Search for jobs on LinkedIn/Indeed/Google using JobSpy |
| `Match jobs` | Score and rank scraped jobs against your master resume |
| `Tailor for job #N` | Tailor resume for job #N from matched results |
| `Show job #N` | Show full details and score breakdown for a matched job |

## Job Search & Matching

Search for jobs across multiple job boards, match them against your profile, and tailor your resume for the best fits — all without leaving Claude Code.

### Supported Job Boards

- LinkedIn
- Indeed
- Google Jobs
- Glassdoor
- ZipRecruiter (US/Canada only)

### Setup

If you haven't already set up the virtual environment (see Quick Start):

```bash
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

> **Note:** Requires Python 3.10+. On macOS: `brew install python@3.12`. On Linux: use your package manager or [pyenv](https://github.com/pyenv/pyenv).

### Usage

In Claude Code, say:

```
"Search for backend engineer jobs in Bengaluru"
"Match jobs"             — rank results by profile fit
"Show job #3"            — see details and score breakdown
"Tailor for job #1"      — generate a tailored resume for the top match
```

### How Matching Works

Claude reads the scraped job descriptions and scores each one against your `master-resume.yaml` profile on five weighted criteria:

| Criterion | Weight | What it measures |
|-----------|--------|------------------|
| **Skill Match** | 35% | JD skills found in your master resume |
| **Tech Stack Alignment** | 25% | Overlap with your primary technologies |
| **Experience Level** | 20% | Seniority alignment |
| **Domain Relevance** | 10% | Industry/domain overlap |
| **Location Fit** | 10% | Remote/location compatibility |

### Manual Script Usage

You can also run the search script directly:

```bash
python3 scripts/search_jobs.py \
  --search-term "software engineer" \
  --location "Bengaluru, India" \
  --sites linkedin,indeed,google \
  --results 25 \
  --hours-old 72
```

Results are saved to `searches/` as both JSON and CSV. See `python3 scripts/search_jobs.py --help` for all options.

## Project Structure

```
resume-builder/
├── CLAUDE.md                    # AI workflow instructions
├── master-resume.sample.yaml    # Template — copy to master-resume.yaml
├── master-resume.yaml           # Your career data (gitignored)
├── templates/
│   └── resume-template.tex      # ATS-friendly LaTeX template
├── jobs/                        # Job descriptions (gitignored)
├── output/                      # Generated .tex files (gitignored)
├── imports/                     # Source resumes for import (gitignored)
├── scripts/
│   └── search_jobs.py           # Job search script (wraps python-jobspy)
├── searches/                    # Scraped job results (gitignored)
└── requirements.txt             # Python dependencies
```

## What Gets Generated

Each tailored resume is saved to `output/<company>-<role>.tex`. Upload this file to [Overleaf](https://www.overleaf.com/) and compile with pdfLaTeX to get a clean PDF.

After generation, you get an ATS match report showing:
- Keywords matched/missing
- Skills coverage
- Estimated ATS score
- Suggestions for improvement

## How Tailoring Works

1. **JD Analysis** — Extracts required skills, preferred skills, action verbs, and terminology
2. **Matching** — Maps JD requirements to your experience and projects
3. **Skill Gap Check** — Asks you to confirm/deny skills from the JD that aren't in your master data. Confirmed skills get saved permanently.
4. **Content Tailoring** — Rewrites bullets with JD keywords front-loaded, reorders skills, selects the most relevant projects
5. **LaTeX Generation** — Fills the ATS-safe template and saves the .tex file
6. **Match Report** — Shows how well your resume covers the JD

## ATS Optimization

The generated resumes follow ATS best practices:
- Single column layout, no graphics or icons
- Standard section headings (Experience, Projects, Education, Technical Skills, Achievements)
- Clean fonts (Computer Modern)
- Keyword mirroring from the job description
- Quantified impact using the XYZ formula
