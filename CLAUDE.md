# Resume Builder - Project Instructions

## Overview
This project tailors resumes for specific job descriptions to maximize ATS (Applicant Tracking System) scores. It can also import an existing resume (PDF or text) to bootstrap the master data file. It outputs Overleaf-compatible LaTeX files.

## Getting Started (for new users)

There are two ways to set up your master data:

1. **Import your resume**: Say `"Import resume"` and provide your existing resume (PDF file path or paste the text). Claude will parse it and generate `master-resume.yaml` for you.
2. **Manual setup**: Copy `master-resume.sample.yaml` to `master-resume.yaml` and fill in your details following the annotated comments.

## Project Structure
```
resume-builder/
├── CLAUDE.md                    # This file — instructions for Claude
├── master-resume.yaml           # Your career data (gitignored — personal)
├── master-resume.sample.yaml    # Annotated template to copy and fill in
├── templates/
│   └── resume-template.tex      # ATS-friendly LaTeX template with placeholders
├── jobs/
│   └── <company>-<role>.txt     # Job descriptions (user pastes these)
├── output/
│   └── <company>-<role>.tex     # Generated tailored resumes
├── imports/                     # (Optional) Source resumes for import (PDF/text)
├── scripts/
│   └── search_jobs.py           # Job search script (wraps python-jobspy)
├── searches/                    # Scraped job results (gitignored)
└── requirements.txt             # Python dependencies (for job search)
```

## Workflow: How to Tailor a Resume

When the user asks to tailor a resume for a job description:

### Step 1: Analyze the Job Description
- Extract **required skills** (must-have)
- Extract **preferred/nice-to-have skills**
- Identify **key action verbs** used in the JD
- Identify **industry-specific terminology**
- Note the **seniority level** and **role focus** (backend, full stack, frontend, etc.)
- Save the JD to `jobs/<company>-<role>.txt`

### Step 2: Match Against Master Resume
- Compare JD requirements against `master-resume.yaml`
- Identify which experiences/bullets best demonstrate each requirement
- Note any **gaps** (JD asks for something not in the resume)
- Decide which projects are most relevant to include

### Step 2.5: Skill Gap Verification (CRITICAL — do NOT skip)
After matching, identify skills/technologies from the JD that are **not present** in `master-resume.yaml` (neither in the `skills` section nor implied by experience bullets/project tech stacks).

For each missing skill, **ask the user** using AskUserQuestion with multi-select:
- Present the list of missing skills as options
- User ticks the ones they actually have, unticks the ones they don't
- Example: "The JD mentions these skills not in your master data. Which do you actually have?"
  - [ ] Kubernetes
  - [ ] Terraform
  - [ ] GraphQL
  - [ ] Kafka

**After user responds:**
- **Skills the user confirms (ticked):** Immediately add them to the appropriate category in `master-resume.yaml` so they persist for future tailoring. Then include them in the tailored resume.
- **Skills the user denies (unticked):** Do NOT add to resume or master data. Note them in the ATS match report as "gaps".
- This ensures the master data grows over time and becomes more complete with each tailoring session.

**Where to add confirmed skills in master-resume.yaml:**
- Programming languages → `skills.languages`
- Frameworks/libraries → `skills.frameworks`
- Databases → `skills.databases`
- Tools/platforms/infra → `skills.tools`
- If a skill also warrants a new `keywords` entry on a relevant experience role, add it there too

### Step 3: Tailor Content
Apply these ATS optimization rules:

#### Keyword Optimization
- **Mirror exact phrases** from the JD (e.g., if JD says "RESTful APIs", use "RESTful APIs" not "REST endpoints")
- **Front-load keywords** in bullet points — put the most relevant keyword/skill early in each bullet
- **Include both spelled-out and abbreviated forms** where applicable (e.g., "Continuous Integration/Continuous Deployment (CI/CD)")
- **Match the JD's language** for job title if appropriate (e.g., if JD says "Software Engineer" and candidate's title is "Full Stack Engineer", consider which works better)

