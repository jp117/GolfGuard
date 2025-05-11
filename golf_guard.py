import math
import statistics
from scipy.stats import norm

def calculate_score_differential(score, course_rating, course_slope):
    """
    Calculate the score differential using the USGA formula:
    ((Gross Score - Course Rating) × 113) / Slope Rating
    
    Where:
    - 113 is the standard slope rating
    - Course Slope is the difficulty of the course for bogey golfers
    - Course Rating is the expected score for scratch golfers
    - Score is the actual score shot
    """
    return ((score - course_rating) * 113) / course_slope

def get_standard_deviation_range(handicap_index):
    """
    Get the standard deviation range based on handicap index ranges.
    Returns (low_std_dev, high_std_dev)
    """
    if handicap_index <= 0:
        return (1.8, 2.2)
    elif handicap_index <= 5:
        return (2.0, 2.5)
    elif handicap_index <= 10:
        return (2.5, 3.0)
    elif handicap_index <= 15:
        return (3.0, 3.5)
    elif handicap_index <= 20:
        return (3.5, 4.0)
    elif handicap_index <= 25:
        return (4.0, 4.5)
    elif handicap_index <= 30:
        return (4.5, 5.0)
    else:
        return (5.0, 5.5)

def calculate_z_score(handicap_index, course_rating, course_slope, score):
    """
    Calculate the z-score for a round based on expected performance.
    """
    # Calculate Course Handicap
    course_handicap = handicap_index * (course_slope / 113)
    
    # Calculate Expected Score
    expected_score = course_rating + course_handicap
    
    # Calculate Strokes Better Than Expected
    strokes_better = expected_score - score
    
    # Get Standard Deviation (using midpoint of range)
    low_std_dev, high_std_dev = get_standard_deviation_range(handicap_index)
    std_dev = (low_std_dev + high_std_dev) / 2
    
    # Calculate Z-Score
    return strokes_better / std_dev

def get_flag_status(score_differential, z_score, strokes_better):
    """
    Determine the flag status based on differential and z-score thresholds.
    Only flags suspiciously good scores, not bad scores.
    Returns (flag_level, explanation)
    """
    # Only flag if the score is better than expected (positive strokes_better)
    if strokes_better > 0:
        # Tier 1: Automatic Red Flag
        if score_differential <= -1.0 or z_score >= 2.5:
            return ("🔺 RED FLAG", 
                    "Likely sandbagging - Either scratch-level performance or 2.5+ standard deviations better than expected")
        
        # Tier 2: Review Flag
        elif score_differential <= 0.0 or (z_score >= 1.5 and z_score < 2.5):
            return ("🟡 REVIEW", 
                    "Possible anomaly - Could be a career-best round or a fluke, especially in tournament play")
    
    # No Flag for normal or worse-than-expected scores
    return ("⚪ NO FLAG", 
            "Normal round relative to handicap")

def calculate_probability_range(handicap_index, course_rating, course_slope, score):
    """
    Calculate the probability range of shooting a particular score
    based on the golfer's handicap index.
    Returns (low_probability, high_probability)
    """
    # 1. Calculate Course Handicap
    course_handicap = handicap_index * (course_slope / 113)
    
    # 2. Calculate Expected Score
    expected_score = course_rating + course_handicap
    
    # 3. Calculate Strokes Better Than Expected
    strokes_better = expected_score - score
    
    # 4. Get Standard Deviation range
    low_std_dev, high_std_dev = get_standard_deviation_range(handicap_index)
    
    # 5. Calculate Z-Scores for both ends of the range
    low_z_score = strokes_better / high_std_dev  # Using high_std_dev gives lower z-score
    high_z_score = strokes_better / low_std_dev  # Using low_std_dev gives higher z-score
    
    # 6. Calculate Probability range using normal distribution
    # For better scores (positive strokes_better), we want the probability of being this good or better
    # For worse scores (negative strokes_better), we want the probability of being this bad or worse
    if strokes_better > 0:
        # For good scores, use survival function (1 - CDF)
        low_probability = norm.sf(low_z_score)
        high_probability = norm.sf(high_z_score)
    else:
        # For bad scores, use CDF directly
        low_probability = norm.cdf(low_z_score)
        high_probability = norm.cdf(high_z_score)
    
    # Ensure probabilities are never 0
    low_probability = max(low_probability, 1e-10)
    high_probability = max(high_probability, 1e-10)
    
    return (low_probability, high_probability)

