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
## Sample Output<img width="1919" height="878" alt="Screenshot 2026-04-27 135732" src="https://github.com/user-attachments/assets/f4f152e8-56b7-4630-8ec4-8f8fd03d3577" />
<img width="1919" height="878" alt="Screenshot 2026-04-27 135717" src="https://github.com/user-attachments/assets/69a1e8ab-8d6b-43c9-ae0c-ed74e93d08b1" />
<img width="1919" height="883" alt="Screenshot 2026-04-27 135702" src="https://github.com/user-attachments/assets/ff5d406e-4a1a-40a9-9497-bef8a9e20f46" />
