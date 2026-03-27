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
└── imports/                     # (Optional) Source resumes for import (PDF/text)
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
