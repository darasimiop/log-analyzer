import pandas as pd
from log_analyzer.log_analyzer import parse_logs


def _write(tmp_path, content: str):
    path = tmp_path / "auth.log"
    path.write_text(content)
    return path


def test_failed_login_parsing(tmp_path):
    content = "Feb 26 18:54:32 host sshd[704]: Failed password for root from 10.0.0.5 port 22 ssh2\n"
    path = _write(tmp_path, content)
    df = parse_logs(str(path))
    assert len(df) == 1
    assert df.iloc[0]["Status"] == "Failed"
    assert df.iloc[0]["User"] == "root"
    assert df.iloc[0]["IP"] == "10.0.0.5"


def test_success_login_parsing(tmp_path):
    content = "Feb 26 19:11:52 host sshd[5991]: Accepted password for dara from 172.16.0.2 port 22 ssh2\n"
    path = _write(tmp_path, content)
    df = parse_logs(str(path))
    assert len(df) == 1
    assert df.iloc[0]["Status"] == "Success"
    assert df.iloc[0]["User"] == "dara"
    assert df.iloc[0]["IP"] == "172.16.0.2"


def test_invalid_user_parsing(tmp_path):
    content = "Feb 26 18:54:32 host sshd[704]: Failed password for invalid user admin from 192.168.1.10 port 22 ssh2\n"
    path = _write(tmp_path, content)
    df = parse_logs(str(path))
    assert len(df) == 1
    assert df.iloc[0]["Status"] == "Failed"
    assert df.iloc[0]["User"] == "admin"
    assert df.iloc[0]["IP"] == "192.168.1.10"


def test_empty_file_handling(tmp_path):
    path = _write(tmp_path, "")
    df = parse_logs(str(path))
    assert isinstance(df, pd.DataFrame)
    assert df.empty
    assert set(["Timestamp", "Status", "User", "IP", "Raw"]).issubset(df.columns)
