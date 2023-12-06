from csv import reader, writer
from itertools import combinations
from math import factorial
import os
from sqlite3 import connect
import sys
from sequence_alignment import GlobalAlignment, LocalAlignment, SequenceAlignment

def main():
    seqs = user_input()
    print_line('*')

    # Connect to SQLite database
    conn = connect('results.db')
    c = conn.cursor()

    # Create table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS results (
            Sequence1 TEXT,
            Sequence2 TEXT,
            GlobalAlignment1 TEXT,
            GlobalAlignment2 TEXT,
            GlobalAlignmentScore INTEGER,
            LocalAlignment1 TEXT,
            LocalAlignment2 TEXT,
            LocalAlignmentScore INTEGER
        )
    ''')

    num_seqs = len(seqs)
    num_combinations = factorial(num_seqs) / 2*factorial(num_seqs - 2)
    
    print(f'Number of sequences: {num_seqs}')
    print(f'Number of combinations: {num_combinations}')
    print_line('*')

    # Get results from all combinations of sequences
    for seq1, seq2 in combinations(seqs, 2):
        ga = GlobalAlignment((seq1, seq2))
        la = LocalAlignment((seq1, seq2))

        ga_align1, ga_align2 = ga.align
        la_align1, la_align2 = la.align

        # Print results
        print(f'Sequence 1: {seq1}\nSequence 2: {seq2}\n')
        print(f'Global Alignment:\n\t{ga_align1}\n\t{ga_align2}\n\tAlignment Score: {ga.alignment_score}\n')
        print(f'Local Alignment:\n\t{la_align1}\n\t{la_align2}\n\tAlignment Score: {la.alignment_score}')
        print_line('-')

        # Add results to database
        c.execute('INSERT INTO results VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (seq1, seq2, ga_align1, ga_align2, ga.alignment_score, la_align1, la_align2, ga.alignment_score))

    conn.commit()
    conn.close()

    # # Save results to CSV file
    # with open('results.csv', 'w', newline='') as file:
    #     w = writer(file)
    #     w.writerow(['Sequence1', 'Sequence1', 'GlobalAlignment1', 'GlobalAlignment2', 'GlobalAlignmentScore', 'LocalAlignment1', 'LocalAlignment2', 'LocalAlignmentScore'])
    #     w.writerows(results)


def user_input():
    seqs = None
    if len(sys.argv) >= 3: # Command-line inputs
        seqs = sys.argv[1:]
    elif len(sys.argv) == 2:
        if sys.argv[1] in ['help', '--help', 'h', '-h']: # Help
            usage_help()
        elif os.path.isfile(sys.argv[1]) and os.path.splitext(sys.argv[1])[1].lower() == '.csv': # Valid CSV file input (should have each sequence on a new line)
            with open(sys.argv[1], 'r') as file:
                seqs = [row[0].strip() for row in reader(file)]
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

    return SequenceAlignment.validate_input(seqs)


def usage_help():
    raise SystemExit(f'Usage:\n'
          f'{sys.argv[0]} sequence1 sequence2  # Command-line inputs\n'
          f'{sys.argv[0]} filename.csv         # CSV file input\n'
          f'{sys.argv[0]}                      # Interactive inputs')


def print_line(c):
    print('\n' + c * 50 + '\n')
    

if __name__ == '__main__':
    main()