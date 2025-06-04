from flask import Flask, request, send_file, render_template
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    img_file = request.files['image']
    target_format = request.form['format'].lower()

    img = Image.open(img_file.stream)

    if target_format == 'jpg' or target_format == 'jpeg':
        img = img.convert('RGB')  # JPEG doesn't support transparency

    img_io = io.BytesIO()
    img.save(img_io, format=target_format.upper())
    img_io.seek(0)

    return send_file(
        img_io,
        mimetype=f'image/{target_format}',
        as_attachment=True,
        download_name=f'converted_image.{target_format}'
    )

if __name__ == '__main__':
    app.run(debug=True)
