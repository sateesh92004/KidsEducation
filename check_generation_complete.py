"""
Check if all Algebra questions have been generated and loaded into database
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from database.db_manager import db

# Expected topics from the syllabus
EXPECTED_TOPICS = {
    "Chapter 2: Functions, Equations, and Graphs": [
        "2-1 Relations and Functions",
        "2-2 Direct Variation",
        "2-3 Linear Functions and Slope-Intercept Form",
        "2-4 More About Linear Equations",
        "2-5 Using Linear Models",
        "2-6 Families of Functions",
        "2-7 Absolute Value Functions and Graphs",
        "2-8 Two-Variable Inequalities",
        "Concept Byte: Piecewise Functions"
    ],
    "Chapter 3: Linear Systems": [
        "3-1 Solving Systems Using Tables and Graphs",
        "3-2 Solving Systems Algebraically",
        "3-3 Systems of Inequalities",
        "3-4 Linear Programming",
        "3-5 Systems With Three Variables",
        "3-6 Solving Systems Using Matrices",
        "Concept Byte TECHNOLOGY: Linear Programming",
        "Concept Byte ACTIVITY: Graphs in Three Dimensions"
    ],
    "Chapter 4: Quadratic Functions and Equations": [
        "4-1 Quadratic Functions and Transformations",
        "4-2 Standard Form of a Quadratic Function",
        "4-3 Modeling With Quadratic Functions",
        "4-4 Factoring Quadratic Expressions",
        "4-5 Quadratic Equations",
        "4-6 Completing the Square",
        "4-7 The Quadratic Formula",
        "4-8 Complex Numbers",
        "4-9 Quadratic Systems",
        "Concept Byte: Identifying Quadratic Data",
        "Concept Byte: Writing Equations From Roots",
        "Concept Byte: Quadratic Inequalities",
        "Concept Byte EXTENSION: Powers of Complex Numbers",
        "Algebra Review: Square Roots and Radicals"
    ],
    "Chapter 5: Polynomials and Polynomial Functions": [
        "5-1 Polynomial Functions",
        "5-2 Polynomials, Linear Factors, and Zeros",
        "5-3 Solving Polynomial Equations",
        "5-4 Dividing Polynomials",
        "5-5 Theorems About Roots of Polynomial Equations",
        "5-6 The Fundamental Theorem of Algebra",
        "5-7 The Binomial Theorem",
        "5-8 Polynomial Models in the Real World",
        "5-9 Transforming Polynomial Functions",
        "Concept Byte EXTENSION: Using Polynomial Identities",
        "Concept Byte ACTIVITY: Graphing Polynomials Using Zeros"
    ],
    "Chapter 6: Radical Functions and Rational Exponents": [
        "6-1 Roots and Radical Expressions",
        "6-2 Multiplying and Dividing Radical Expressions",
        "6-3 Binomial Radical Expressions",
        "6-4 Rational Exponents",
        "6-5 Solving Square Root and Other Radical Equations",
        "6-6 Function Operations",
        "6-7 Inverse Relations and Functions",
        "6-8 Graphing Radical Functions",
        "Concept Byte REVIEW: Properties of Exponents",
        "Concept Byte TECHNOLOGY: Graphing Inverses"
    ],
    "Chapter 7: Exponential and Logarithmic Functions": [
        "7-1 Exploring Exponential Models",
        "7-2 Properties of Exponential Functions",
        "7-3 Logarithmic Functions as Inverses",
        "7-4 Properties of Logarithms",
        "7-5 Exponential and Logarithmic Equations",
        "7-6 Natural Logarithms",
        "7-7 Transforming Exponential and Logarithmic Functions",
        "7-8 Curve Fitting with Exponential and Logarithmic Models"
    ],
    "Chapter 8: Rational Functions": [
        "8-1 Inverse Variation",
        "8-2 The Reciprocal Function Family",
        "8-3 Rational Functions and Their Graphs",
        "8-4 Rational Expressions",
        "8-5 Adding and Subtracting Rational Expressions",
        "8-6 Solving Rational Equations",
        "8-7 Probability Models",
        "Concept Byte TECHNOLOGY: Rational Functions"
    ],
    "Chapter 9: Sequences and Series": [
        "9-1 Mathematical Patterns",
        "9-2 Arithmetic Sequences",
        "9-3 Geometric Sequences",
        "9-4 Arithmetic Series",
        "9-5 Geometric Series",
        "Concept Byte EXTENSION: The Fibonacci Sequence",
        "Concept Byte Geometry and Infinite Series"
    ]
}

def get_all_expected_topics():
    """Get flat list of all expected topics"""
    all_topics = []
    for chapter_topics in EXPECTED_TOPICS.values():
        all_topics.extend(chapter_topics)
    return all_topics

def check_completion_status():
    """Check if all questions have been generated"""
    print("="*80)
    print("📊 ALGEBRA QUESTION GENERATION - COMPLETION STATUS")
    print("="*80)
    
    # Get all expected topics
    all_expected_topics = get_all_expected_topics()
    total_expected = len(all_expected_topics)
    
    print(f"\n📚 Expected Topics: {total_expected}")
    print(f"🎯 Target: 100 questions per topic")
    print(f"📈 Total Questions Target: {total_expected * 100:,}")
    
    # Get questions from database
    all_questions = db.execute_query(
        "SELECT topic, COUNT(*) as count FROM questions WHERE grade = '8' AND subject = 'Mathematics' GROUP BY topic"
    )
    
    # Create a dictionary of topic -> count
    topic_counts = {row['topic']: row['count'] for row in all_questions}
    
    # Check each expected topic
    completed_topics = []
    incomplete_topics = []
    missing_topics = []
    
    for topic in all_expected_topics:
        count = topic_counts.get(topic, 0)
        if count >= 100:
            completed_topics.append((topic, count))
        elif count > 0:
            incomplete_topics.append((topic, count))
        else:
            missing_topics.append(topic)
    
    # Print summary
    print(f"\n✅ Completed Topics (≥100 questions): {len(completed_topics)}/{total_expected}")
    print(f"⚠️  Incomplete Topics (<100 questions): {len(incomplete_topics)}")
    print(f"❌ Missing Topics (0 questions): {len(missing_topics)}")
    
    total_generated = sum(topic_counts.values())
    print(f"\n📊 Total Questions Generated: {total_generated:,} / {total_expected * 100:,}")
    print(f"📈 Completion Percentage: {(total_generated / (total_expected * 100) * 100):.1f}%")
    
    # Detailed breakdown
    if completed_topics:
        print(f"\n✅ COMPLETED TOPICS ({len(completed_topics)}):")
        for topic, count in sorted(completed_topics, key=lambda x: x[1], reverse=True)[:10]:  # Show top 10
            print(f"   ✓ {topic}: {count} questions")
        if len(completed_topics) > 10:
            print(f"   ... and {len(completed_topics) - 10} more")
    
    if incomplete_topics:
        print(f"\n⚠️  INCOMPLETE TOPICS ({len(incomplete_topics)}):")
        for topic, count in sorted(incomplete_topics, key=lambda x: x[1], reverse=True):
            print(f"   ⚠️  {topic}: {count} questions (need {100 - count} more)")
    
    if missing_topics:
        print(f"\n❌ MISSING TOPICS ({len(missing_topics)}):")
        for topic in missing_topics[:10]:  # Show first 10
            print(f"   ❌ {topic}: 0 questions")
        if len(missing_topics) > 10:
            print(f"   ... and {len(missing_topics) - 10} more")
    
    # Final status
    print("\n" + "="*80)
    if len(completed_topics) == total_expected:
        print("🎉 ALL QUESTIONS GENERATED AND LOADED INTO DATABASE! 🎉")
        print("="*80)
        return True
    else:
        remaining = total_expected - len(completed_topics)
        print(f"⏳ GENERATION IN PROGRESS: {remaining} topics remaining")
        print("="*80)
        return False

if __name__ == "__main__":
    try:
        is_complete = check_completion_status()
        exit(0 if is_complete else 1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

