# Sample Dataset Directory

Place your CSV training datasets in this directory.

## Expected Format

```csv
label,message
spam,"FREE iPhone! Click here to claim your prize now!"
ham,"Hi, meeting tomorrow at 10am. Let me know if available."
```

Supported label formats: `spam`/`ham`, `1`/`0`, `true`/`false`

## Training

Either upload the CSV via the admin UI (Dataset Management page) or run:

```bash
cd ml
python main.py train dataset/your_dataset.csv
```

## Note

The sample data used during development is provided by the seed script
(`backend/scripts/seed_data.py`) and is clearly identified as development
sample data, not production-quality training data.
