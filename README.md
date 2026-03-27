# Resume Builder

An AI-powered resume tailoring system that generates ATS-optimized, Overleaf-compatible LaTeX resumes. Powered by [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

## How It Works

1. You provide your career data in a structured YAML file (or import it from an existing resume)
2. You paste a job description
3. Claude analyzes the JD, matches it against your experience, and generates a tailored one-page LaTeX resume optimized for ATS systems

The system mirrors exact JD keywords, reorders skills by relevance, rewrites bullets to emphasize matching experience, and verifies skill gaps with you before adding anything new.

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI installed and configured

## Quick Start

```bash
# Clone the repo
git clone <repo-url>
cd resume-builder

# Option A: Import your existing resume
# Open Claude Code and say:
#   "Import resume" — then provide your resume PDF path or paste the text

# Option B: Manual setup
cp master-resume.sample.yaml master-resume.yaml
# Edit master-resume.yaml with your details

# Tailor for a job
# Open Claude Code and say:
#   "Tailor for <paste job description here>"
```

## Commands

| Command | What it does |
|---|---|
| `Tailor for [JD]` | Full tailoring workflow — analyze JD, match, verify skills, generate .tex |
| `Import resume` | Parse a PDF or text resume into `master-resume.yaml` |
| `Just the keywords` | Analyze a JD without generating a resume |
| `Update master` | Add new info to `master-resume.yaml` |
| `Regenerate` | Re-run generation with adjusted parameters |
| `Compare` | Side-by-side of original vs tailored bullets |

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
└── imports/                     # Source resumes for import (gitignored)
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
