from flask import Flask, render_template, request
import main

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get and validate user input
        input_type = request.form.get('input_type')
        if input_type == 'manual':
            seqs = request.form.get('sequences').split('\n')
        else:
            print('0' * 100)
            print(request.files.get('csv'))

            seqs = main.read_csv(request.files.get('csv'))
        seqs = main.SequenceAlignment.validate_input(seqs)

        conn, c = main.open_database()

        main.get_results(seqs, c)
        
        rows = c.execute("SELECT * FROM results ORDER BY Timestamp DESC").fetchall()

        print(rows)
    
        main.close_database(conn)

    return render_template('home.html') # , rows=None)