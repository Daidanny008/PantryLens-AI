from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from processImage import get_groceries_from_image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    groceries = session.get('groceries', [])
    raw_text = session.get('raw_text', "")
    return render_template('PantryLensMain.html', groceries=groceries, raw_text=raw_text)

@app.route('/inventory')
def inventory():
    groceries = session.get('groceries', [])
    return render_template('Ingredients.html', groceries=groceries)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        raw_text, groceries = get_groceries_from_image(file_path)
        session['groceries'] = groceries
        session['raw_text'] = raw_text
        return render_template('PantryLensMain.html', groceries=groceries, raw_text=raw_text)
    return redirect(url_for('index'))

@app.route('/get_groceries', methods=['GET'])
def get_groceries():
    groceries = session.get('groceries', [])
    return jsonify(groceries)

if __name__ == '__main__':
    app.run()