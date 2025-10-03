import os
import pandas as pd
from log_analyzer.log_analyzer import parse_logs


def test_parse_sample_log(tmp_path):
    sample = """
Feb 26 18:54:32 host sshd[704]: Failed password for invalid user badguy from 203.0.113.5 port 22 ssh2
Feb 26 19:11:52 host sshd[5991]: Accepted password for alice from 192.0.2.10 port 2222 ssh2
    """
    p = tmp_path / "sample.log"
    p.write_text(sample)

    df = parse_logs(str(p))
    assert isinstance(df, pd.DataFrame)
    assert set(['Timestamp', 'Status', 'User', 'IP']).issubset(df.columns)
    # Expect 2 rows
    assert len(df) == 2
    # Check statuses
    assert 'Failed' in df['Status'].values
    assert 'Success' in df['Status'].values

