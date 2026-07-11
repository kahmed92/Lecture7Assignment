#!/usr/bin/env python3
"""
Grade Calculator - Calculate your actual grade based on teacher's specific rules
"""

import csv
from collections import defaultdict
from statistics import mean

def load_scores(filename):
    """Load scores from CSV file"""
    scores_by_category = defaultdict(list)

    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Category'].strip() and row['Score']:
                category = row['Category'].strip()
                try:
                    score = float(row['Score'])
                    max_points = float(row['Max Points'])
                    percentage = (score / max_points) * 100

                    scores_by_category[category].append({
                        'assignment': row['Assignment'].strip(),
                        'score': score,
                        'max_points': max_points,
                        'percentage': percentage
                    })
                except (ValueError, ZeroDivisionError):
                    continue

    return scores_by_category

def load_policy(filename):
    """Load grading policy from CSV file"""
    policy = {}
    current_section = None

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or not row[0].strip():
                continue

            if 'WEIGHTS' in row[0]:
                current_section = 'weights'
                policy['weights'] = {}
            elif 'SPECIAL RULES' in row[0]:
                current_section = 'rules'
                policy['rules'] = {}
            elif 'GRADE SCALE' in row[0]:
                current_section = 'grades'
                policy['grades'] = {}
            elif current_section == 'weights' and row[0] not in ['Category', 'CATEGORY WEIGHTS']:
                try:
                    weight = float(row[1].strip('%')) / 100
                    policy['weights'][row[0].strip()] = weight
                except (ValueError, IndexError):
                    pass
            elif current_section == 'rules' and row[0] not in ['Rule', '']:
                if len(row) >= 2:
                    policy['rules'][row[0].strip()] = row[1].strip()
            elif current_section == 'grades' and row[0] not in ['Grade', 'GRADE SCALE']:
                try:
                    min_grade = float(row[1])
                    max_grade = float(row[2])
                    policy['grades'][row[0].strip()] = (min_grade, max_grade)
                except (ValueError, IndexError):
                    pass

    return policy

def calculate_category_grade(scores, category_name):
    """Calculate average for a category, applying drop rules"""
    if not scores:
        return None

    percentages = [s['percentage'] for s in scores]

    # Apply drop rules
    if category_name == 'Homework' and len(percentages) > 1:
        percentages.remove(min(percentages))  # Drop lowest homework
        print(f"  → Dropped lowest homework score")
    elif category_name == 'Quizzes' and len(percentages) > 1:
        percentages.remove(min(percentages))  # Drop lowest quiz
        print(f"  → Dropped lowest quiz score")

    if percentages:
        return mean(percentages)
    return None

def calculate_grade(scores_file, policy_file):
    """Calculate overall grade based on policy"""
    scores = load_scores(scores_file)
    policy = load_policy(policy_file)

    print("=" * 70)
    print("GRADE CALCULATION SUMMARY")
    print("=" * 70)

    category_grades = {}

    # Calculate grade for each category
    for category in sorted(scores.keys()):
        print(f"\n{category.upper()}")
        print("-" * 70)

        for item in scores[category]:
            print(f"  {item['assignment']}: {item['percentage']:.1f}%")

        avg = calculate_category_grade(scores[category], category)
        if avg is not None:
            category_grades[category] = avg
            print(f"  Category Average: {avg:.2f}%")

    # Handle Final Exam replacement rule
    if 'Final Exam' in category_grades and 'Midterm' in category_grades:
        if category_grades['Final Exam'] > category_grades['Midterm']:
            print(f"\n📝 Final Exam ({category_grades['Final Exam']:.1f}%) > Midterm ({category_grades['Midterm']:.1f}%)")
            print(f"   → Final Exam replaces Midterm in calculation")
            category_grades['Midterm'] = category_grades['Final Exam']

    # Calculate weighted grade
    print(f"\n{'=' * 70}")
    print("WEIGHTED GRADE CALCULATION")
    print("=" * 70)

    total_weight = 0
    weighted_sum = 0

    for category, weight in policy.get('weights', {}).items():
        if category in category_grades:
            grade = category_grades[category]
            weighted = grade * weight
            weighted_sum += weighted
            total_weight += weight
            print(f"{category:20} {grade:6.2f}% × {weight*100:5.0f}% = {weighted:6.2f}%")

    if total_weight > 0:
        overall_grade = weighted_sum / total_weight
    else:
        overall_grade = 0

    print("-" * 70)
    print(f"{'OVERALL GRADE':20} {overall_grade:6.2f}%")
    print("=" * 70)

    # Determine letter grade
    for letter, (min_grade, max_grade) in sorted(policy.get('grades', {}).items()):
        if min_grade <= overall_grade <= max_grade:
            print(f"Letter Grade: {letter}")
            break

    return overall_grade, category_grades

def calculate_needed_score(current_grade, current_weight, target_grade, final_weight=20):
    """Calculate score needed on final exam to reach target grade"""
    # (current_grade * current_weight + final_score * final_weight) / total_weight = target
    # final_score = (target * total_weight - current_grade * current_weight) / final_weight

    total_weight = current_weight + final_weight
    needed = (target_grade * total_weight - current_grade * current_weight) / final_weight

    return max(0, min(100, needed))

def main():
    print("\n🎓 GRADE CALCULATOR")
    print("Based on your actual teacher's rules\n")

    try:
        overall_grade, category_grades = calculate_grade('Scores.csv', 'Grading_Policy.csv')

        # Calculate what's needed for different target grades
        print(f"\n{'=' * 70}")
        print("WHAT YOU NEED ON THE FINAL EXAM")
        print("=" * 70)

        # Calculate current grade without final exam
        current_weight = 100 - 20  # 80% without final
        current_grade = overall_grade

        for target in [90, 85, 80, 75]:
            needed = calculate_needed_score(current_grade, current_weight, target, final_weight=20)
            print(f"To get an A (90%+): Need {needed:.1f}% on final exam")
            print(f"To get a B (80%+): Need {needed:.1f}% on final exam")
            print(f"To get a C (70%+): Need {needed:.1f}% on final exam")
            break

        print("=" * 70)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Make sure Scores.csv and Grading_Policy.csv are in the same directory")

if __name__ == '__main__':
    main()
