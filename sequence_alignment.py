from abc import ABC, abstractmethod
import numpy as np

#############################

class SequenceAlignment(ABC):
    # Private class variables: int representation of directions
    _LEFT = 0
    _UP = 1
    _DIAGONAL = 2
    _NO_DIRECTION = -1

    def __init__(self, seq1, seq2, MATCH=1, MISMATCH=-1, GAP=-2):
        self._seq1 = seq1
        self._seq2 = seq2
        self._align1 = None
        self._align2 = None
        self._n = len(seq1) + 1 # Number of rows of mat (height); seq1 is vertical axis
        self._m = len(seq2) + 1 # Number of columns of mat (width); seq2 is horizontal axis
        self._MATCH = MATCH
        self._MISMATCH = MISMATCH
        self._GAP = GAP
        self._initialize_matrix(self._n, self._m) # Instance variable mat


    # Create n by m structured NumPy matrix of int tuples (alignment score, direction score came from)
    # Note: data structure choosen for time/space efficiency and ease of use
    def _initialize_matrix(self, n, m):
        self.mat = np.zeros((n, m), dtype=[('score', 'i4'), ('direction', 'i1')])


    # Fill mat with score calculated as the max score of 3 or 4 possible alignment options:
    #   1. left_score + GAP: align seq2[i] with a gap in seq1 (horizontal movement over seq2)
    #   2. up_score + GAP: align seq1[j] with a gap in seq2 (vertical movement over seq1)
    #   3. diagonal_score + MATCH/MISMATCH): align seq1[i] with seq2[j] (movement over both)
    #   4. 0: if zero_floor (as in LocalAlignment)
    # Direction comes from the alignment option that yielded the max score
    # Note: if the 3/4 possible scores are the same, arbitarily choose direction as no direction (if zero_floor) -> left -> up -> diagonal, as this program only wants to return 1 possible best alignment
    def _fill_matrix(self, zero_floor):
        for i in range(1, self._n):
            for j in range(1, self._m):
                direction_scores = [self.mat['score'][i, j-1] + self._GAP, # Left
                                    self.mat['score'][i-1, j] + self._GAP, # Up
                                    self.mat['score'][i-1, j-1] + (self._MATCH if self._seq1[i-1] == self._seq2[j-1] else self._MISMATCH)] # Diagonal
                
                if zero_floor and not any(score > 0 for score in direction_scores):
                    max_score = 0
                    direction = self._NO_DIRECTION
                else:
                    max_score = max(direction_scores)
                    direction = direction_scores.index(max_score)
                
                self.mat[i, j] = (max_score, direction)
    

    @abstractmethod
    def _traceback(self):
        return '', ''
    

    # Given list of tuples [(x1, y1), (x2, y2), ...], return tuple of strings (x1x2..., y1y2...)
    @staticmethod
    def _tuple_list_to_strings(tuple_list):
        return ''.join(x[0] for x in tuple_list), ''.join(x[1] for x in tuple_list)


    # Return seq1 and seq2 (uppercased) if both only contain A, C, G, and T
    # Raise exception otherwise
    @staticmethod
    def validate_input(seq1, seq2):
        if not (SequenceAlignment._is_valid_dna(seq1) and SequenceAlignment._is_valid_dna(seq2)):
            raise SystemExit('One or both sequences are invalid (contain characters other than A, C, G, and T.)')
        
        return seq1.upper(), seq2.upper()


    # Return true if seq only contains the letters A, C, G, and T
    # Return false otherwise
    @staticmethod
    def _is_valid_dna(seq):
        return set(seq.upper()).issubset('ACGT')

    
    @property
    def align(self):
        return self._align1, self._align2

#############################

class GlobalAlignment(SequenceAlignment):
    def __init__(self, seq1, seq2, MATCH=1, MISMATCH=-1, GAP=-2):
        super().__init__(seq1, seq2, MATCH, MISMATCH, GAP)
        self._fill_matrix(False)
        self._traceback()


    # Set 1st row and column to (multiples of GAPs, point to top left)
    # Note: setting values of 1st row and column is usually part of fill_matrix(), but since it is standardized across all inputs, it is done here for efficiency
    def _initialize_matrix(self, n, m):
        super()._initialize_matrix(n, m)
        # Global alignment specific logic
        self.mat['score'][0, :] = [i*self._GAP for i in range(m)]  # Set 1st row score to multiples of GAP
        self.mat['direction'][0, :] = self._LEFT
        self.mat['score'][:, 0] = [i*self._GAP for i in range(n)]  # Set 1st column score to multiples of GAP
        self.mat['direction'][:, 0] = self._UP
        self.mat['direction'][0, 0] = self._NO_DIRECTION # Indicate top right cell isn't part of traceback
    

    # Create 2 strings that include all the nucleotides of seq1 and seq2 in their original order but with gaps (represented by -) inserted to maxmize alignment score
    def _traceback(self):
        alignment = [] # List of tuples (seq1[i] or -, seq2[j] or -)
        
        # Start at bottom right of mat
        i = self._n - 1
        j = self._m - 1
        
        # Follow the arrows of mat['direction'] until top left of mat is reached
        while i > 0 or j > 0:
            if self.mat['direction'][i, j] == self._DIAGONAL:
                alignment.append((self._seq1[i-1], self._seq2[j-1])) # Match
                i -= 1
                j -= 1
            elif self.mat['direction'][i, j] == self._LEFT:
                alignment.append(('-', self._seq2[j-1])) # Gap in seq1
                j -= 1
            else: # mat['direction'][i, j] == UP
                alignment.append((self._seq1[i-1], '-')) # Gap in seq2
                i -= 1
        
        alignment.reverse() # Since we started at bottom right of mat, reverse to right order
        
        self._align1, self._align2 = SequenceAlignment._tuple_list_to_strings(alignment)

#############################

class LocalAlignment(SequenceAlignment):
    def __init__(self, seq1, seq2, MATCH=1, MISMATCH=-1, GAP=-2):
        super().__init__(seq1, seq2, MATCH, MISMATCH, GAP)
        self._fill_matrix(True)
        self._traceback()


    def _traceback(self):
        pass