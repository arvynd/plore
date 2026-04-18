import argparse
import os
import sys

import polars as pl
import pyarrow as pa


def read_csv_file(path: str) -> pl.DataFrame:

    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found {path}")
    else:
        df = pl.read_csv(path)

    return df


def write_to_stdout(df: pl.DataFrame):

    arrow_table = df.to_arrow()
    sink = pa.BufferOutputStream()
    writer = pa.ipc.new_stream(sink, arrow_table.schema)
    writer.write_table(arrow_table)
    writer.close()
    sys.stdout.buffer.write(sink.getvalue().to_pybytes())


parser = argparse.ArgumentParser(
    prog="sidecar",
    description="sidecar for plore extension",
    epilog="Text at the bottom of help",
)


parser.add_argument("filename")
args = parser.parse_args()

# TODO: wrap in main() + if __name__ == "__main__" guard
# TODO: handle errors as JSON to stderr instead of raw tracebacks
# TODO: extend load_file() to dispatch on extension (.csv, .parquet, .json)

# Orchestrate

df = read_csv_file(args.filename)
write_to_stdout(df)
