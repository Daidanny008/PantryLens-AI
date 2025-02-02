from flask import Flask, render_template, request
from flask.templating import _render
from processImage import getGroceries


app = Flask(__name__)


@app.route('/')
def index():
    groceries = getGroceries()
    return render_template('PantryLensMain.html', groceries=groceries)

@app.route('/inventory')
def inventory():
    return render_template('Ingredients.html')

if __name__ == '__main__':
    app.run()