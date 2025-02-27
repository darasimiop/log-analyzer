import argparse
import pandas as pd
import re
import os
import glob
import gzip
import matplotlib.pyplot as plt

# Define log file parsing function
def parse_logs(log_files):
    results = []

    patterns = {
        "Invalid User": r"(?P<timestamp>\w{3} \d{2} \d{2}:\d{2}:\d{2}) .*Failed password for invalid user (?P<username>\S+) from (?P<ip>[\d\.]+)",
        "Valid User": r"(?P<timestamp>\w{3} \d{2} \d{2}:\d{2}:\d{2}) .*Accepted password for (?P<username>\S+) from (?P<ip>[\d\.]+)"
    }

    for log_file in log_files:
        try:
            print(f"🔍 Analyzing {log_file}...")
            open_func = gzip.open if log_file.endswith('.gz') else open

            with open_func(log_file, "rt", encoding="utf-8", errors="ignore") as f:
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
        except Exception as e:
            print(f"⚠️ Error processing {log_file}: {e}")

    return results

# Write results to CSV
def save_to_csv(data, output_file="security_report.csv"):
    if not data:
        print("⚠️ No security events found.")
        return
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"✅ Security report generated: {output_file}")

# Generate visual reports
def generate_charts(data):
    df = pd.DataFrame(data)

    # Count failed vs. successful logins
    status_counts = df["Status"].value_counts()

    # 🔹 Bar Chart
    plt.figure(figsize=(6, 4))
    status_counts.plot(kind="bar", color=["red", "green"])
    plt.title("Failed vs. Successful SSH Logins")
    plt.xlabel("Login Type")
    plt.ylabel("Number of Attempts")
    plt.xticks(rotation=0)
    plt.savefig("login_attempts_bar.png")
    print("📊 Bar chart saved as login_attempts_bar.png")

    # 🔹 Pie Chart
    plt.figure(figsize=(6, 6))
    status_counts.plot(kind="pie", autopct="%1.1f%%", colors=["red", "green"])
    plt.title("SSH Login Attempt Breakdown")
    plt.ylabel("")
    plt.savefig("login_attempts_pie.png")
    print("📊 Pie chart saved as login_attempts_pie.png")

# Main function
def main():
    parser = argparse.ArgumentParser(description="Log Analyzer for SSH failures")
    parser.add_argument("-d", "--directory", type=str, default="/var/log/", help="Directory containing log files")
    args = parser.parse_args()

    log_files = glob.glob(os.path.join(args.directory, "auth.log*"))
    if not log_files:
        print("❌ No log files found in the specified directory.")
        return

    log_data = parse_logs(log_files)
    
    if log_data:
        save_to_csv(log_data)
        generate_charts(log_data)  # NEW: Generate graphs after saving CSV

# Run script
if __name__ == "__main__":
    main()
