# What's My Grade, Really

Calculate your actual grade based on your teacher's specific grading rules.

## Files

### Scores.csv
Contains your actual assignment, quiz, and exam scores:
- **Date**: When the assignment was due/taken
- **Category**: Type (Homework, Quiz, Midterm, Project, Final Exam)
- **Assignment**: Name of the work
- **Score**: Points earned
- **Max Points**: Total possible points
- **Percentage**: Your percentage on that item

### Grading_Policy.csv
Contains your teacher's grading rules:
- **Category Weights**: How much each category counts toward final grade
- **Special Rules**: Dropped scores, exam replacements, bonuses, penalties
- **Grade Scale**: Letter grade cutoffs

### grade_calculator.py
Python script that:
1. Reads your scores from Scores.csv
2. Applies your teacher's rules from Grading_Policy.csv
3. Calculates your current grade by category
4. Shows your overall weighted grade
5. Tells you what score you need on the final exam to reach target grades

## How to Use

### Step 1: Update Your Scores
Edit `Scores.csv` and add your real scores:
- Replace sample assignments with yours
- Keep the same format
- Set Final Exam score to 0 (or your actual score if you've taken it)

### Step 2: Update the Grading Policy
Edit `Grading_Policy.csv` with your teacher's rules:
- Category weights (must add up to 100%)
- Which scores get dropped
- Any special rules (exam replacements, bonuses, etc.)
- Your school's letter grade scale

### Step 3: Run the Calculator
```bash
python grade_calculator.py
```

This will show:
- Your grade in each category
- How drops and replacements affect your score
- Your current overall grade
- The exact score you need on remaining exams to reach target grades

## Example Output
```
GRADE CALCULATION SUMMARY
==================================================

HOMEWORK
  HW 1: 90.0%
  HW 2: 96.0%
  HW 3: 100.0%
  HW 4: 84.0%
  → Dropped lowest homework score
  Category Average: 94.00%

QUIZZES
  Quiz 1: 80.0%
  Quiz 2: 70.0%
  Quiz 3: 90.0%
  → Dropped lowest quiz score
  Category Average: 85.00%

OVERALL GRADE: 85.42%
Letter Grade: B

WHAT YOU NEED ON THE FINAL EXAM
To get an A (90%+): Need 96.3% on final exam
To get a B (80%+): Need 76.3% on final exam
To get a C (70%+): Need 56.3% on final exam
```

## Tips
- Run this regularly as you complete assignments to track your progress
- Use it to set realistic grade targets
- Understand exactly what you need before major exams
- Keep it updated throughout the semester
