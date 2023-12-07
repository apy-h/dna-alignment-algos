from flask import Flask, render_template, request
import main
from math import factorial

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get and validate user input
        input_type = request.form.get('input_type')
        if input_type == 'manual':
            seqs = request.form.get('sequences')
        else:
            seqs = request.files.get('csv').read().decode('utf-8')
        
        seqs = main.SequenceAlignment.validate_input(split_by_line(seqs.replace(' ', '')), True)

        num_seqs = len(seqs)
        num_combinations = factorial(num_seqs) / 2*factorial(num_seqs - 2)

        conn, c = main.open_database()

        main.get_results(seqs, c, True)
        
        # rows = c.execute("SELECT * FROM results ORDER BY time DESC").fetchall()
    
        # main.close_database(conn)

    return render_template('home.html')

def split_by_line(str):
    return str.replace('\r\n', '\n').split('\n')