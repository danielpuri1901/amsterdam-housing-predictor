# Amsterdam housing predictor

An educational regression project using generated sample data for student housing in Amsterdam.
It compares linear regression, a decision tree, and a random forest.

The sample data does not represent observed housing transactions.
The project is not a validated rental-price service.

## Evaluation limit

The current analysis creates `price_per_sqm` from the target price before selecting model inputs.
The input selection removes `price` but retains `price_per_sqm`.
The model therefore receives information derived from the value it must predict.
This is target leakage.

The earlier README reported R² 0.946 and RMSE EUR 59.33.
Those historical scores cannot establish prediction quality for unseen housing prices.
The feature path needs correction and the evaluation needs a fresh run before those scores can be used.

## Files

| Path | Purpose |
| --- | --- |
| `data/` | Raw and processed sample data. |
| `src/data_preprocessing.py` | Cleaning and feature preparation. |
| `src/train_models.py` | Model training and evaluation. |
| `run_analysis.py` | Runs the analysis pipeline. |
| `demo.py` | Provides a command-line demonstration. |
| `app.py` | Provides a Streamlit interface. |
| `notebooks/` | Contains the analysis notebook. |

## Local setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run the existing demonstration

```bash
python demo.py
```

The full pipeline writes processed data, trained models, and plots:

```bash
python run_analysis.py
```

The Streamlit interface starts with:

```bash
streamlit run app.py
```

These routes run the current implementation, including the evaluation limit described above.
See [`TECHNICAL_NOTES.md`](TECHNICAL_NOTES.md) and [`USAGE.md`](USAGE.md) for earlier project notes.
