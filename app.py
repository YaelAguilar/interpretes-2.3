from flask import Flask, request, render_template
import analyzer

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        code = request.form['code']
        result = analyzer.analyze_code(code)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
