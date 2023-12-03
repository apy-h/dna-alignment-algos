from csv import reader
from itertools import combinations
import os
import sys
from sequence_alignment import GlobalAlignment, LocalAlignment, SequenceAlignment

def main():
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

    seqs = SequenceAlignment.validate_input(seqs)

    # Generate all combinations of sequences
    for seq1, seq2 in combinations(seqs, 2):
        ga = GlobalAlignment((seq1, seq2))
        la = LocalAlignment((seq1, seq2))


def usage_help():
    raise SystemExit(f'Usage:\n'
          f'{sys.argv[0]} sequence1 sequence2  # Command-line inputs\n'
          f'{sys.argv[0]} filename.csv         # CSV file input\n'
          f'{sys.argv[0]}                      # Interactive inputs')

if __name__ == '__main__':
    main()