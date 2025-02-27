import re
import pandas as pd

LOG_FILE = "auth.log"  # Use real logs now

PATTERNS = {
    "failed_ssh": r"Failed password for (invalid user )?(\w+) from ([\d\.]+) port \d+",
    "successful_ssh": r"Accepted password for (\w+) from ([\d\.]+) port \d+"
}

def parse_logs(log_file):
    results = {"failed_ssh": [], "successful_ssh": []}

    with open(log_file, "r") as f:
        for line in f:
            for key, pattern in PATTERNS.items():
                match = re.search(pattern, line)
                if match:
                    results[key].append(match.groups())

    return results

def generate_report(parsed_data):
    report_df = pd.DataFrame(parsed_data["failed_ssh"], columns=["Invalid User", "Username", "IP Address"])
    report_df.to_csv("security_report.csv", index=False)
    print("Security report generated: security_report.csv")

if __name__ == "__main__":
    log_data = parse_logs(LOG_FILE)
    generate_report(log_data)
