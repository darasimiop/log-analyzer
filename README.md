# Log Analyzer

A small, presentable project that parses authentication-style logs (for example `/var/log/auth.log`) and produces a clean CSV report plus simple visualizations (bar and pie charts). Designed as a quick demo you can show at career fairs or include in your GitHub portfolio.

Features
- Flask demo with file upload and report download
- Robust parsing heuristics for common auth log entries
- Generates `security_report.csv`, `login_attempts_bar.png`, and `login_attempts_pie.png`
- Unit test for the parser to demonstrate good engineering practices

Quickstart

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows (PowerShell): venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

2. Run the demo web app (local):

```bash
python app.py
# then open http://localhost:5000 in your browser
```

3. Or run the CLI against the included `sample_log.txt`:

```bash
python -m log_analyzer.log_analyzer -f log_analyzer/sample_log.txt -o ./static
```

What's improved for presentation
- Clear README and instructions
- Polished web UI and safe file handling
- CSV + visuals saved to `static/` so images and reports are easy to display on GitHub Pages or the demo site

License

MIT

Badges

![CI](https://github.com/darasimiop/log-analyzer/actions/workflows/ci.yml/badge.svg)

Docker

Build the image and run the demo locally:

```bash
docker build -t log-analyzer .
docker run --rm -p 5000:5000 log-analyzer
# open http://localhost:5000 in your browser
```

GitHub Actions

This repo includes a GitHub Actions workflow at `.github/workflows/ci.yml` which will run tests on push/PR. After you push this branch the CI badge above will show the build status.

Want more polish?
- I can add a Docker Compose file to run the app plus a tiny static file server, or add a GitHub Pages demo for the static outputs. Tell me which and I’ll wire it in.