#### Bullet Point Rules
- Start every bullet with a **strong action verb** (Developed, Optimized, Architected, Implemented, Designed, Built, Led, Automated)
- **Quantify impact** wherever possible (%, time saved, scale, users affected)
- Follow the **XYZ formula**: Accomplished [X] as measured by [Y] by doing [Z]
- Keep bullets to **1-2 lines max**
- Rewrite bullets to emphasize aspects relevant to the target JD
- **Do NOT fabricate** experience or skills — only reframe existing experience

#### Skills Section
- **Reorder skills** to put JD-mentioned skills first in each category
- **Add skills** only if genuinely possessed (check if mentioned in experience bullets)
- **Remove irrelevant skills** if space is tight and they add no value for the specific role

#### Section Ordering
- Default: Experience > Projects > Education > Skills > Achievements
- If the JD heavily emphasizes specific skills, consider: Experience > Skills > Projects > Education > Achievements
- Keep Education section if the user has a strong educational background

#### What to Include/Exclude
- Always include the user's primary/longest employment
- Hackathons, short stints, internships — include only if relevant to the JD
- Projects — pick the 1-2 most relevant; can omit others if not relevant
- Achievements — always include patents and high-signal items; include others if relevant

### Step 4: Generate LaTeX Output
- Use the template from `templates/resume-template.tex` as the structural base
- Fill in all content with tailored resume data
- Save to `output/<company>-<role>.tex`
- The output must compile cleanly in Overleaf with pdfLaTeX

### Step 5: Provide ATS Match Report
After generating the resume, provide:
```
=== ATS MATCH REPORT ===
JD Keywords Matched:     [list]
JD Keywords Missing:     [list with explanation why they can't be added]
Skills Coverage:         X/Y required skills matched
Estimated ATS Score:     High/Medium/Low with reasoning
Suggestions:             Any additional improvements possible
```

## Workflow: Import Resume into Master Data

When the user asks to "import a resume", "parse a resume", "create master from resume", or provides a PDF/text resume to be converted into master-resume.yaml format:

### Step 1: Accept the Resume Input

Determine the input format:

- **PDF file**: The user provides a path to a PDF file. Use the Read tool to read the PDF — Claude Code natively supports reading PDFs. If multi-page, read all pages.
- **Plain text / pasted content**: The user pastes the resume text directly into the conversation. No file reading needed.
- **Optionally save**: If the user provides a file, copy it to `imports/` for reference.

If the input is ambiguous (e.g., the user says "here's my resume" without providing anything), ask: "Please either provide the path to your resume PDF, or paste the resume text directly."

### Step 2: Parse and Extract Resume Sections

Read through the entire resume and extract data into these categories:

#### Contact Information
Extract: name, phone, email, LinkedIn URL, GitHub URL.
- Strip prefixes like "Email:", "Phone:", "LinkedIn:" etc.
- For LinkedIn/GitHub, store just the URL path (e.g., `linkedin.com/in/john-doe`), not the full `https://` URL.
- If any contact field is missing, leave it as `""` and flag it in Step 3.

#### Experience
Extract each position into the nested company/roles structure:
- **Company grouping**: Multiple roles at the same company go under one `company` entry with multiple `roles`.
- **Title**: Use the most senior/recent title as the top-level `title`. Each role gets its own `title` in the `roles` array.
- **Dates**: Normalize to `Mon YYYY` format (e.g., `Aug 2023`). If only years are given, use `Jan YYYY` for start and `Dec YYYY` for end. Use `Present` for current roles. Set company-level `start`/`end` to the earliest/latest role dates.
- **Location**: Extract city/state/country. If not specified, leave as `""`.
- **Bullets**: Preserve the original text as-is. Do NOT rewrite or enhance — the tailoring workflow handles that.
- **Keywords**: Generate 5-12 relevant keywords per role from the bullet content (technologies, domain terms, methodologies).
- **Team**: Use `""` if not specified — most external resumes won't have team names.
- **Single role per company**: Still use the `roles` array with one entry for schema consistency.
- **Ambiguous roles**: If unclear whether entries are separate roles at the same company or different companies, ask the user in Step 3.

