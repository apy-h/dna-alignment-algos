from flask import Flask, Response, render_template, request, send_file, jsonify
import main
import csv
import io
import os


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

    # Get all rows from database with row IDs
    rows = c.execute(f'SELECT rowid, * FROM results ORDER BY {sort_column} {sort_order}').fetchall()

    main.close_database(conn)

    return render_template('home.html', rows=rows, error=error, sort_column=sort_column, sort_order=sort_order)


# Download results as CSV
@app.route('/download')
def download_results():
    conn, c = main.open_database()
    rows = c.execute('SELECT * FROM results ORDER BY time DESC').fetchall()
    main.close_database(conn)
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Sequence 1', 'Sequence 2', 'Global Alignment 1', 'Global Alignment 2', 
                     'Global Score', 'Local Alignment 1', 'Local Alignment 2', 'Local Score', 'Timestamp'])
    
    # Write data
    for row in rows:
        writer.writerow(row)
    
    # Prepare response
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=results.csv'}
    )


# Download selected results as CSV
@app.route('/download_selected', methods=['POST'])
def download_selected():
    data = request.get_json()
    row_ids = data.get('rowIds', [])
    
    if not row_ids:
        return jsonify({'error': 'No rows selected'}), 400
    
    conn, c = main.open_database()
    
    # Create placeholders for SQL IN clause
    placeholders = ','.join('?' * len(row_ids))
    query = f'SELECT * FROM results WHERE rowid IN ({placeholders}) ORDER BY time DESC'
    rows = c.execute(query, row_ids).fetchall()
    main.close_database(conn)
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Sequence 1', 'Sequence 2', 'Global Alignment 1', 'Global Alignment 2', 
                     'Global Score', 'Local Alignment 1', 'Local Alignment 2', 'Local Score', 'Timestamp'])
    
    # Write data
    for row in rows:
        writer.writerow(row)
    
    # Prepare response
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=selected_results.csv'}
    )


# Download all except selected results as CSV
@app.route('/download_except_selected', methods=['POST'])
def download_except_selected():
    data = request.get_json()
    row_ids = data.get('rowIds', [])
    
    conn, c = main.open_database()
    
    if row_ids:
        # Create placeholders for SQL NOT IN clause
        placeholders = ','.join('?' * len(row_ids))
        query = f'SELECT * FROM results WHERE rowid NOT IN ({placeholders}) ORDER BY time DESC'
        rows = c.execute(query, row_ids).fetchall()
    else:
        # If no rows selected, export all
        rows = c.execute('SELECT * FROM results ORDER BY time DESC').fetchall()
    
    main.close_database(conn)
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Sequence 1', 'Sequence 2', 'Global Alignment 1', 'Global Alignment 2', 
                     'Global Score', 'Local Alignment 1', 'Local Alignment 2', 'Local Score', 'Timestamp'])
    
    # Write data
    for row in rows:
        writer.writerow(row)
    
    # Prepare response
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=unselected_results.csv'}
    )


# Delete a single row
@app.route('/delete_row/<int:row_id>', methods=['POST'])
def delete_row(row_id):
    conn, c = main.open_database()
    c.execute('DELETE FROM results WHERE rowid = ?', (row_id,))
    conn.commit()
    main.close_database(conn)
    return jsonify({'success': True})


# Delete selected rows
@app.route('/delete_selected', methods=['POST'])
def delete_selected():
    data = request.get_json()
    row_ids = data.get('rowIds', [])
    
    if not row_ids:
        return jsonify({'error': 'No rows selected'}), 400
    
    conn, c = main.open_database()
    placeholders = ','.join('?' * len(row_ids))
    c.execute(f'DELETE FROM results WHERE rowid IN ({placeholders})', row_ids)
    conn.commit()
    main.close_database(conn)
    
    return jsonify({'success': True, 'count': len(row_ids)})


# Clear all database rows
@app.route('/clear_database', methods=['POST'])
def clear_database():
    conn, c = main.open_database()
    c.execute('DELETE FROM results')
    conn.commit()
    main.close_database(conn)
    return jsonify({'success': True})


# Return list representation of string split by newlines (and \r\n for compatibility)
def split_by_line(str):
    return str.replace('\r\n', '\n').split('\n')