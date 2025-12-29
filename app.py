import os
from flask import Flask, render_template, request
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

app = Flask(__name__)

# This pulls your API Key from the Render settings for safety
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

def get_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "be/" in url:
        return url.split("be/")[1]
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = ""
    if request.method == 'POST':
        url = request.form.get('url')
        video_id = get_video_id(url)
        try:
            # Fetch the text from the video
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            full_text = " ".join([t['text'] for t in transcript])
            
            # AI Summary Prompt
            prompt = f"Summarize this YouTube video transcript into clear bullet points: {full_text}"
            response = model.generate_content(prompt)
            summary = response.text
        except Exception as e:
            summary = f"Error: {str(e)}. (Check if the video has captions enabled)"
            
    return render_template('index.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
