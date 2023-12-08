# DNA Alignment: Design Document

## File Structure

The main logic of my program is coded in Python, and I use the Flask framework with HTML, CSS, and JS to create the GUI.

```console
/dna-alignment
    /static
        favicon.png
        script.js
        style.css
    /templates
        home.html
    .gitingnore
    app.py
    DESIGN.md
    main.py
    README.md
    results.db
    sequence_alignment.py
    test_sequence_alignment.py
    test.csv
```

* `/static/favicon.png`: a PNG of a circle of DNA, used as the logo and loading sequence image
* `/static/script.js`: where I provide client-side functionalities like the tooltips for overflowed cells, ability to switch between "Manual Input" and "Upload CSV", client-side validification of inputs, and loading sequence
* `/static/style.css`: where I style my HTML webpage
* `/templates/home.html`: where I create the backbone of my webpage, including the form where users submit their sequences as input using the "Manual Input" or "Upload CSV" functionalities
* `.gitignore`: list of files and folders for the version control system to not track
* `app.py`: where I define my webpage routes `/` (the bulk of the GUI) and `/download`, as well as where I use the values inputted in the form to perform the algorithms and interact with `results.db`
* `DESIGN.md`: this design document!
* `main.py`: where my CLI tool can be run from and where I define helper functions like `get_results()` that encapsulate many steps of my program
* [README.md](README.md): the user manual
* `results.db`: where I store a history of the results in the `results` table of this SQLite3 database, with the following columns:
    * `seq1 TEXT NOT NULL`: Sequence 1
    * `seq2 TEXT NOT NULL`: Sequence 2
    * `ga_align1 TEXT`: Global Alignment 1
    * `ga_align2 TEXT`: Global Alignment 2
    * `ga_score INTEGER`: Global Alignment Score
    * `la_align1 TEXT`: Local Alignment 1
    * `la_align2 TEXT`: Local Alignment 2
    * `la_score INTEGER`: Local Alignment Score
    * `time DATETIME DEFAULT CURRENT_TIMESTAMP`: Timestamp
* `sequence_alignment.py`: where I define the abstract class `SequenceAlignment`, which the `GlobalAlignment` and `LocalAlignment` subclasses inherit from with all the necessary fields and methods to perform their respective algorithms
* `test_sequence_alignment.py`: where I define various unit test cases in `SAME_LENGTH_SEQ_CASES`, `DIFF_LENGTH_SEQ_CASES`, and `EMPTY_SEQ_CASES` to ensure that my program implements the algorithms properly
* `test.csv`: where I list 26 DNA sequences (20 valid, 6 invalid) of approximately 30-40 nucleotides in length to test my program with

***

## Algorithms

### Needleman-Wunsch Algorithm for Global Alignment

I will walk you through how this algorithm works step-by-step by using the sample inputs `seq1 = TGGTG` and `seq2 = ATCGT`.

1. Set `n` to one more than the number of nucleotides in `seq1`, so `n = 6`
2. Set `m` to one more than the number of nucleotides in `seq2`, so `m = 6`
3. Using `initialize_matrix()`, create an `n` by `m` matrix of 0s, where we can imagine the nucleotides of `seq1` along the vertical axis and the nucleotides of `seq2` along the horizontal axis

|   |   | A | T | C | G | T |
|---|---|---|---|---|---|---|
|   | 0 | 0 | 0 | 0 | 0 | 0 |
| T | 0 | 0 | 0 | 0 | 0 | 0 |
| G | 0 | 0 | 0 | 0 | 0 | 0 |
| G | 0 | 0 | 0 | 0 | 0 | 0 |
| T | 0 | 0 | 0 | 0 | 0 | 0 |
| G | 0 | 0 | 0 | 0 | 0 | 0 |

4. In `fill_matrix()`, starting from the top left cell, calculate the score of each cell as the maximum of:
    * The score of the cell to its left + a gap penalty (set to -2): this represents aligning the nucleotide in `seq2` with a gap in `seq1`, so we are moving horizontally over `seq2`    
    * The score of the cell above it + a gap penalty: this represents aligning the nucleotide in `seq1` with a gap in `seq2`, so we are moving vertically over `seq1` 
    * The score of the cell to its upper-left diagonal + a match reward if they nucleotides in `seq1` and `seq2` (set to 1) are the same or a mismatch penalty (set to -1) otherwise: this representings aligning the nucleotides of `seq1` and `seq2`
5. In each cell, also store the direction that the current cell's score was derived from (either left, up, or diagonal)

