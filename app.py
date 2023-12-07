from flask import Flask, render_template, request
import main

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get and validate user input
        input_type = request.form.get('input_type')
        if input_type == 'manual':
            seqs = request.form.get('sequences').split('\r\n')
            print(seqs)
        else:
            seqs = request.files.get('csv').read().decode('utf-8')
            print(type(seqs))
            # main.read_csv(request.files.get('csv').read().decode())
        seqs = main.SequenceAlignment.validate_input(seqs)

        conn, c = main.open_database()

        main.get_results(seqs, c)
        
        rows = c.execute("SELECT * FROM results ORDER BY time DESC").fetchall()
    
        main.close_database(conn)

    return render_template('home.html') # , rows=None)