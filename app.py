from flask import Flask, request, render_template_string
import lexer
import my_parser

app = Flask(__name__)

template = """
<!doctype html>
<title>Code Analyzer</title>
<h1>Analyze Your Code</h1>
<form action="" method=post>
  <textarea name=code rows=10 cols=40>{{ code }}</textarea><br>
  <input type=submit value=Analyze>
</form>
{% if analysis %}
    <h2>Analyzer Lexico</h2>
    <table border=1>
      <tr>
        <th>Tokens</th>
        <th>PR</th>
        <th>ID</th>
        <th>Numeros</th>
        <th>Simbolos</th>
        <th>Error</th>
      </tr>
    {% for row in analysis %}
      <tr>
        <td>{{ row.tokens }}</td>
        <td>{{ row.PR }}</td>
        <td>{{ row.ID }}</td>
        <td>{{ row.Numeros }}</td>
        <td>{{ row.Simbolos }}</td>
        <td>{{ row.Error }}</td>
      </tr>
    {% endfor %}
      <tr>
        <td>Total</td>
        <td>{{ total.PR }}</td>
        <td>{{ total.ID }}</td>
        <td>{{ total.Numeros }}</td>
        <td>{{ total.Simbolos }}</td>
        <td>{{ total.Error }}</td>
      </tr>
    </table>
{% if errors %}
    <h2>Errors</h2>
    <ul>
    {% for error in errors %}
        <li>{{ error }}</li>
    {% endfor %}
    </ul>
{% endif %}
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    code = ""
    analysis = []
    total = {"PR": 0, "ID": 0, "Numeros": 0, "Simbolos": 0, "Error": 0}
    errors = []
    if request.method == "POST":
        code = request.form["code"]
        lexer.lexer.input(code)
        tokens = []

        try:
            while True:
                tok = lexer.lexer.token()
                if not tok:
                    break
                tokens.append(tok)
                if tok.type in total:
                    total[tok.type] += 1
                else:
                    if tok.type in ["PLUS", "MINUS", "TIMES", "DIVIDE", "LPAREN", "RPAREN", "LBRACE", "RBRACE", "SEMI", "EQ", "LE", "GE", "LT", "GT", "NE"]:
                        total["Simbolos"] += 1
                    elif tok.type == "NUMBER":
                        total["Numeros"] += 1
                    elif tok.type == "ID":
                        total["ID"] += 1
                    elif tok.type in ["FOR", "PRINTLN"]:
                        total["PR"] += 1
            my_parser.parser.parse(code, lexer=lexer.lexer)
        except SyntaxError as e:
            errors.append(str(e))
            total["Error"] += 1

        for tok in tokens:
            analysis.append({
                "tokens": tok.type,
                "PR": 'x' if tok.type in ["FOR", "PRINTLN"] else '',
                "ID": 'x' if tok.type == "ID" else '',
                "Numeros": 'x' if tok.type == "NUMBER" else '',
                "Simbolos": 'x' if tok.type in ["PLUS", "MINUS", "TIMES", "DIVIDE", "LPAREN", "RPAREN", "LBRACE", "RBRACE", "SEMI", "EQ", "LE", "GE", "LT", "GT", "NE"] else '',
                "Error": 'x' if tok.type == "ERROR" else ''
            })

    return render_template_string(template, code=code, analysis=analysis, total=total, errors=errors)

if __name__ == "__main__":
    app.run(debug=True)
