# GolfGuard

GolfGuard is a command-line application that calculates golf score differentials and analyzes the probability of shooting specific scores based on a golfer's handicap index. It helps identify potential anomalies in golf scores and provides detailed statistical analysis.

## Features

- Calculate score differentials using USGA formula
- Analyze probability of shooting specific scores
- Calculate odds ranges (1 in X)
- Flag suspicious scores based on statistical analysis
- Provide detailed performance metrics and Z-scores

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/GolfGuard.git
cd GolfGuard
```

2. Create and activate a virtual environment:

On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Make sure your virtual environment is activated (you should see `(venv)` in your terminal prompt)

2. Run the application:
```bash
python golf_guard.py
```

3. Follow the prompts to enter:
   - Golfer's name
   - Handicap index
   - Course rating
   - Course slope
   - Score

## Example Output

The application will provide:
- Score differential
- Expected score vs actual score
- Probability analysis with best-case, midpoint, and worst-case scenarios
- Odds ranges (1 in X)
- Flag status for suspicious scores
- Z-scores and standard deviation analysis

## Dependencies

- scipy
- statistics (built-in)
- math (built-in)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
