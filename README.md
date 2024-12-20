# Football Performance Scoring

## 📊 About the Project

This project is a **football performance scoring model** designed to evaluate player performances using weighted metrics. The system allows:
- Comparison of player performances across different positions.
- Flexible adjustment of weights for specific metrics based on their importance.
- Integration of real-world football data for in-depth analysis.

The model primarily focuses on **strikers (CF - Centre Forwards)** and calculates a **performance score** based on various metrics such as goals, assists, shots, and passes.

---

## ⚙️ Features

- **Data Cleaning**: Automatically handles missing and irrelevant data.
- **Position Generalization**: Converts detailed positions into generalized roles (e.g., Striker, Midfielder, etc.).
- **Weighted Scoring**: Assigns custom weights to performance metrics for objective scoring.
- **Customizable**: Easily adaptable to other player positions or leagues.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- Required libraries:
  - `pandas`
  - `numpy`
  - `openpyxl`

You can install the necessary libraries with:
```bash
pip install pandas numpy openpyxl
