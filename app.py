from flask import Flask, request, render_template, url_for
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


@app.route("/", methods=["GET", "POST"])
def upload_file():
    message = None
    if request.method == "POST":
        uploaded = request.files.get("file")
        if uploaded and uploaded.filename:
            filename = secure_filename(uploaded.filename)
            saved_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            uploaded.save(saved_path)

            # Parse and generate reports into the static folder
            df = parse_logs(saved_path)
            report_csv, bar_path, pie_path = generate_reports(df, output_dir=app.config["STATIC_FOLDER"]) 

            message = f"Report generated: {os.path.basename(report_csv)}"
            rows = df.to_dict(orient='records')
            # Only send small number of rows to template for performance
            return render_template("index.html", message=message, rows=rows[:200], bar_image=os.path.basename(bar_path), pie_image=os.path.basename(pie_path), report_file=os.path.basename(report_csv))
        else:
            message = "No file selected"

    return render_template("index.html", message=message, rows=None, bar_image=None, pie_image=None, report_file=None)


if __name__ == "__main__":
    # Use 0.0.0.0 for convenience when presenting; remove debug=True for production
    app.run(host="0.0.0.0", port=5000, debug=True)