#### Projects
Extract each project:
- **name**: Project name/title
- **tech**: Array of technologies (parse from "Tech stack:", "Built with:", or extract from descriptions)
- **year**: Most recent year if a range is given
- **bullets**: Preserve original text as-is
- **keywords**: Generate 4-8 relevant keywords per project

#### Education
Extract each degree:
- **institution**: Full name
- **degree**: Full degree name (e.g., "Master of Technology in Software Engineering")
- **start** / **end**: Year as string. Use `Present` if ongoing.
- **gpa**: Include scale (e.g., "9.19/10", "3.8/4.0"). Omit if not listed.

#### Skills
Categorize all mentioned skills into four buckets:
- **languages**: Programming/scripting languages (Java, Python, JavaScript, SQL, etc.)
- **frameworks**: Frameworks and libraries (Spring Boot, React, Django, etc.)
- **databases**: Databases and data stores (PostgreSQL, MongoDB, Redis, etc.)
- **tools**: DevOps, cloud, CI/CD, platforms, etc. (Docker, AWS, Git, Jenkins, etc.)

Look for skills in: explicit Skills sections, experience bullets, project tech stacks, and certifications.

#### Achievements
Extract awards, patents, certifications, publications, hackathon results:
- **title**: Short descriptive title
- **detail**: Supporting detail (patent number, placement, issuer, etc.)
- **year**: Year as string

#### Non-standard Sections
Map sections not in the schema to the closest match:
- Certifications → Achievements
- Publications → Achievements
- Volunteer work → Experience (with a note) or omit if not career-relevant
- Ask the user if the mapping is unclear.

### Step 3: Present Parsed Data for User Review

Before writing any file, present a structured summary:

```
=== PARSED RESUME SUMMARY ===

Contact:
  Name:     [name]
  Phone:    [phone]
  Email:    [email]
  LinkedIn: [linkedin]
  GitHub:   [github]

Experience: [N] companies, [M] total roles
  [Company | Title | Dates | Location | # bullets per role]

Projects: [N] projects
  [Name | Tech | Year | # bullets]

Education: [N] entries
  [Institution | Degree | Dates | GPA]

Skills:
  Languages:  [list]
  Frameworks: [list]
  Databases:  [list]
  Tools:      [list]

Achievements: [N] entries
  [Title | Year]

=== ISSUES & QUESTIONS ===
- [Missing fields, ambiguous dates, unclear role boundaries, etc.]
```

Wait for the user to confirm or provide corrections. Apply all corrections before proceeding.

### Step 4: Choose Output File

Ask the user using AskUserQuestion:

> "Where should I save the master resume data?"
> 1. **Overwrite** existing `master-resume.yaml`
> 2. **Create new file** as `master-resume-<lastname>.yaml`

If no existing `master-resume.yaml` exists, skip this question and create it directly.

### Step 5: Generate the YAML File

Write the YAML file using this exact schema and field ordering:

```yaml
contact:
  name: "..."
  phone: "..."
  email: "..."
  linkedin: "..."
  github: "..."

experience:
  - company: "..."
    title: "..."
    location: "..."
    start: Mon YYYY
    end: Mon YYYY | Present
    roles:
      - team: "..."
        title: "..."
        start: Mon YYYY
        end: Mon YYYY | Present
        bullets:
          - "..."
        keywords:
          - "..."

projects:
  - name: "..."
    tech: [...]
    year: YYYY
    bullets:
      - "..."
    keywords:
      - "..."

education:
  - institution: "..."
    degree: "..."
    start: "YYYY"
    end: "YYYY"
    gpa: "..."

skills:
  languages: [...]
  frameworks: [...]
  databases: [...]
  tools: [...]

achievements:
  - title: "..."
    detail: "..."
    year: "YYYY"
```

