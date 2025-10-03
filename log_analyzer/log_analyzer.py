import os
from typing import Tuple
import pandas as pd
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


LOG_LINE_RE = re.compile(r"^(?P<month>\w+)\s+(?P<day>\d+)\s+(?P<time>\d+:\d+:\d+)\s+(?P<host>\S+)\s+(?P<service>[^:]+):\s+(?P<message>.*)$")


def parse_logs(log_file: str) -> pd.DataFrame:
    """Parse an auth-like log file and return a pandas DataFrame.

    Columns: Timestamp (string), Status (Success/Failed/Other), User, IP
    """
    rows = []
    with open(log_file, "r", encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            m = LOG_LINE_RE.match(line.strip())
            if not m:
                continue
            msg = m.group("message")
            timestamp = f"{m.group('month')} {m.group('day')} {m.group('time')}"

            # Common patterns
            if "Failed password" in msg or "Failed" in msg and "password" in msg:
                status = "Failed"
            elif "Accepted password" in msg or "Accepted" in msg:
                status = "Success"
            else:
                status = "Other"

            # Try to extract user and IP address
            user = None
            ip = None
            # user patterns: for sshd: for user <user> or invalid user <user>
            user_match = re.search(r"for (invalid user )?(?P<user>[\w@.-]+)", msg)
            if user_match:
                user = user_match.group("user")

            # IP patterns
            ip_match = re.search(r"from (?P<ip>[0-9]+(?:\.[0-9]+){3})", msg)
            if ip_match:
                ip = ip_match.group("ip")

            rows.append({"Timestamp": timestamp, "Status": status, "User": user or "-", "IP": ip or "-", "Raw": msg})

    df = pd.DataFrame(rows)
    return df


def generate_reports(df: pd.DataFrame, output_dir: str = ".") -> Tuple[str, str, str]:
    """Generate CSV and two charts (bar + pie) summarizing login attempts.

    Returns tuple: (csv_path, bar_image_path, pie_image_path)
    """
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "security_report.csv")
    df.to_csv(csv_path, index=False)

    # Bar: failed vs success count
    counts = df['Status'].value_counts()
    bar_path = os.path.join(output_dir, "login_attempts_bar.png")
    plt.figure(figsize=(6,4))
    counts.plot(kind='bar', color=['#e74c3c' if s=='Failed' else '#2ecc71' for s in counts.index])
    plt.title('Login Attempts by Status')
    plt.xlabel('Status')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(bar_path)
    plt.close()

    # Pie: top 5 IPs
    top_ips = df['IP'].value_counts().head(5)
    pie_path = os.path.join(output_dir, "login_attempts_pie.png")
    plt.figure(figsize=(6,6))
    if top_ips.sum() == 0:
        plt.text(0.5, 0.5, 'No IP data', horizontalalignment='center', verticalalignment='center')
    else:
        top_ips.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Top IPs by Attempts')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig(pie_path)
    plt.close()

    return csv_path, bar_path, pie_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Parse auth log and produce reports')
    parser.add_argument('-f', '--file', default='sample_log.txt')
    parser.add_argument('-o', '--out', default='.')
    args = parser.parse_args()
    df = parse_logs(args.file)
    generate_reports(df, output_dir=args.out)
