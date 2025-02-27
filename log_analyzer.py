import argparse
import pandas as pd
import re
import os

# Define log file parsing function
def parse_logs(log_file):
    if not os.path.exists(log_file):
        print(f"❌ Error: Log file '{log_file}' not found!")
        return None

    results = []
    patterns = {
        "Invalid User": r"(?P<timestamp>\w{3} \d{2} \d{2}:\d{2}:\d{2}) .*Failed password for invalid user (?P<username>\w+) from (?P<ip>[\d\.]+)",
        "Valid User": r"(?P<timestamp>\w{3} \d{2} \d{2}:\d{2}:\d{2}) .*Accepted password for (?P<username>\w+) from (?P<ip>[\d\.]+)"
    }

    with open(log_file, "r") as f:
        for line in f:
            for status, pattern in patterns.items():
                match = re.search(pattern, line)
                if match:
                    results.append({
                        "Timestamp": match.group("timestamp"),
                        "Status": status,
                        "Username": match.group("username"),
                        "IP Address": match.group("ip")
                    })

    return results


# Write results to CSV
def save_to_csv(data, output_file="security_report.csv"):
    if not data:
        print("⚠️ No security events found in log file.")
        return
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"✅ Security report generated: {output_file}")

# Main function
def main():
    parser = argparse.ArgumentParser(description="Log Analyzer for SSH failures")
    parser.add_argument("-f", "--file", type=str, default="auth.log", help="Path to log file")
    args = parser.parse_args()

    log_data = parse_logs(args.file)
    save_to_csv(log_data)

# Run script
if __name__ == "__main__":
    main()
