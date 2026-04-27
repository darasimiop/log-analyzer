from flask import Flask, request, render_template
import os
from werkzeug.utils import secure_filename
from log_analyzer.log_analyzer import parse_logs, generate_reports


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
STATIC_FOLDER = os.path.join(BASE_DIR, "static")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["STATIC_FOLDER"] = STATIC_FOLDER
app.config["ALLOWED_EXTENSIONS"] = {".log", ".txt"}


def _is_allowed(filename: str) -> bool:
    _, ext = os.path.splitext(filename.lower())
    return ext in app.config["ALLOWED_EXTENSIONS"]


@app.route("/", methods=["GET", "POST"])
def upload_file():
    message = None
    message_type = "info"
    summary = None
    top_ips = []
    if request.method == "POST":
        uploaded = request.files.get("file")
        if not uploaded or not uploaded.filename:
            message = "Please choose a .log or .txt file to upload."
            message_type = "danger"
        elif not _is_allowed(uploaded.filename):
            message = "Only .log and .txt files are allowed."
            message_type = "danger"
        else:
            filename = secure_filename(uploaded.filename)
            saved_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            uploaded.save(saved_path)

            try:
                df = parse_logs(saved_path)
                report_csv, status_bar_path, top_ips_path = generate_reports(
                    df, output_dir=app.config["STATIC_FOLDER"]
                )
            except Exception:
                message = "Sorry, there was a problem parsing that file."
                message_type = "danger"
            else:
                rows = df.to_dict(orient="records")
                total = len(df)
                failed = int((df["Status"] == "Failed").sum()) if not df.empty else 0
                success = int((df["Status"] == "Success").sum()) if not df.empty else 0
                top_ips = (
                    df.loc[df["IP"] != "-", "IP"].value_counts().head(5).items()
                    if not df.empty
                    else []
                )
                summary = {
                    "total": total,
                    "failed": failed,
                    "success": success,
                }
                message = f"Report generated: {os.path.basename(report_csv)}"
                message_type = "success"
                return render_template(
                    "index.html",
                    message=message,
                    message_type=message_type,
                    summary=summary,
                    top_ips=top_ips,
                    rows=rows[:200],
                    status_bar=os.path.basename(status_bar_path),
                    top_ips_bar=os.path.basename(top_ips_path),
                    report_file=os.path.basename(report_csv),
                )

    return render_template(
        "index.html",
        message=message,
        message_type=message_type,
        summary=summary,
        top_ips=top_ips,
        rows=None,
        status_bar=None,
        top_ips_bar=None,
        report_file=None,
    )


if __name__ == "__main__":
    # Use 0.0.0.0 for convenience when presenting; remove debug=True for production
    app.run(host="0.0.0.0", port=5000, debug=True)
