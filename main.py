from csv import reader
from itertools import combinations
import os
from sqlite3 import connect
import sys
from sequence_alignment import GlobalAlignment, LocalAlignment, SequenceAlignment


def main():
    # Get input from CLI program
    seqs = cli_input()
    print_line('*')

    conn, c = open_database()

    num_seqs = len(seqs)
    num_combinations = int(num_seqs * (num_seqs - 1) / 2)  # Combination formula for k=2

    print(f'Number of sequences: {num_seqs}')
    print(f'Number of combinations: {num_combinations}')
    print_line('*')

    # Save results to database and print them
    get_results(seqs, c, True)

    close_database(conn)


# Save alignment results from all combinations of sequences to database
# (And print them if program is being run as CLI tool)
def get_results(seqs, c, cli=False):
    for seq1, seq2 in combinations(seqs, 2):
        ga = GlobalAlignment((seq1, seq2))
        la = LocalAlignment((seq1, seq2))

        ga_align1, ga_align2 = ga.align
        la_align1, la_align2 = la.align

        c.execute('INSERT INTO results (seq1, seq2, ga_align1, ga_align2, ga_score, la_align1, la_align2, la_score) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (seq1, seq2, ga_align1, ga_align2, int(ga.alignment_score), la_align1, la_align2, int(la.alignment_score)))

        if cli:
            print(f'Sequence 1: {seq1}\nSequence 2: {seq2}\n')
            print(f'Global Alignment:\n\t{ga_align1}\n\t{ga_align2}\n\tAlignment Score: {ga.alignment_score}\n')
            print(f'Local Alignment:\n\t{la_align1}\n\t{la_align2}\n\tAlignment Score: {la.alignment_score}')
            print_line('-')


def cli_input():
    seqs = []
    if len(sys.argv) >= 3: # Command-line inputs
        seqs = sys.argv[1:]
    elif len(sys.argv) == 2:
        if sys.argv[1] in ['help', '--help', 'h', '-h']: # Help
            usage_help()
        elif os.path.isfile(sys.argv[1]) and os.path.splitext(sys.argv[1])[1].lower() == '.csv': # Valid CSV file input (should have each sequence on a new line)
            with open(sys.argv[1], 'r') as file:
                seqs = [row[0].strip() for row in reader(file) if row]
        else: # Invalid CSV file input
            raise SystemExit(f'Error: {sys.argv[1]} is not a valid CSV file')
    elif len(sys.argv) == 1: # Execution-time inputs
        while True:
            seq = input('Enter a sequence (or "done" to proceed): ')
            if seq.lower() in ['done', 'd']:
                break
            seqs.append(seq)
    else: # Help
        usage_help()

    return SequenceAlignment.validate_input(seqs, True)


# Raise exception that provides input format
def usage_help():
    raise SystemExit(f'Usage:\n'
          f'python3 {sys.argv[0]} sequence1 sequence2  # Command-line inputs\n'
          f'python3 {sys.argv[0]} filename.csv         # CSV file input\n'
          f'python3 {sys.argv[0]}                      # Interactive inputs')


# Create database connection and create results table if needed
def open_database():
    conn = connect('results.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS results (
            seq1 TEXT NOT NULL,
            seq2 TEXT NOT NULL,
            ga_align1 TEXT,
            ga_align2 TEXT,
            ga_score INTEGER,
            la_align1 TEXT,
            la_align2 TEXT,
            la_score INTEGER,
            time DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    return conn, c


def close_database(conn):
    conn.commit()
    conn.close()


# Print the character c n times, surronded by newlines on both sides
def print_line(c, n=50):
    print('\n' + c * n + '\n')
    

if __name__ == '__main__':
    main()