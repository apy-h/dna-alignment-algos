import csv
import os
import sys
from sequence_alignment import GlobalAlignment, LocalAlignment, SequenceAlignment

def main():
    seq1 = seq2 = None
    if len(sys.argv) == 3: # Command-line inputs
        seq1, seq2 = sys.argv[1], sys.argv[2]
    elif len(sys.argv) == 2:
        if sys.argv[1] in ['help', '--help', 'h', '-h']: # Help
            usage_help()
        elif os.path.isfile(sys.argv[1]) and os.path.splitext(sys.argv[1])[1].lower() == '.csv': # Valid CSV file input
            with open(sys.argv[1], 'r') as file:
                seq1, seq2 = next(csv.reader(file))
        else: # Invalid CSV file input
            raise SystemExit(f'Error: {sys.argv[1]} is not a valid CSV file')
    elif len(sys.argv) == 1: # Execution-time inputs
        seq1 = input('Sequence 1: ')
        seq2 = input('Sequence 2: ')
    else: # Help
        usage_help()

    seq = SequenceAlignment.validate_input(seq1, seq2)
    
    ga = GlobalAlignment(seq)
    la = LocalAlignment(seq)

def usage_help():
    raise SystemExit(f'Usage:\n'
          f'{sys.argv[0]} sequence1 sequence2  # Command-line inputs\n'
          f'{sys.argv[0]} filename.csv         # CSV file input\n'
          f'{sys.argv[0]}                      # Interactive inputs')

if __name__ == '__main__':
    main()