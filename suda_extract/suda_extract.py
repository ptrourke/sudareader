import argparse
import os

from settings import EXTRACT_SOURCE_FILES
from settings import INDEX_HOSTNAME
from extract_entry import ExtractEntry
from suda_extract.extract_entries import ExtractEntries


def main(**kwargs):
    path: str = kwargs.get("path")
    file_name: str = kwargs.get("file")
    export_path: str = kwargs.get("export")
    yaml_file: bool = kwargs.get("yaml_file")
    json_file: bool = kwargs.get("json_file")
    if file_name:
        file_path: str = os.path.join(path, file_name)
        extract_entry = ExtractEntry(file_path)
        lemma_string: str = ""
        if export_path:
            export_type = "yaml" if yaml_file else "json"
            extract_entry.export(export_path, format=export_type)
        else:
            if yaml_file:
                lemma_string = extract_entry.to_yaml()
            elif json_file:
                lemma_string = extract_entry.to_json()
            print(lemma_string)
    else:
        extract_entries = ExtractEntries(path)
        pass

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        "--path",
        "-p",
        type=str,
        dest="path",
        help="Path to Suda On Line page files (without file names) to extract.",
        default=EXTRACT_SOURCE_FILES
    )
    argument_parser.add_argument(
        "--file",
        "-f",
        type=str,
        dest="file",
        help="File name (without path) 0f specific Suda On Line page file to extract."
    )
    argument_parser.add_argument(
        "--export",
        "-e",
        type=str,
        dest="export",
        help="Export file name and path."
    )
    argument_parser.add_argument(
        "--json-format",
        "-j",
        dest="json_file",
        help="Output as json.",
        action='store_true'
    )
    argument_parser.add_argument(
        "--yaml-format",
        "-y",
        dest="yaml_file",
        help="Output as yaml.",
        action='store_true'
    )
    argument_parser.add_argument(
        "--save-to-index",
        type=str,
        dest="save_to_index",
        help="Save to index instance at hostname given.",
        default=INDEX_HOSTNAME
    )

    args = argument_parser.parse_args()
    options: dict = vars(args)
    main(**options)
