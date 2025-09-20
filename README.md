AUTOMATED-OMR-EVALUATION SYSTEM:
The Automated OMR Sheet Evaluation System is a web-based tool that evaluates OMR sheets quickly and accurately.
It supports multiple exam versions, calculates per-subject and total scores, and exports results as CSV.
The system reduces evaluation time from days to minutes while maintaining high accuracy.

Problem Statement
•	Current Challenge
o	Manual evaluation of OMR sheets is time-consuming especially for exams with large numbers of students
o	Human evaluation is prone to errors such as misreading marks or miscalculating scores
o	Multiple versions of the same exam increase the complexity of evaluation

•	Impact
o	Evaluators spend days or weeks completing the grading process
o	Delays in results affect student feedback and learning
o	Errors in scoring can lead to inaccurate assessments impacting student performance evaluations

•	Goal of the Project
o	Build a fully automated OMR evaluation system
o	Ensure accuracy less than 0.5 percent error tolerance and speed
o	Handle multiple exam versions and large batches of sheets
o	Provide a web-based interface for easy use by evaluators
o	Allow evaluators to focus on analyzing results and student insights rather than manual grading

•	Key Objectives
1.	Accept OMR sheets as images captured via mobile phone cameras
2.	Detect and evaluate filled bubbles accurately
3.	Compute per-subject scores and total scores
4.	Support CSV export for batch result analysis
5.	Reduce evaluation turnaround from days to minutes while maintaining high accuracy
6.	
Approach

•	Image Processing
o	Detect and crop the OMR sheet
o	Correct perspective for mobile captures

•	Bubble Detection
o	Divide sheet into cells for each question
o	Detect filled bubbles via thresholding and pixel analysis

•	Answer Key Comparison
o	Upload answer key as an image
o	Extract answers using bubble detection
o	Compare student sheets with answer key

•	Scoring and Output
o	Calculate per-subject and total scores
o	Display results with score cards and progress bars
o	Export results as CSV


Usage
•	Step 1 Upload answer key sheet image in JPG or PNG format
•	Step 2 Upload student OMR sheets in JPG or PNG format
•	Step 3 Select sheet version from sidebar
•	Step 4 Click Evaluate Sheets
•	Step 5 View score cards and progress bars
•	Step 6 Download CSV file of results

Subjects
•	Python
•	EDA
•	SQL
•	POWER BI
•	Statistics

Folder Structure
•	OMR-Evaluation-System folder contains
o	main.py Streamlit web app
o	omr_core.py OMR detection and evaluation logic
o	style.py Website styling
o	runtest.py Optional testing script
o	requirements.txt Python dependencies
o	README.md Project documentation

Future Enhancements
•	Preview detected bubbles on uploaded sheets
•	Support dynamic number of questions and subjects
•	Database integration for automated result storage
