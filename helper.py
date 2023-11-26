# Int representation of directions
class Direction:
    LEFT = 0
    UP = 1
    DIAGONAL = 2

# Return seq1 and seq2 (uppercased) if both only contain A, C, G, and T
# Raise exception otherwise
def validate_input(seq1, seq2):
    if not (is_valid_dna(seq1) and is_valid_dna(seq2)):
        raise SystemExit('One or both sequences are invalid (contain characters other than A, C, G, and T.)')
    
    return seq1.upper(), seq2.upper()


# Return true if seq only contains the letters A, C, G, and T
# Return false otherwise
def is_valid_dna(seq):
    return set(seq.upper()).issubset('ACGT')