**Formatting rules:**
- Double quotes for strings with special characters (colons, commas, parentheses)
- Inline `[item1, item2]` arrays for `tech`, `languages`, `frameworks`, `databases`, `tools`
- Indented `- "..."` lists for `bullets` and `keywords`
- Consistent 2-space indentation

### Step 6: Confirmation

After writing the file:

```
=== IMPORT COMPLETE ===
File written: [path]
  - Contact: [complete/partial — list missing fields]
  - Experience: [N] companies, [M] roles, [B] total bullets
  - Projects: [N] projects
  - Education: [N] entries
  - Skills: [N] languages, [N] frameworks, [N] databases, [N] tools
  - Achievements: [N] entries

You can now use "Tailor for [JD]" to generate a tailored resume from this data.
```

## ATS Formatting Rules (ALWAYS follow)
- **Single column layout only** — no multi-column sections
- **No graphics, icons, images, or charts**
- **No text boxes or tables for layout** (tabular for alignment is fine)
- **Standard section headings**: Experience, Projects, Education, Technical Skills, Achievements
- **Standard fonts**: Computer Modern (LaTeX default) is perfect
- **No header/footer content** except page numbers if multi-page
- **File format**: .tex that compiles to clean PDF
- **Consistent date formatting**: Mon YYYY – Mon YYYY
- **No special characters** that might break ATS parsing

## Workflow: Search for Jobs

When the user asks to "search jobs", "find jobs", "find jobs for [role]", or provides job search criteria:

### Step 1: Gather Search Criteria

If the user hasn't provided all details, ask using AskUserQuestion:
- **Search term** (required): e.g., "software engineer", "backend developer", "full stack engineer"
- **Location** (optional): e.g., "Bengaluru, India", "San Francisco, CA", "Remote"
- **Job sites** (optional): default is linkedin,indeed,google. Options: linkedin, indeed, google, glassdoor, zip_recruiter
- **Additional filters** (optional): job type (fulltime/parttime/contract/internship), remote-only, posting age in hours (default 72)

### Step 2: Run the Search Script

Execute the search:
```bash
python3 scripts/search_jobs.py \
  --search-term "<term>" \
  --location "<location>" \
  --sites <sites> \
  --results 25 \
  --hours-old <hours> \
  [--remote] [--job-type <type>] [--country <country>]
```

**If Python 3.10+ is not available**, inform the user:
> "The job search feature requires Python 3.10+. Install it via `brew install python@3.12` or `pyenv install 3.12`, then set up dependencies: `python3.12 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`"

**If using a virtual environment**, use `.venv/bin/python3` instead of `python3`.

**If the script fails** due to rate limiting or network issues, suggest:
- Reducing `--results` to 10
- Searching one site at a time (e.g., `--sites indeed`)
- Trying again after a brief wait

### Step 3: Confirm Results

After the script runs, read the generated JSON file from `searches/` and report:
```
=== JOB SEARCH RESULTS ===
Search:    <search term>
Location:  <location>
Sources:   <sites>
Found:     <N> jobs
Saved to:  searches/<filename>.json

Say "Match jobs" to score and rank results against your profile.
```

## Workflow: Match Jobs Against Profile

When the user asks to "match jobs", "rank jobs", "score jobs", or "which jobs fit me":

### Step 1: Load Data

- Read the most recent JSON file in `searches/` (or a specific file if the user names one)
- Read `master-resume.yaml`

### Step 2: Score Each Job

For each job with a non-empty description, calculate a fit score (out of 100) using these weighted criteria:

#### Scoring Rubric

| Criterion | Weight | How to Score |
|-----------|--------|--------------|
| **Skill Match** | 35 pts | Count skills/technologies in JD that appear in master-resume `skills` section OR experience/project `keywords`. Score = (matched / total_jd_skills) × 35 |
| **Tech Stack Alignment** | 25 pts | Check if the JD's primary stack (e.g., "Java + Spring Boot + PostgreSQL") aligns with candidate's strongest technologies (most bullets/keywords). Score = (aligned_primary / total_primary) × 25 |
| **Experience Level Match** | 20 pts | Compare JD seniority signals (years required, "senior"/"junior"/"lead" in title) against candidate's experience. Full match = 20, adjacent level = 12, mismatch = 5 |
| **Domain Relevance** | 10 pts | Does the JD's industry/domain overlap with candidate's experience domains? Full overlap = 10, partial = 5, none = 2 |
| **Location/Remote Fit** | 10 pts | Remote or candidate's current city = 10, relocation required = 5, unclear = 7 |

