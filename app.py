from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)
DOWNLOAD_DIR = "downloads"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        video_id = str(uuid.uuid4())
        output_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp4")

        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': output_path
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return send_file(output_path, as_attachment=True)
        except Exception as e:
            return f"Download failed: {e}"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)