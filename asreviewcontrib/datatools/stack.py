import argparse
from pathlib import Path

import pandas as pd
from asreview import ASReviewData
from asreview.data.base import load_data


def _check_suffix(input_files, output_file):
    # Also raises ValueError on URLs that do not end with a file extension
    suffixes = [Path(item).suffix for item in input_files if item is not None]
    suffixes.append(Path(output_file).suffix)

    set_ris = {".txt", ".ris"}
    set_tabular = {".csv", ".tab", ".tsv", ".xlsx"}
    set_suffixes = set(suffixes)

    if len(set(suffixes)) > 1:
        if not (set_suffixes.issubset(set_ris) or set_suffixes.issubset(set_tabular)):
            raise ValueError(
                "• Several file types were given; All input files, as well as the output file should be of the same "
                "type. "
            )


def stack(output_file, input_files):
    _check_suffix(input_files, output_file)

    list_dfs = [load_data(item).df for item in input_files]
    df_stacked = pd.concat(list_dfs).reset_index(drop=True)
    as_stacked = ASReviewData(df=df_stacked)

    as_stacked.to_file(output_file)


def _parse_arguments_stack():
    parser = argparse.ArgumentParser(prog="ASReview dataset stacking")
    parser.add_argument("output_path", type=str, help="The output file path.")
    parser.add_argument(
        "datasets", type=str, nargs="+", help="Any number of datasets to stack."
    )

    return parser