**Scoring Guidelines:**
- Match skills case-insensitively with common aliases (e.g., "JS" = "JavaScript", "Postgres" = "PostgreSQL", "k8s" = "Kubernetes")
- Weigh technologies appearing in multiple experience roles/projects more heavily — these are strongest skills
- Jobs with no description get score 0 and are marked "insufficient data"
- Round final score to nearest integer

### Step 3: Present Ranked Results

```
=== JOB MATCH RESULTS ===
Based on: searches/<filename>.json
Profile:  <candidate name> — <current title>

#  | Score | Title                        | Company       | Location       | Key Matches
---|-------|------------------------------|---------------|----------------|------------------
1  | 87    | Full Stack Engineer           | Stripe        | Remote         | Java, Spring Boot, PostgreSQL, REST APIs
2  | 82    | Backend Software Engineer     | Datadog       | New York, NY   | Java, distributed systems, monitoring
3  | 74    | Software Engineer II          | Google        | Bengaluru      | full stack, large-scale systems
...

Jobs with insufficient data: <N> (no description available)

Say "Tailor for job #N" to generate a tailored resume, or "Show job #N" to see full details.
```

### Step 4: Job Detail View (optional)

When the user says "Show job #N":
- Display the full job description
- Show the detailed score breakdown (each criterion with points awarded)
- List matched skills and gap skills
- Provide the job URL

## Workflow: Tailor for a Matched Job

When the user says "Tailor for job #N" (referencing a matched job from search results):

### Step 1: Retrieve the Job

- Load the searches JSON file used in the most recent "Match jobs" run
- Find job #N from the ranked list
- Extract the full job description

### Step 2: Save as Job Description

Save the job description to `jobs/<company>-<role>.txt` in standard format:
```
Company: <company name>
Role: <job title>
Source: <site_name> / <job_url>

---

<full job description>
```

### Step 3: Bridge to Existing Tailoring Workflow

Run the standard "Tailor for [JD]" workflow (Steps 1–5) using the saved JD. The existing pipeline handles everything: JD analysis, master resume matching, skill gap verification, content tailoring, LaTeX generation, and ATS match report.

## Important Constraints
- NEVER add skills to the resume without user confirmation via Step 2.5
- NEVER invent experience or achievements not in master-resume.yaml
- NEVER change dates, company names, or degree information
- ALWAYS keep the resume to ONE page
- ALWAYS run Step 2.5 if there are JD skills missing from master data — do not silently skip them
- After user confirms new skills, ALWAYS update master-resume.yaml before generating the .tex
- When rewriting bullets, preserve the core truth — only change emphasis and wording
- When importing a resume, NEVER embellish or rewrite bullet points — import them verbatim. Enhancement happens only during the tailoring workflow.

## Quick Command Reference
When the user says:
- "Tailor for [JD]" → Run full workflow above
- "Just the keywords" → Run Step 1 only, show analysis
- "Update master" → Update master-resume.yaml with new info
- "Regenerate" → Re-run Steps 3-5 with adjusted parameters
- "Compare" → Show side-by-side of original vs tailored bullets
- "Import resume" → Run Import Resume workflow above
- "Parse resume" → Run Import Resume workflow above
- "Create master from [resume]" → Run Import Resume workflow above
- "Search jobs" / "Find jobs for [role]" → Run Search for Jobs workflow
- "Match jobs" → Run Match Jobs workflow — score and rank against profile
- "Tailor for job #N" → Save matched job's JD, then run full tailoring workflow
- "Show job #N" → Show full details and score breakdown for a matched job
