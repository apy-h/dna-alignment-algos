from flask import Flask, render_template, request
import csv
import sqlite3
# import your sequence alignment module

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get form data
        input_type = request.form.get('input_type')
        sequences = request.form.get('sequences')

        # Validate sequences
        if input_type == 'individual':
            sequences = sequences.split('\n')
            for seq in sequences:
                if not SequenceAlignment.is_valid_dna(seq):
                    return 'Invalid DNA sequence', 400
        elif input_type == 'csv':
            # Validate CSV file
            pass

        # Perform alignment algorithms
        # ...

        # Render results
        return render_template('results.html', results=results)
    else:
        return render_template('home.html')

@app.route('/database')
def database():
    # Connect to SQLite database
    conn = sqlite3.connect('results.db')
    c = conn.cursor()

    # Query database
    c.execute('SELECT * FROM results')
    data = c.fetchall()

    # Close connection
    conn.close()

    # Render data as table
    return render_template('database.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)