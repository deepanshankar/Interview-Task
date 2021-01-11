# Interview-Task
Project to parse input files and generate report and summary


# Instructions to run the programs:

Please have the following files in the "Interview Task" folder:

error_codes.json
input_file.txt
standard_definition.json

The "src" folder contains the main source code in "assignment.py" file, which reads input file and parses the inputs
to calculate the error codes.

You can run the assignment.py file in "src" folder in preferred IDE or in command line by traversing to "src" folder
and run "python assignment.py".

The formed report is stored in "parsed/report.csv" and summary is stored in "parsed/summary.txt"

Once program assignment.py has completed its execution, the results are stored in "parsed" folder
and logs are stored in "logs/summary.log" by replacing any previous logs.

# Unit Testing:

The "test" folder contains "unit_test.py" file, where the unit testing is done

You can run "unit_test.py" in preferred IDE or in command line by traversing to "test" folder
and run "python -m unittest -v unit_test.py" to check the methods passed and failed

Also the logs are stored in "logs/summary.log" by replacing previous logs.
