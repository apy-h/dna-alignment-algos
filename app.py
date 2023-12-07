from flask import Flask, render_template, request
import main
from math import factorial


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    conn, c = main.open_database()

    # If form is submitted
    if request.method == 'POST':
        # Get and validate user input
        input_type = request.form.get('input_type')
        if input_type == 'manual':
            seqs = request.form.get('sequences')
        else:
            seqs = request.files.get('csv').read().decode()
        seqs = main.SequenceAlignment.validate_input(split_by_line(seqs.replace(' ', '')))

        print(f'Seqs: {seqs}')
        print(f'Number: {len(seqs)}')

        # Add results to database
        main.get_results(seqs, c)

    # Get all rows from database
    rows = c.execute("SELECT seq1, seq2, ga_align1, ga_align2, ga_score, la_align1, la_align2, la_score FROM results ORDER BY time DESC").fetchall()

    main.close_database(conn)

    return render_template('home.html', rows=rows)

# Return list representation of string split by newlines (and \r\n for compatibility)
def split_by_line(str):
    return str.replace('\r\n', '\n').split('\n')