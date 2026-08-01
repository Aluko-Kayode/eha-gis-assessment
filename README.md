# eha-gis-assessment
# eHealth Africa GIS and Data Analytics Technical Assessment

This repository contains my submission for the Senior Coordinator, 
Data and GIS Analytics technical assessment.

## Questions attempted
- Part 1, Question 1: Campaign team tracking and coverage reconciliation
- Part 2, Question 3: Converting a paper questionnaire into a digital form
- Part 3, Question 5: Coordinating delivery through the round
- Part 3, Question 6: Building capability in the counterpart agency

## Scope note
Given the assessment window, this submission covers Part 1 Question 1 (full), Part 3 
Question 5 and Question 6 (compulsory, full), and Part 2 Question 3 (partial: paper 
questionnaire defects identified and specimen label check digit validation built and 
tested; XLSForm build and remaining written components not completed). Question 2 and 
Question 4 were not attempted, given the time available.

## How to reproduce results
Requires Python 3 with the packages listed in `requirements.txt` (`pip install -r requirements.txt`).

Run the following scripts in order from the project root:

1. `python scripts/01_load_inspect.py` — loads and combines all 160 GPS track files, 
   prints summary statistics
2. `python scripts/02_clean_flag.py` — fixes mixed timestamp formats, flags null island 
   points, missing accuracy readings, and implausible speed values
3. `python scripts/03_investigate_patterns.py` — checks whether flagged defects concentrate 
   in specific loggers or teams
4. `python scripts/04_visits_reconciliation.py` — matches GPS points to settlements, 
   reconciles against the e-tally, identifies missed settlements
5. `python scripts/05_cluster_and_map.py` — tests whether missed settlements are spatially 
   clustered and produces the A3 map (`maps/missed_settlements_map.png`)

The Question 1 coverage brief is at `maps/coverage_brief.md`. The Question 3 specimen 
label check digit validator, with test cases, is at `scripts/check_digit.py` and can be 
run standalone: `python scripts/check_digit.py`.

Written responses for Question 1, Question 5, and Question 6 are in 
`eHA_Written_Responses.pdf`, included in the submitted zip folder, not in this repository.

## Repository structure
- data/ raw input files
- scripts/ processing and analysis code
- outputs/ generated tables and cleaned data
- maps/ final PDF map products
