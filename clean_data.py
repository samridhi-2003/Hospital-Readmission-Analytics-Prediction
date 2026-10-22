from urllib.request import urlretrieve
from zipfile import ZipFile
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

input_file = DATA_DIR / "diabetic_data.csv"

if not input_file.exists():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    url = "https://archive.ics.uci.edu/static/public/296/diabetes+130-us+hospitals+for+years+1999-2008.zip"
    zip_path = DATA_DIR / "diabetes_dataset.zip"

    print("Downloading dataset...")
    urlretrieve(url, zip_path)

    with ZipFile(zip_path, "r") as zip_file:
        with zip_file.open("diabetic_data.csv") as source:
            with open(input_file, "wb") as destination:
                destination.write(source.read())

    zip_path.unlink()
    print("Dataset downloaded successfully!")

output_file = DATA_DIR / "hospital_cleaned.csv"

if not input_file.exists():
    print("Original dataset not found!")
    print("Please place diabetic_data.csv inside the data folder.")
    raise SystemExit(1)

df = pd.read_csv(input_file, low_memory=False)

print("Original Dataset Shape:", df.shape)

df = df.replace("?", "Unknown")
df = df.fillna("Unknown")

df["readmitted_30d"] = (
    df["readmitted"] == "<30"
).astype(int)

df = df.drop(columns=["weight"], errors="ignore")

df.to_csv(output_file, index=False)

print("Cleaned Dataset Saved Successfully!")
print("Cleaned Dataset Shape:", df.shape)

print("\nTarget Distribution:")
print(df["readmitted_30d"].value_counts())


existing = pd.read_csv(
    DATA_DIR / "hospital_cleaned.csv",
    low_memory=False
)

generated = pd.read_csv(
    DATA_DIR / "hospital_cleaned_test.csv",
    low_memory=False
)

print("\nExisting Dataset:", existing.shape)
print("Generated Dataset:", generated.shape)

print("\nExtra Columns in Generated Dataset:")
print(sorted(set(generated.columns) - set(existing.columns)))

print("\nMissing Columns in Generated Dataset:")
print(sorted(set(existing.columns) - set(generated.columns)))

common_columns = existing.columns.intersection(generated.columns)

different_columns = [
    col for col in common_columns
    if not existing[col].equals(generated[col])
]

print("\nColumns With Different Values:")
print(different_columns)

print("\nTotal Different Columns:", len(different_columns))

