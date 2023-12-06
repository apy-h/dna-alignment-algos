from flask import Flask, render_template, request
import csv
import sqlite3
from sequence_alignment import GlobalAlignment, LocalAlignment, SequenceAlignment

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
    
    # Fetch data from the database
    # conn = sqlite3.connect('results.db')
    # c = conn.cursor()
    # c.execute("SELECT * FROM results ORDER BY GlobalAlignmentScore DESC")
    # rows = c.fetchall()
    # conn.close()

    return render_template('home.html') # , rows=None)