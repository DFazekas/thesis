import csv
import pandas as pd
from datetime import datetime


def df2CSV(df: pd.DataFrame, path: str, fileName: str, timestamp: str):
    """Prints a Pandas Dataframe to a CSV file.

        Args:
            df (pd.DataFrame): The data to print.
            path (str): The relative path of the export file.
            fileName (str): The name of the export file.
            timestamp (str): A timestamp to prefix the filename used to uniquely identify this file.
    """
    file = '%s%s_%s.csv' % (path, timestamp, fileName)
    df.to_csv(file)
    print("Saved results to: %s" % file)


def exportCSV(filepath: str, rows: "list(str)"):
    """Exports data to a CSV file.

        Args:
            filepath (str): The path of the exported file.
            rows (list): The data to export.
    """
    with open(filepath, 'w') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    print("\tSaved data to: %s" % filepath)
