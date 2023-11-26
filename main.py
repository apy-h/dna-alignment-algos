import sys
from helper import validate_input
from global_alignment import global_alignment

def main():
    if ((len(sys.argv) > 1 and sys.argv[1] in ['help', '--help', 'h', '-h']) or 
        len(sys.argv) != 3):
        raise SystemExit(f'Usage: {sys.argv[0]} [sequence 1] [sequence 2]')
    
    seq1, seq2 = validate_input(sys.argv[1], sys.argv[2])
    return global_alignment(seq1, seq2)


if __name__ == '__main__':
    main()