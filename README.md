# Log Analyzer

Beginner-friendly cybersecurity log triage tool built with Python and Flask. This tool simulates basic SOC log triage by identifying suspicious login activity from authentication logs.

It parses Linux authentication logs, identifies failed and successful login attempts, summarizes high-activity IP addresses, and generates CSV reports and visual charts.

## Features
- Parses Linux authentication logs
- Identifies failed and successful login attempts
- Extracts timestamp, username, IP address, and raw message
- Summarizes high-activity IP addresses
- Generates CSV reports and visual charts
- Web UI for uploads and a simple CLI mode

## Run
```bash
pip install -r requirements.txt
python app.py
```

```bash
python -m log_analyzer.log_analyzer -f sample_log.txt -o static
```

```bash
python -m pytest
```
