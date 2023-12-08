# DNA Alignment: User's Manual

## Overview
I coded a program that enables biologists to score the similarity between DNA sequences and view the aligned portions. Given DNA sequences as [input](#input), the program [outputs](#output) a numerical and visual representation of their alignment.

It does this by implementing two algorithms for DNA alignment: the [Needleman-Wunsch algorithm for global alignment](DESIGN.md#needleman-wunsch-algorithm-for-global-alignment) and the [Smith-Waterman algorithm for local alignment](DESIGN.md#smith-waterman-algorithm-for-local-alignment). I describe both in detail in the [algorithms](DESIGN.md#algorithms) section of my [design document](DESIGN.md). The main takeaways are that one can either try to align two DNA sequences over all their nucleotides using the Needleman-Wunsch algorithm or look for portions of the inputted sequences that are closely aligned using the Smith-Waterman algorithm.

After [getting ready to to test my code](#set-up), try out its two methods of use: its [graphical user interface (GUI)](#gui) or [command-line interface (CLI)](#cli). I describe how to use both in detail in their respective sections.

***

## Input & Output

### Input

The user inputs two or more DNA sequences as their standard string representations, where `A` represents the nucleotide adenine, `T` represents thymine, `C` represents cytosine, and `G` represents guanine. For example, `GATTCGACGC` is a sample input  sequence with 10 nucleotides with two adenines, two thymines, three cytosines, and three guanines.

Depending on how the user is interacting with the program, they will either seperate each input sequence with either a single space or a newline. If the user is uploading a file as input, it must have the `.CSV` extension (case insensitive) and have each sequence on a newline with no other seperators.

### Output

Depending on the number of sequences the user inputs, the program will produce a different number of sets of outputs. The program produces one set of outputs for each combinations of two inputted sequences: for example, with `A`, `T`, and `C` as inputs, the combinations are {`A`, `T`}, {`A`, `C`}, and {`T`, `C`}, and each of the three combinations produces its own set of ouputs. Each set of outputs consists of the following:
* **Global Alignment 1**: this is string representation of a DNA sequence, potentially with gaps (represented by hyphens, `-`).
* **Global Alignment 2**: 
* **Global Alignment Score**: 
* **Local Alignment 1**: 
* **Local Alignment 2**: 
* **Local Alignment Score**: 

***

## Set-Up
To prepare to test the program:
1. Download the distribution code of the program
2. Upload the distribution code to Visual Studio Code (VSCode) or [cs50.dev](https://cs50.dev/)
3. Open a terminal window
4. Navigate to the root directory of my project called `/dna-alignment` using `cd`
5. Continue to the [GUI](#gui) or [CLI](#cli) section for instructions on how to use each respectively

***

## GUI

I created a website for my program to make the user experience more pleasant. It enables people from non-technical backgrounds to use the program and easily visualize its.

### Steps
6. Run `flask run` in the terminal
7. Click on the link that is printed to the console to navigate to the webpage, where you should see the words "DNA Alignment".
8. Click on the "Manual Input" radio button and try out the test cases marked as "Manual" listed below
9. Click on the "Upload CSV" file and try out the test cases marked as "CSV" listed below

### Test Cases
To validate the exact global and local alignment sequences and scores that the inputted sequences produce, feel free to use the Needleman-Wunsch and Smith-Waterman tools linked in the [resources section](#resources) with a match score of 1, mismatch score of -1, and gap score of -2, as is standard.

***

## CLI

I initially intended for my program to only have a CLI and no GUI. The CLI is good for program testing purposes and a quicker processing time.

### Steps
6. Run `python3 main.py help`, `python3 main.py --help`, `python3 main.py h`, or `python3 main.py -h` in the terminal. This will output to the console instructions on how to use the program:
```console
~/dna-alignment$ python3 main.py help
Usage:
python3 main.py sequence1 sequence2  # Command-line inputs
python3 main.py filename.csv         # CSV file input
python3 main.py                      # Interactive inputs
```
7. Try out the test cases marked by "Command-Line" listed below
8. Try out the test cases marked by "CSV" listed below
9. Try out the test cases marked by "Interactive" listed below
10. Try out the unit test cases marked by "Unit Tests" listed below

### Test Cases
Again, feel free to validate the exact outputs using the tools linked in the [resources section](#resources)!

| Type | Input | Expected Output | Explaination | Purpose |
| ---- | ----- | --------------- | ------------ | ------- |
| Command-Line | `python3 main.py ATCG ATTG` | One set of ouputs | The two inputted sequences are valid | Simple test case |
| Command-Line | `python3 main.py ATcg attG` | One set of ouputs | The two inputted sequences are valid | Proves program is case insensitive |
| Command-Line | `python3 main.py ATCG ATTGC ` | One sets of ouput | The two inputted sequences are valid | Proves that the inputted sequences can be different lenghts |
| Command-Line | `python3 main.py ATCG ATTGx ` | `Error: At least two valid DNA sequences are required` | The second sequence is invalid, so there is only one valid sequence | Proves that the program can handle errors |
| Command-Line | `python3 main.py ATCG ATTG ATGG` | Three sets of ouputs | The three inputted sequences are valid | Proves that the program can handle over two inputted sequences |
| CSV | `python3 main.py dne.csv` | `Error: dne.csv is not a valid CSV file` | `dne.csv` does not exist in the working directory | Proves that the program can handle errors |
| CSV | `python3 main.py app.py` | `Error: app.py is not a valid CSV file` | `app.py` is not a valid CSV file | Proves that the program can handle errors |
| CSV | `python3 main.py test.csv` | 190 sets of ouputs | 20 of the 26 inputted sequences are valid | Proves that the program can handle many test cases |
| Interactive | `python3 main.py` followed by `ATCG`, `ATTG`, a newline, then `done` | One set of outputs | The two inputted sequences are valid | Proves that the program can ignore newlines |
| Interactive | `python3 main.py` followed by `ATCG`, then `DOne` | `Error: At least two valid DNA sequences are required` | Only one valid input was provided | Proves that the program can handle errors and `done` is case insensitive |
| Interactive | `python3 main.py` followed by `ATCG`, `ATG C`, `GCTA`, then `d` | One set of outputs | The second sequence is invalid, so two valid inputs were provided | Proves that the program can handle errors and `d` works as well as `done` |
| Unit Tests | `python3 -m unittest -v test_sequence_alignment.TestGlobalAlignment` | `OK` (pass) | The program can handle input of the same length, different lengths, and having some empty inputs | Prove that the global alignment portion of the program works on individual sequence pairs |
| Unit Tests | `python3 -m unittest -v test_sequence_alignment.TestLocalAlignment` | `OK` (pass) | The program can handle input of the same length, different lengths, and having some empty inputs | Prove that the local alignment portion of the program works on individual sequence pairs |

***

### Resources:
* [Needleman-Wunsch Algorithm Wikipedia](https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm)
* [Smith-Waterman Algorithm Wikipedia](https://en.wikipedia.org/wiki/Smith%E2%80%93Waterman_algorithm)
* [Needleman-Wunsch Tool](https://bioboot.github.io/bimm143_W20/class-material/nw/)
* [Smith-Waterman Tool](https://rna.informatik.uni-freiburg.de/Teaching/index.jsp?toolName=Smith-Waterman)
* [Needleman-Wunsch Algorithm Video Walkthrough](https://www.youtube.com/watch?v=of3B02hZGS0)
* [Smith-Waterman Algorithm Video Walkthrough 1](https://www.youtube.com/watch?v=te_csPu5lmM)
* [Smith-Waterman Algorithm Video Walkthrough 2](https://www.youtube.com/watch?v=sSJYxzeFfWU)

***

**Generative AI Use Disclaimer**: I used CS50's Duck Debugger (DDB) and OpenAI's ChatGPT to help brainstorm ideas for my final project. I used ChatGPT to help teach me how the two algorithms work and write psuedocode for each. I used GitHub Copilot to help in the coding, testing, debugging, and commenting process.