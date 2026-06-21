# Accessible HTML Coder

Accessible HTML Coder is a small Python command-line sample for exploring
LangGraph. It generates a complete static HTML document from a local
requirements file, reviews the document with axe-core, and loops until the page
has no accessibility findings or the workflow reaches a stopping condition.

> [!WARNING]
> This is an experimental project and should not be considered production-ready.

The project was created to learn how LangGraph can coordinate a simple
evaluator-optimizer workflow. A model-backed coder creates or revises the HTML,
while a deterministic reviewer runs axe-core in a Playwright browser context and
returns accessibility findings for the next coder pass.

## What It Does

The CLI accepts the name of a requirements file from the local `files`
directory:

```powershell
.\.venv\Scripts\python.exe -m accessible_html_coder the-big-lebowski.txt
```

The workflow then:

- reads the requirements file from `files`
- asks GPT-4o to create a complete HTML5 document
- loads the generated HTML into Playwright
- injects axe-core and collects accessibility findings
- sends the previous HTML and findings back to the coder for revision
- repeats until there are no findings, findings stop changing, or the maximum
  iteration count is reached
- writes the final HTML document back to `files`

For example, `files\the-big-lebowski.txt` produces
`files\the-big-lebowski.html`.

## Requirements

- Python 3.11.
- PowerShell on Windows.
- Node.js and npm for the local `axe-core` package.
- Playwright's Chromium browser.
- An `OPENAI_API_KEY` environment variable for OpenAI model calls.

## Setup

Create the virtual environment and install the Python project with development
dependencies:

```powershell
.\scripts\setup-dev.ps1
```

Install the local axe-core dependency from the repository root:

```powershell
npm install axe-core --save-dev
```

Install Playwright's Chromium browser:

```powershell
.\.venv\Scripts\playwright.exe install chromium
```

The setup script expects Python 3.11 at the path configured in
`scripts\setup-dev.ps1`.

## Running

Run the HTML coder from the repository root:

```powershell
.\.venv\Scripts\python.exe -m accessible_html_coder the-big-lebowski.txt
```

Example output:

```text
Created file: the-big-lebowski.html
Iterations: 3
Stop reason: no_accessibility_findings
Remaining findings: 0
```

The generated document is written to the `files` directory using the same base
name as the requirements file and an `.html` extension.

## Development Checks

Run formatting, linting, type checking, and tests:

```powershell
.\scripts\check.ps1
```

This runs:

- `ruff format .`
- `ruff check .`
- `pyright`
- `pytest`

## Project Structure

```text
src/accessible_html_coder/
  __main__.py  Package entry point for python -m accessible_html_coder
  cli.py       Command-line entry point and file-level orchestration
  coder.py     GPT-4o-backed HTML creation and revision
  files.py     Local requirements and HTML file helpers
  graph.py     LangGraph workflow, nodes, and routing logic
  models.py    Pydantic models for coder output and axe findings
  reviewer.py  Playwright and axe-core accessibility reviewer
  state.py     LangGraph state definition

files/
  the-big-lebowski.txt
  the-big-lebowski.jpg

tests/
  test_smoke.py

scripts/
  setup-dev.ps1
  check.ps1
```

## Notes

This project is a LangGraph learning exercise, not a general-purpose web page
builder. The sample requirements are intentionally small so the feedback loop
stays easy to inspect.

axe-core can catch many machine-detectable accessibility problems, but it is
not a complete accessibility review. Some concerns, such as whether link text
or image alt text is truly appropriate, still require human judgment.

The coder is model-driven, so generated HTML and the number of iterations can
vary between runs. OpenAI API calls may incur usage costs.

## Third-Party Notices

This project has direct runtime dependencies on third-party Python packages,
including `langgraph` (MIT), `langchain` (MIT), `langchain-openai` (MIT),
`playwright` (Apache-2.0), and `pydantic` (MIT). It also uses the npm package
`axe-core` (MPL-2.0). See each package's license metadata for full license and
notice terms.

## License

GNU General Public License v3.0. See the `LICENSE` file for details.
