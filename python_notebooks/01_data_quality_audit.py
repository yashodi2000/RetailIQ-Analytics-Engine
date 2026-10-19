import pandas as pd
import numpy as np
import os

# ============================================================
# RETAILIQ - DATA QUALITY AUDIT
# ============================================================

RAW_DATA_PATH = "data/raw/"


def audit_dataset():

    print("=" * 60)
    print("       RETAILIQ - DATA QUALITY AUDIT REPORT")
    print("=" * 60)
    print()

    # --------------------------------------------------------
    # Find CSV files
    # --------------------------------------------------------
    if not os.path.exists(RAW_DATA_PATH):
        print(f"❌ Data folder not found: {RAW_DATA_PATH}")
        return

    files = sorted(
        [f for f in os.listdir(RAW_DATA_PATH) if f.endswith(".csv")]
    )

    if not files:
        print("❌ No CSV files found in the raw data folder.")
        return

    # --------------------------------------------------------
    # Audit each dataset
    # --------------------------------------------------------
    for file in files:

        file_path = os.path.join(RAW_DATA_PATH, file)
        table_name = file.replace(".csv", "")

        try:
            df = pd.read_csv(file_path)

            print("-" * 60)
            print(f"TABLE: {table_name}")
            print("-" * 60)

            # ------------------------------------------------
            # 1. Dataset Size
            # ------------------------------------------------
            print(f"Rows    : {df.shape[0]}")
            print(f"Columns : {df.shape[1]}")

            # ------------------------------------------------
            # 2. Missing Values
            # ------------------------------------------------
            print("\n[1] Missing Values")

            null_counts = df.isnull().sum()
            missing_cols = null_counts[null_counts > 0]

            if not missing_cols.empty:

                for col, count in missing_cols.items():

                    percentage = (count / len(df)) * 100

                    print(
                        f"  ⚠️ {col}: "
                        f"{count} nulls ({percentage:.2f}%)"
                    )

            else:
                print("  ✅ No Missing Values")

            # ------------------------------------------------
            # 3. Duplicate Rows
            # ------------------------------------------------
            print("\n[2] Duplicate Rows")

            duplicate_count = df.duplicated().sum()

            if duplicate_count > 0:
                print(
                    f"  ⚠️ Duplicate Rows Found: "
                    f"{duplicate_count}"
                )
            else:
                print("  ✅ No Duplicate Rows")

            # ------------------------------------------------
            # 4. Negative Numeric Values
            # ------------------------------------------------
            print("\n[3] Negative Numeric Values")

            numeric_cols = df.select_dtypes(
                include=[np.number]
            ).columns

            negative_found = False

            for col in numeric_cols:

                negative_count = (df[col] < 0).sum()

                if negative_count > 0:

                    negative_found = True

                    print(
                        f"  ⚠️ {col}: "
                        f"{negative_count} negative values"
                    )

            if not negative_found:
                print("  ✅ No Negative Numeric Values")

            # ------------------------------------------------
            # 5. Zero Values
            # ------------------------------------------------
            print("\n[4] Zero Values")

            zero_found = False

            for col in numeric_cols:

                zero_count = (df[col] == 0).sum()

                if zero_count > 0:

                    zero_found = True

                    print(
                        f"  ℹ️ {col}: "
                        f"{zero_count} zero values"
                    )

            if not zero_found:
                print("  ✅ No Zero Numeric Values")

            # ------------------------------------------------
            # 6. Data Types
            # ------------------------------------------------
            print("\n[5] Data Types")

            print(df.dtypes.to_string())

            # ------------------------------------------------
            # 7. Unique Values
            # ------------------------------------------------
            print("\n[6] Unique Value Counts")

            for col in df.columns:

                unique_count = df[col].nunique()

                print(
                    f"  {col}: "
                    f"{unique_count} unique values"
                )

            print()

        except Exception as e:

            print(
                f"❌ Error auditing {file}: {e}"
            )

    print("=" * 60)
    print("             AUDIT COMPLETED")
    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    audit_dataset()