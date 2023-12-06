from csv import reader, writer
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

    print_line('*')

    results = [] # List of tuples (seq1, seq2, ga_align1, ga_align2, ga_alignment_score, la_align1, la_align2, la_alignment_score)
    num_combinations = 0
    
    # Generate all combinations of sequences
    for seq1, seq2 in combinations(seqs, 2):
        num_combinations += 1

        ga = GlobalAlignment((seq1, seq2))
        la = LocalAlignment((seq1, seq2))

        ga_align1, ga_align2 = ga.align
        la_align1, la_align2 = la.align

        results.append((seq1, seq2, ga_align1, ga_align2, ga.alignment_score, la_align1, la_align2, ga.alignment_score))
    
    # Print results
    print(f'Number of sequences: {len(seqs)}')
    print(f'Number of combinations: {num_combinations}')
    print_line('*')

    for result in results:
        print(f'Sequence 1: {result[0]}\nSequence 2: {result[1]}\n')
        print(f'Global Alignment:\n\t{result[2]}\n\t{result[3]}\n\tAlignment Score: {result[4]}\n')
        print(f'Local Alignment:\n\t{result[5]}\n\t{result[6]}\n\tAlignment Score: {result[7]}')
        print_line('-')

    # Save results to CSV file
    with open('results.csv', 'w', newline='') as file:
        w = writer(file)
        w.writerow(['Sequence1', 'Sequence1', 'GlobalAlignment1', 'GlobalAlignment2', 'GlobalAlignmentScore', 'LocalAlignment1', 'LocalAlignment2', 'LocalAlignmentScore'])
        w.writerows(results)


def usage_help():
    raise SystemExit(f'Usage:\n'
          f'{sys.argv[0]} sequence1 sequence2  # Command-line inputs\n'
          f'{sys.argv[0]} filename.csv         # CSV file input\n'
          f'{sys.argv[0]}                      # Interactive inputs')

def print_line(c):
    print('\n' + c * 50 + '\n')

if __name__ == '__main__':
    main()