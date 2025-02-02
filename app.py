from flask import Flask, render_template, request, redirect, url_for
from flask.templating import _render
from processImage import getGroceries, get_groceries_from_image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/')
def index():
    groceries = getGroceries()
    return render_template('PantryLensMain.html', groceries=groceries)

@app.route('/inventory')
def inventory():
    groceries = getGroceries()
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
        groceries = get_groceries_from_image(file_path)
        return render_template('PantryLensMain.html', groceries=groceries)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()