from flask import Flask, request, render_template
import pandas as pd
import os
from log_analyzer import parse_logs, save_to_csv, generate_charts

app = Flask(__name__)

# Create an uploads folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # Process the uploaded log file
            log_data = parse_logs([filepath])
            save_to_csv(log_data)
            generate_charts(log_data)

            return '''
            <h1>✅ Analysis Complete!</h1>
            <p>Check security_report.csv & generated charts.</p>
            <p><a href="/">🔄 Upload Another File</a></p>
            '''

    return '''
    <h1>🔍 Log Analyzer Web App</h1>
    <form method="post" enctype="multipart/form-data">
        Upload Log File: <input type="file" name="file">
        <input type="submit" value="Analyze">
    </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)
