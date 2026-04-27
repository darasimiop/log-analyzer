import os
from typing import List, Tuple
import pandas as pd
import re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


LOG_LINE_RE = re.compile(
    r"^(?P<month>\w+)\s+(?P<day>\d+)\s+(?P<time>\d+:\d+:\d+)\s+(?P<host>\S+)\s+(?P<service>[^:]+):\s+(?P<message>.*)$"
)
FAILED_RE = re.compile(r"Failed password for (invalid user )?(?P<user>[\w@.-]+)")
ACCEPTED_RE = re.compile(r"Accepted password for (?P<user>[\w@.-]+)")
IP_RE = re.compile(r"from (?P<ip>[0-9]+(?:\.[0-9]+){3})")


def parse_logs(log_file: str) -> pd.DataFrame:
    """Parse an auth-style log file and return a pandas DataFrame."""
    rows: List[dict] = []
    with open(log_file, "r", encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            m = LOG_LINE_RE.match(line)
            if not m:
                continue

            msg = m.group("message")
            timestamp = f"{m.group('month')} {m.group('day')} {m.group('time')}"

            failed_match = FAILED_RE.search(msg)
            accepted_match = ACCEPTED_RE.search(msg)

            if failed_match:
                status = "Failed"
                user = failed_match.group("user")
            elif accepted_match:
                status = "Success"
                user = accepted_match.group("user")
            else:
                status = "Other"
                user = "-"

            ip_match = IP_RE.search(msg)
            ip = ip_match.group("ip") if ip_match else "-"

            rows.append(
                {
                    "Timestamp": timestamp,
                    "Status": status,
                    "User": user or "-",
                    "IP": ip or "-",
                    "Raw": msg,
                }
            )

    if not rows:
        return pd.DataFrame(columns=["Timestamp", "Status", "User", "IP", "Raw"])

    return pd.DataFrame(rows)


def generate_reports(df: pd.DataFrame, output_dir: str = ".") -> Tuple[str, str, str]:
    """Generate CSV and two charts (status counts + top IPs).

    Returns tuple: (csv_path, status_bar_path, top_ips_bar_path)
    """
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "security_report.csv")
    df.to_csv(csv_path, index=False)

    status_counts = df["Status"].value_counts() if not df.empty else pd.Series(dtype=int)
    status_bar_path = os.path.join(output_dir, "login_attempts_bar.png")
    plt.figure(figsize=(6, 4))
    if status_counts.empty:
        plt.text(0.5, 0.5, "No data", ha="center", va="center")
    else:
        colors = []
        for s in status_counts.index:
            if s == "Failed":
                colors.append("#e74c3c")
            elif s == "Success":
                colors.append("#2ecc71")
            else:
                colors.append("#95a5a6")
        status_counts.plot(kind="bar", color=colors)
    plt.title("Login Attempts by Status")
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(status_bar_path)
    plt.close()

    top_ips = (
        df.loc[df["IP"] != "-", "IP"].value_counts().head(5)
        if not df.empty
        else pd.Series(dtype=int)
    )
    top_ips_bar_path = os.path.join(output_dir, "top_ips_bar.png")
    plt.figure(figsize=(6, 4))
    if top_ips.empty:
        plt.text(0.5, 0.5, "No IP data", ha="center", va="center")
    else:
        top_ips.plot(kind="bar", color="#3498db")
    plt.title("Top IPs by Attempts")
    plt.xlabel("IP Address")
    plt.ylabel("Count")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(top_ips_bar_path)
    plt.close()

    return csv_path, status_bar_path, top_ips_bar_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Parse auth log and produce reports')
    parser.add_argument('-f', '--file', default='sample_log.txt')
    parser.add_argument('-o', '--out', default='.')
    args = parser.parse_args()
    df = parse_logs(args.file)
    generate_reports(df, output_dir=args.out)
