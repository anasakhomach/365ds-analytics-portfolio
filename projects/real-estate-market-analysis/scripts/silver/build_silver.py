from __future__ import annotations

import numpy as np
import pandas as pd

from common import connect, normalize_column, write_dataframe


AGE_BINS = [19, 25, 31, 36, 42, 48, 54, 59, 65, 71, 76]


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned.columns = [normalize_column(col) for col in cleaned.columns]
    return cleaned.drop(columns=[col for col in cleaned.columns if col.startswith("unnamed")])


def _clean_string(series: pd.Series) -> pd.Series:
    return series.astype("string").str.strip().replace({"": pd.NA, "nan": pd.NA})


def _parse_money(series: pd.Series) -> pd.Series:
    cleaned = (
        series.astype("string")
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    return pd.to_numeric(cleaned, errors="coerce")


def _clean_customers(raw: pd.DataFrame) -> pd.DataFrame:
    customers = _normalize_columns(raw)
    customers = customers.rename(columns={"customerid": "customer_id"})

    text_columns = ["customer_id", "entity", "name", "surname", "sex", "country", "state", "purpose", "mortgage", "source"]
    for column in text_columns:
        customers[column] = _clean_string(customers[column])

    customers["birth_date"] = pd.to_datetime(customers["birth_date"], errors="coerce")
    customers["deal_satisfaction"] = pd.to_numeric(customers["deal_satisfaction"], errors="coerce").astype("Int64")
    customers["country"] = customers["country"].fillna("Unknown")
    customers["state"] = customers["state"].fillna("Unknown")
    customers["has_mortgage"] = customers["mortgage"].eq("Yes")

    return customers


def _clean_properties(raw: pd.DataFrame) -> pd.DataFrame:
    properties = _normalize_columns(raw)
    properties = properties.rename(columns={"id": "property_id", "property": "property_number", "customerid": "customer_id"})

    properties["property_id"] = pd.to_numeric(properties["property_id"], errors="coerce").astype("Int64")
    properties["building_id"] = pd.to_numeric(properties["building"], errors="coerce").astype("Int64")
    properties = properties.drop(columns=["building"])
    properties["property_number"] = pd.to_numeric(properties["property_number"], errors="coerce").astype("Int64")
    properties["area"] = pd.to_numeric(properties["area"], errors="coerce")
    properties["price"] = _parse_money(properties["price"])
    properties["sale_date"] = pd.to_datetime(properties["date_sale"], errors="coerce")
    properties = properties.drop(columns=["date_sale"])

    properties["type"] = _clean_string(properties["type"])
    properties["status"] = _clean_string(properties["status"]).replace({"-": "Available"})
    properties["customer_id"] = _clean_string(properties["customer_id"])
    properties["sold_flag"] = properties["status"].eq("Sold")
    properties["building_label"] = "Building " + properties["building_id"].astype("string")
    properties["revenue"] = np.where(properties["sold_flag"], properties["price"], 0.0)

    return properties


def _build_transactions(properties: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    transactions = properties.merge(customers, on="customer_id", how="left", suffixes=("", "_customer"))
    transactions["age_at_purchase"] = (
        (transactions["sale_date"] - transactions["birth_date"]).dt.days / 365.25
    ).round(1)
    transactions.loc[~transactions["sold_flag"], "age_at_purchase"] = np.nan
    transactions["sale_year"] = transactions["sale_date"].dt.year.astype("Int64")
    transactions["sale_month"] = transactions["sale_date"].dt.strftime("%Y-%m")
    transactions["age_interval"] = pd.cut(transactions["age_at_purchase"], bins=AGE_BINS).astype("string")
    transactions["price_interval"] = pd.cut(transactions["price"], bins=10).astype("string")
    transactions["country"] = transactions["country"].fillna("Unknown")
    transactions["state"] = transactions["state"].fillna("Unknown")
    transactions["deal_satisfaction"] = transactions["deal_satisfaction"].astype("Int64")
    transactions["has_mortgage"] = transactions["has_mortgage"].fillna(False)
    return transactions


def build_silver() -> dict[str, int]:
    with connect() as con:
        raw_customers = con.execute("SELECT * FROM bronze.raw_customers").fetchdf()
        raw_properties = con.execute("SELECT * FROM bronze.raw_properties").fetchdf()

        customers = _clean_customers(raw_customers)
        properties = _clean_properties(raw_properties)
        transactions = _build_transactions(properties, customers)

        write_dataframe(con, "silver", "cleaned_customers", customers)
        write_dataframe(con, "silver", "cleaned_properties", properties)
        write_dataframe(con, "silver", "property_transactions", transactions)

        return {
            "cleaned_customers": len(customers),
            "cleaned_properties": len(properties),
            "property_transactions": len(transactions),
        }


if __name__ == "__main__":
    counts = build_silver()
    for table, row_count in counts.items():
        print(f"{table}: {row_count} rows")
