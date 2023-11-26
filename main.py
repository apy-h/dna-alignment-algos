import sys
from sequence_alignment import GlobalAlignment, LocalAlignment, SequenceAlignment

def main():
    if ((len(sys.argv) > 1 and sys.argv[1] in ['help', '--help', 'h', '-h']) or 
        len(sys.argv) != 3):
        raise SystemExit(f'Usage: {sys.argv[0]} [sequence 1] [sequence 2]')
    
    seq1, seq2 = SequenceAlignment.validate_input(sys.argv[1], sys.argv[2])
    ga = GlobalAlignment(seq1, seq2, 1, -1, -2)
    print(ga.align)


if __name__ == '__main__':
    main()