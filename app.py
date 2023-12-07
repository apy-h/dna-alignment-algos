from flask import Flask, Response, render_template, request, send_file
import main


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    conn, c = main.open_database()
    error = None

    # Get URL parameters for sorting table of results
    sort_column = request.args.get('sort_column', default='time', type=str)
    sort_order = request.args.get('sort_order', default='DESC', type=str)

    # If form is submitted
    if request.method == 'POST':
        # Get and validate user input
        input_type = request.form.get('input_type')
        if input_type == 'manual':
            seqs = request.form.get('sequences')
        else:
            seqs = request.files.get('csv').read().decode()
        
        seqs = main.SequenceAlignment.validate_input(split_by_line(seqs.replace(' ', '')))
        
        # If invalid input (less than 2 valid sequences), display error message
        if isinstance(seqs, Response) and seqs.status_code == 400:
            error = seqs.json['error']
        else:
            main.get_results(seqs, c) # Get new results to add to database

    # Get all rows from database
    rows = c.execute(f'SELECT * FROM results ORDER BY {sort_column} {sort_order}').fetchall()

    main.close_database(conn)

    return render_template('home.html', rows=rows, error=error)


# Download database of results
@app.route('/download')
def download_results():
    return send_file('results.db', as_attachment=True)


# Return list representation of string split by newlines (and \r\n for compatibility)
def split_by_line(str):
    return str.replace('\r\n', '\n').split('\n')