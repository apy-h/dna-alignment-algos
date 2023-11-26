import numpy as np
from helper import Direction

MATCH = 1
MISMATCH = -1
GAP = -2


def global_alignment(seq1, seq2):
    mat = initialize_matrix(len(seq1) + 1, len(seq2) + 1)
    mat = fill_matrix(mat, seq1, seq2)
    x = traceback(mat, seq1, seq2)
    print(mat)
    print(x)
    return x


# Return n by m matrix of int tuples (alignment score, direction score came from)
# Cells hold (0, 0) except for 1st row and column (multiples of GAPs, point to top left)
# Note: setting values of 1st row and column is usually part of fill_matrix(), but since it is standardized across all inputs, it is done here for efficiency
def initialize_matrix(n, m):
    # Create structured NumPy matrix (structure choosen for time/space efficiency and usability)
    mat = np.zeros((n, m), dtype=[('score', 'i4'), ('direction', 'i1')])
    mat['score'][0, :] = [i*GAP for i in range(m)]  # Set 1st row score to multiples of GAP
    mat['direction'][0, :] = Direction.LEFT
    mat['score'][:, 0] = [i*GAP for i in range(n)]  # Set 1st column score to multiples of GAP
    mat['direction'][:, 0] = Direction.UP
    mat['direction'][0, 0] = -1 # To indicate top right cell isn't part of traceback
    return mat


# Return n by m matrix of int tuples (score, direction)
def fill_matrix(mat, seq1, seq2):
    n, m = mat.shape
    # Start at 1 since 1st row and column were already filled in initialize_matrix()
    for i in range(1, n):
        for j in range(1, m):
            mat[i, j] = calculate_cell(mat['score'][i, j-1], 
                                       mat['score'][i-1, j], 
                                       mat['score'][i-1, j-1], 
                                       seq1[i-1] == seq2[j-1])
    return mat


# Return int tuple (score, direction) for the cell at (i, j)
# Score is calculated as the max score of 3 possible alignment options:
#   1. left_score + GAP: align seq1[i] with a gap in seq2 (horizontal movement over seq1)
#   2. up_score + GAP: align seq2[j] with a gap in seq1 (vertical movement over seq2)
#   3. diagonal_score + MATCH/MISMATCH): align seq1[i] with seq2[j] (movement over both)
# Direction comes from the alignment option that yielded the max score
# Note: if the 3 possible scores are the same, arbitarily choose direction as left over up over diagonal because this program only wants to return 1 possible best alignment
def calculate_cell(left_score, up_score, diagonal_score, is_match):
    direction_scores = [left_score + GAP, 
                        up_score + GAP, 
                        diagonal_score + (MATCH if is_match else MISMATCH)]

    max_score = max(direction_scores)
    direction = direction_scores.index(max_score)

    return max_score, direction

# Return string tuple (seq1 with gaps, seq2 with gaps) representing aligned sequences
# Note: gaps are represented by -
def traceback(mat, seq1, seq2):
    alignment = [] # List of tuples (seq1[i] or -, seq2[j])
    i, j = len(seq1), len(seq2)
    while i > 0 or j > 0:
        if mat['direction'][i, j] == Direction.DIAGONAL:
            alignment.append((seq1[i-1], seq2[j-1]))
            i -= 1
            j -= 1
        elif mat['direction'][i, j] == Direction.LEFT:  # Changed this line
            alignment.append(('-', seq2[j-1]))
            j -= 1
        else: # mat['direction'][i, j] == Direction.UP or i > 0  # And this line
            alignment.append((seq1[i-1], '-'))
            i -= 1
    alignment.reverse()
    str1 = ''.join(x[0] for x in alignment)
    str2 = ''.join(x[1] for x in alignment)
    return str1, str2