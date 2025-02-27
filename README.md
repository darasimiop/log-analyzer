# Log Analyzer 🛡️

This Python script analyzes Linux authentication logs (`auth.log`) to detect **failed SSH login attempts**. It extracts invalid login attempts and saves them into a structured CSV file.

## 🚀 Installation & Setup

1️⃣ **Clone the repository:**
   ```bash
   git clone https://github.com/darasimiop/log-analyzer.git
   cd log-analyzer

2️⃣ Create a virtual environment & install dependencies:

python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

⚙️ Usage
📌 Analyze Default System Logs (auth.log):

1️⃣ Copy the system log file (Linux only):

sudo cp /var/log/auth.log ./auth.log

2️⃣ Run the Log Analyzer:

python log_analyzer.py

3️⃣ Check the generated report:

cat security_report.csv

📌 Analyze Custom Log Files:

Instead of using auth.log, you can specify any log file:

python log_analyzer.py -f my_custom_log.log

📊 Example Output

Status,Username,IP Address
Invalid User,invaliduser,127.0.0.1
Invalid User,invaliduser,127.0.0.1
Invalid User,invaliduser,127.0.0.1
Valid User,validuser,192.168.1.10

📌 Features

✔️ Extracts failed SSH login attempts
✔️ Extracts successful SSH logins
✔️ Saves data in CSV format
✔️ Works with real system logs
✔️ Allows custom log file input
📜 License

MIT License