def main():
    print("Welcome to GolfGuard - Golf Score Probability Calculator")
    print("------------------------------------------------------")
    
    # Get input from user
    name = input("Enter golfer's name: ")
    handicap_index = float(input("Enter handicap index: "))
    course_rating = float(input("Enter course rating: "))
    course_slope = float(input("Enter course slope: "))
    score = float(input("Enter score: "))
    
    # Calculate score differential
    score_differential = calculate_score_differential(score, course_rating, course_slope)
    
    # Calculate course handicap and expected score
    course_handicap = handicap_index * (course_slope / 113)
    expected_score = course_rating + course_handicap
    strokes_better = expected_score - score
    
    # Calculate probability range
    low_prob, high_prob = calculate_probability_range(handicap_index, course_rating, course_slope, score)
    mid_prob = (low_prob + high_prob) / 2
    
    # Calculate odds ranges (1 in X)
    # Note: Higher probability = lower odds (1 in X)
    best_odds = round(1 / low_prob)  # Best case = lowest probability = highest odds
    worst_odds = round(1 / high_prob)  # Worst case = highest probability = lowest odds
    mid_odds = round(1 / mid_prob)
    
    # Calculate percentage chance ranges
    best_percentage = low_prob * 100
    worst_percentage = high_prob * 100
    mid_percentage = mid_prob * 100
    
    # Get standard deviation range
    low_std_dev, high_std_dev = get_standard_deviation_range(handicap_index)
    
    # Calculate z-scores for all scenarios
    # For better scores (positive strokes_better):
    # - Best case uses high_std_dev (gives lower z-score)
    # - Worst case uses low_std_dev (gives higher z-score)
    if strokes_better > 0:
        best_z_score = strokes_better / high_std_dev
        worst_z_score = strokes_better / low_std_dev
    else:
        # For worse scores (negative strokes_better), reverse the logic
        best_z_score = strokes_better / low_std_dev
        worst_z_score = strokes_better / high_std_dev
    
    mid_z_score = strokes_better / ((low_std_dev + high_std_dev) / 2)
    
    # Get flag status (using midpoint z-score for flagging)
    flag_level, flag_explanation = get_flag_status(score_differential, mid_z_score, strokes_better)
    
    # Print results
    print("\nResults:")
    print(f"Player: {name}")
    print(f"Score: {score} (Expected Score: {expected_score:.1f})")
    print(f"Performance: {abs(strokes_better):.1f} strokes {'better' if strokes_better > 0 else 'worse'} than expected")
    print("\nProbability Analysis:")
    print(f"Best-case scenario (most optimistic):")
    print(f"  - Odds: 1 in {best_odds:,} ({best_percentage:.2f}% chance)")
    print(f"  - Z-Score: {best_z_score:.2f} standard deviations")
    print(f"Midpoint scenario:")
    print(f"  - Odds: 1 in {mid_odds:,} ({mid_percentage:.2f}% chance)")
    print(f"  - Z-Score: {mid_z_score:.2f} standard deviations")
    print(f"Worst-case scenario (most conservative):")
    print(f"  - Odds: 1 in {worst_odds:,} ({worst_percentage:.2f}% chance)")
    print(f"  - Z-Score: {worst_z_score:.2f} standard deviations")
    print(f"\n{flag_level}: {flag_explanation}")

if __name__ == "__main__":
    main() 