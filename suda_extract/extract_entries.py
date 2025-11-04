import os
from settings import EXTRACT_SOURCE_FILES
from settings import INDEX_HOSTNAME
from extract_entry import ExtractEntry


class ExtractEntries(object):
    def __init__(self, file_path=EXTRACT_SOURCE_FILES):
        # load directory and get list of files;
        self.file_list = []
        for base_path, subdirectories, file_names in os.walk(file_path):
            for file_name in file_names:
                try:
                    _ = int(file_name)
                    self.file_list.append(os.path.join(base_path, file_name))
                except ValueError:
                    continue

    def extract(
            self,
            export_path: str="",
            file_type: str="json",
            target_index_hostname: str=INDEX_HOSTNAME
    ):
        for file_name in self.file_list:
            entry = ExtractEntry(file_name)
            if export_path:
                entry.export(export_path, file_type)
            else:
                entry.save(target_index_hostname=target_index_hostname)
