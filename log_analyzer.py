import argparse
import re
import pandas as pd

# Argument parser to allow users to specify a log file
parser = argparse.ArgumentParser(description="Log Analyzer for SSH failures")
parser.add_argument("-f", "--file", type=str, default="auth.log", help="Path to log file")
args = parser.parse_args()

# Set log file (defaults to auth.log if not specified)
LOG_FILE = args.file  

# Define regex patterns to match failed and successful SSH logins
PATTERNS = {
    "failed_ssh": r"Failed password for (?:invalid user )?(\S+) from ([\d.]+) port \d+",
    "successful_ssh": r"Accepted password for (\S+) from ([\d.]+) port \d+"
}

def parse_logs(log_file):
    """Parses the given log file and extracts SSH login attempts."""
    results = {"failed_ssh": [], "successful_ssh": []}

    try:
        with open(log_file, "r") as f:
            for line in f:
                for key, pattern in PATTERNS.items():
                    match = re.search(pattern, line)
                    if match:
                        if key == "failed_ssh":
                            results[key].append(["Invalid User", match.group(1), match.group(2)])
                        else:
                            results[key].append(["Valid User", match.group(1), match.group(2)])
    except FileNotFoundError:
        print(f"Error: Log file '{log_file}' not found. Please provide a valid log file.")
        return None
    
    return results

def generate_csv(results, output_file="security_report.csv"):
    """Generates a CSV report from extracted SSH login attempts."""
    if results:
        failed_df = pd.DataFrame(results["failed_ssh"], columns=["Status", "Username", "IP Address"])
        successful_df = pd.DataFrame(results["successful_ssh"], columns=["Status", "Username", "IP Address"])

        with open(output_file, "w") as f:
            failed_df.to_csv(f, index=False, header=True)
            successful_df.to_csv(f, index=False, header=False, mode='a')
        
        print(f"✅ Security report generated: {output_file}")
    else:
        print("❌ No data extracted from log file.")

# Run the log analyzer
if __name__ == "__main__":
    parsed_results = parse_logs(LOG_FILE)
    if parsed_results:
        generate_csv(parsed_results)
