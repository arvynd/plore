import argparse
import json
import os
import sys

import polars as pl
import pyarrow as pa


def read_file(path: str) -> pl.DataFrame:

    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found {path}")
    elif path.endswith(".csv"):
        df = pl.read_csv(path)
    elif path.endswith(".parquet"):
        df = pl.read_parquet(path)
    elif path.endswith(".json"):
        df = pl.read_json(path)
    else:
        raise ValueError(f"Unsupported file type {path}")

    return df


def write_to_stdout(df: pl.DataFrame):

    arrow_table = df.to_arrow()
    sink = pa.BufferOutputStream()
    writer = pa.ipc.new_stream(sink, arrow_table.schema)
    writer.write_table(arrow_table)
    writer.close()
    sys.stdout.buffer.write(sink.getvalue().to_pybytes())


def main():
    parser = argparse.ArgumentParser(
        prog="sidecar",
        description="sidecar for plore extension",
    )

    parser.add_argument("filename")
    args = parser.parse_args()

    try:
        df = read_file(args.filename)
        write_to_stdout(df)
    except (FileNotFoundError, ValueError) as e:
        sys.stderr.write(json.dumps({"error": str(e)}) + "\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
