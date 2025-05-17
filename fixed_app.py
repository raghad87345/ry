from flask import Flask, request, jsonify
from moviepy.editor import VideoFileClip
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/analyze', methods=['POST'])
def analyze_video():
    if 'video' not in request.files:
        return jsonify({"error": "لا يوجد ملف فيديو مرفوع"}), 400

    file = request.files['video']
    topic = request.form.get('topic', '')

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    try:
        clip = VideoFileClip(filepath)
        duration = clip.duration
        resolution = clip.size
        has_audio = clip.audio is not None

        score = 50
        if duration <= 15:
            score += 20
        elif duration > 60:
            score -= 10
        if resolution[0] >= 720:
            score += 10
        if has_audio:
            score += 10
        score = max(0, min(100, score))

        hook = "ابدأ الفيديو بسؤال مثير أو عرض صادم خلال أول ثانيتين."
        tip = "قلل من المقدمات الطويلة، أضف حركة أو مؤثر بصري أول 3 ثواني."

        return jsonify({
            "duration": f"{duration:.1f} ثانية",
            "resolution": f"{resolution[0]}x{resolution[1]}",
            "audio": "نعم" if has_audio else "لا",
            "score": score,
            "hook": hook,
            "tip": tip
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)