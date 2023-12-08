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
* `/templates/home.html`: where I create the backbone of my webpage
* `.gitignore`: list of files and folders for the version control system to not track
* `app.py`: where I define my webpage routes `/` (the bulk of the GUI) and `/download`, as well as where I use the values inputted in the form to perform the algorithms and interact with `results.db`
* `DESIGN.md`: this design document!
* `main.py`: where my CLI tool can be run from and where I define helper functions like `get_results()` that encapsulate many steps of my program
* [README.md](README.md): the user manual
* `results.db`: where I store a history of the results in a an SQLite3 database, with the following columns:
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

### Smith-Waterman algorithm for local alignment

***