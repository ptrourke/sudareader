from extract_entry import ExtractEntry


class ExtractEntries(object):
    def __init__(self):
        # load directory and get list of files;
        self.file_list = []
        pass

    def extract(self, file_type: str, save: str, export: str):
        for file_name in self.file_list:
            entry = ExtractEntry(file_name)
            if save:
                entry.save(save)
            else:
                entry.export(export, file_type)