|  |  | A | T | C | G | T |
|-------|-------|-------|-------|-------|-------| -------|
|  | (0, -) | (-2, ←) | (-4, ←) | (-6, ←) | (-8, ←) | (-10, ←) |
| T | (-2, ↑) | (-1, ↖) | (-1, ↖) | (-3, ←) | (-5, ←) | (-7, ←) |
| G | (-4, ↑) | (-3, ↑) | (-2, ↖) | (-2, ↖) | (-2, ↖) | (-4, ←) |
| G | (-6, ↑) | (-5, ↑) | (-4, ↑) | (-3, ↖) | (-1, ↖) | (-3, ←) |
| T | (-8, ↑) | (-7, ↑) | (-4, ↖) | (-5, ↑) | (-3, ↑) | (0, ↖) |
| G | (-10, ↑) | (-9, ↑) | (-6, ↑) | (-5, ↖) | (-4, ↖) | (-2, ↑) |

6. In `traceback()`, start from bottom right cell and follow the arrows until top left, saving the nucleotides in each `seq1` and `seq2` or gaps (represented by `-`) in the case of horizontal/vertical movement as we go
7. Since we started from the bottom right and went to the top left, reverse the saved sequences to get `align1=-TGGTG` and `align2=ATCGT-`
8. In `set_alignment_score()`, set `alignment_score` to the value of the bottom right cell in the matrix; in this case `alignment_score = -2`

### Smith-Waterman Algorithm for Local Alignment

I will walk you through how this algorithm works step-by-step by using the same sample inputs `seq1 = TGGTG` and `seq2 = ATCGT`.

1. Set `n` to one more than the number of nucleotides in `seq1`, so `n = 6`
2. Set `m` to one more than the number of nucleotides in `seq2`, so `m = 6`
3. Using `initialize_matrix()`, create an `n` by `m` matrix of 0s, where we can imagine the nucleotides of `seq1` along the vertical axis and the nucleotides of `seq2` along the horizontal axis

|   |   | A | T | C | G | T |
|---|---|---|---|---|---|---|
|   | 0 | 0 | 0 | 0 | 0 | 0 |
| T | 0 | 0 | 0 | 0 | 0 | 0 |
| G | 0 | 0 | 0 | 0 | 0 | 0 |
| G | 0 | 0 | 0 | 0 | 0 | 0 |
| T | 0 | 0 | 0 | 0 | 0 | 0 |
| G | 0 | 0 | 0 | 0 | 0 | 0 |

4. In `fill_matrix()`, starting from the top left cell, calculate the score of each cell as the maximum of:
    * The score of the cell to its left + a gap penalty (set to -2): this represents aligning the nucleotide in `seq2` with a gap in `seq1`, so we are moving horizontally over `seq2`    
    * The score of the cell above it + a gap penalty: this represents aligning the nucleotide in `seq1` with a gap in `seq2`, so we are moving vertically over `seq1` 
    * The score of the cell to its upper-left diagonal + a match reward if they nucleotides in `seq1` and `seq2` (set to 1) are the same or a mismatch penalty (set to -1) otherwise: this representings aligning the nucleotides of `seq1` and `seq2`
    * `0`
5. In each cell, also store the direction that the current cell's score was derived from (either left, up, or none, represented by `-`)

|  |  | A | T | C | G | T |
|-------|-------|-------|-------|-------|-------| -------|
| | (0, 0) | (0, 0) | (0, 0) | (0, 0) | (0, 0) | (0, 0) |
| T | (0, 0) | (0, -) | (1, ↖) | (0, -) | (0, -) | (1, ↖) |
| G | (0, 0) | (0, -) | (0, -) | (0, -) | (1, ↖) | (0, -) |
| G | (0, 0) | (0, -) | (0, -) | (0, -) | (1, ↖) | (0, -) |
| T | (0, 0) | (0, -) | (1, ↖) | (0, -) | (0, -) | (2, ↖) |
| G | (0, 0) | (0, -) | (0, -) | (0, -) | (1, ↖) | (0, -) |

6. In `traceback()`, start from the cell with the highest score and follow the arrows until we reach a nonpositive score or a cell without an arrow, saving the nucleotides in each `seq1` and `seq2` or gaps (represented by `-`) in the case of horizontal/vertical movement as we go
7. Since we started from the bottom right and went to the top left, reverse the saved sequences to get `align1=GT` and `align2=GT`
8. In `set_alignment_score()`, set `alignment_score` to the score of the highest scoring cell, so `alignment_score = 2`

***

## Other

* In `main.py`, `get_results()` uses the `combinations()` method of the `itertools` libary to get all combinations of two sequences from all the inputted sequences to run the global and local alignment algorithms on. It saves the set of outputs for each combination of sequences in the `results` table of `results.db` and prints them to the console if it's being run as a CLI tool.
* In `app.py`, `home()` first connects to `results.db` and saves URL parameters about how to sort the table of results. Then, if the form has been submitted, it validates the inputs and runs `main.get_results()`. Next, whether the user has just navigated to the website or they have submitted the form, it gets all rows from `results` and sends them to be included in the HTML table using Jinja.