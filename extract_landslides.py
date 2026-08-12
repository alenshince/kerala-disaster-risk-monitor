import pdfplumber
import pandas as pd


PDF_FILE = r"C:\Users\annma\Downloads\kerala-disaster-system\LANDSLIDE INVENTORY (Field Validated).pdf"
OUTPUT_FILE = "landslide_inventory_extracted.csv"


print("Opening PDF...")

all_rows = []


with pdfplumber.open(PDF_FILE) as pdf:

    total_pages = len(pdf.pages)

    print("Total pages:", total_pages)

    for page_number, page in enumerate(pdf.pages, start=1):

        print(
            f"Reading page {page_number}/{total_pages}..."
        )

        tables = page.extract_tables()

        for table in tables:

            if table:

                for row in table:

                    if row:
                        all_rows.append(row)


print()
print("PDF extraction completed.")

print("Rows extracted:", len(all_rows))


if len(all_rows) == 0:

    print("No tables were found in the PDF.")

else:

    df = pd.DataFrame(all_rows)

    print()
    print("First 5 extracted rows:")
    print(df.head())

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()
    print(
        "Saved:",
        OUTPUT_FILE
    )