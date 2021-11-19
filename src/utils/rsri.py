import pandas as pd
import sys
from datetime import datetime

SINGLE_LANE_CAPACITY = 1200  # {vehicles/lane/hour}
MULTI_LANE_CAPACITY = 1500  # {vehicles/lane/hour}


def exposure(df: pd.DataFrame):
    """Computes exposure at each induction loop.

        Exposure = (Volume / Capacity) * 3.0

        Args:
            df (pd.DataFrame): The data to process.

        Returns:
            [type]: [description]
    """
    print("exposure()")
    exposures = []
    for (index, row) in df.iterrows():
        volume = row['flow (veh/hr)']
        capacity = MULTI_LANE_CAPACITY
        exposure = (volume / capacity) * 3.0
        # print("\t(", volume, " / ", capacity, ") * 3.0 =", exposure)
        exposures.append(exposure)

    df["exposureIndex"] = exposures
    return df


def rsri():
    """
    Calculates `rsri` of a specified road segment.
    """
    rsri = exposure() * probability() * consequence()
    return rsri


def probability():
    pass


def consequence():
    pass


def totalVolume(df):
    return df.sum()


def run(df):
    print(df.info())
    e = exposure(df)


def csvToDataframe(fileName):
    """
    Converts a CSV file into a Pandas DataFrame.

    Opens the CSV file and saves the contents locally. Then parses and returns
    the resulting DataFrame.
    """
    return pd.read_csv(fileName, index_col=0)


def dataframeToCsv(df: pd.DataFrame, path: str, filename: str, timestamp: str):
    """Writes a Pandas Dataframe to a CSV file.

    Args:
        df (pandas.DataFrame): The Dataframe to export.
        path (str): Relative path to export the file into.
        fileName (str): Name of the file to export into.
        timestamp (str): A timestamp to suffix the fileName.
    """
    file = '%s%s_%s.csv' % (path, timestamp, filename)
    df.to_csv(file)
    print("Saved results to: %s" % file)


def main(filename):
    timestamp = datetime.now().strftime('%Y%m%d_%H-%M-%S')
    df_loop = csvToDataframe(filename).set_index(
        ["begin (sec)"], append=True).sort_index()
    print(exposure(df_loop))


if __name__ == "__main__":
    print("if __name__ == __main__()")
    loopFile = sys.argv[1]
    main(loopFile)
    # dataframeToCsv(df_loop, "reports/", "processed-inductionloops", timestamp)

    # volumeFile = sys.argv[1]
    # edgeFile = sys.argv[2]
    # if volumeFile == None:
    #     print("Error: a CVS file for volume data must be provided.")
    #     sys.exit(1)
    # if edgeFile == None:
    #     print("Error: a CSV file for edge data must be provided.")
    #     sys.exit(1)

    # # Convert CVS file into Pandas Dataframe.
    # df_steps = csvToDataFrame(volumeFile)
    # s_volume = totalVolume(df_steps)
    # df_edges = csvToDataFrame(edgeFile)
    # df_edges["Total Volume"] = s_volume
    # df_exposure = exposure(df_edges)
    # print(df_exposure)

    # print("\n\ndf_steps\n(", type(df_steps), "):\n", df_steps)
    # print("\n\ndf_volume\n(", type(s_volume), "):\n", s_volume)
    # print("\n\ndf_edges\n(", type(df_edges), "):\n", df_edges)
