from flask import Flask, render_template, request
from flask.templating import _render

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('PantryLensMain.html')

@app.route('/inventory')
def inventory():
    return render_template('Ingredients.html')


#@app.route('/greet', methods=['POST'])
#def greet():
#    name = request.form['name']
#    return render_template('greet.html', name=name)


if __name__ == '__main__':
    app.run()