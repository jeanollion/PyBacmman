from os import listdir
from os.path import isfile, isdir, join
import json
import pandas as pd

class Dataset():
    def __init__(self, path:str, filter = None):
        self.path = path
        self.ds_name = get_DS_name(path, filter)
        if self.ds_name is not None: # inspect config file
            cf = join(path, self.ds_name+"_config.json")
            with open(cf, errors='ignore') as f:
                try:
                    conf = json.load(f)
                    self.channel_names = [c["name"] for c in conf["structures"]["list"]]
                except Exception as e:
                    print(f"Error trying to load configuration file: {f}")
                    raise e
        self.data = {}

    def set_channel_name(self, old_channel, new_channel):
        old_channel = self._get_channel_index(old_channel)
        assert old_channel < len(self.channel_names), f"invalid channel idx, should be <{len(self.channel_names)}"
        self.channel_names[old_channel] = new_channel

    def _get_channel_name(self, channel):
        if not isinstance(channel, str):
            assert channel<len(self.channel_names), f"invalid channel index, should be < {len(self.channel_names)}"
            return self.channel_names[channel]
        else:
            return channel

    def _get_channel_index(self, channel):
        if isinstance(channel, str):
            assert channel in self.channel_names, f"invalid channel name, should be in {self.channel_names}"
            return self.channel_names.index(channel)
        else:
            return channel

    def _get_data_file_path(self, channel):
        return join(self.path, f"{self.ds_name}_{self._get_channel_index(channel)}.csv")

    def _open_data(self, channel):
        return pd.read_csv(self._get_data_file_path(channel), sep=';')

    def get_data(self, channel):
        channel = self._get_channel_name(channel)
        if channel not in self.data:
            self.data[channel] = self._open_data(channel)
        return self.data[channel]

    def __str__(self):
        return f"{self.ds_name} {self.channel_names} path={self.path}"

class DatasetList(Dataset):
    def __init__(self, dataset_list:list = None, path:str = None, filter = None, channel_name_mapping:dict = None):
        if dataset_list is not None:
            self.datasets = dataset_list
        elif path is not None:
            self.datasets = [Dataset(join(path, f), filter) for f in listdir(path) if isdir(join(path, f))]
            self.datasets = [d for d in self.datasets if d.ds_name is not None]
            if channel_name_mapping is not None:
                for d in self.datasets:
                    for i, n in enumerate(d.channel_names):
                        if n in channel_name_mapping:
                            d.channel_names[i] = channel_name_mapping[n]

        assert len(self.datasets)>1, "no datasets where found"
        # channel names are the common channel names between all channel names
        self.channel_names = None
        for d in self.datasets:
            if self.channel_names is None:
                self.channel_names = d.channel_names
            else:
                inter = set(self.channel_names).intersection(d.channel_names)
                self.channel_names = [n for n in self.channel_names if n in inter]
        assert len(self.channel_names)>0, f"no channel names in common between datasets : {[str(d) for d in self.datasets]}"
        self.data = {}

    def set_channel_name(self, old_channel, new_channel):
        old_channel_idx = self._get_channel_index(old_channel)
        old_channel_name = self._get_channel_name(old_channel)
        assert old_channel_idx < len(self.channel_names), f"invalid channel idx, should be <{len(self.channel_names)}"
        self.channel_names[old_channel_idx] = new_channel
        for d in self.datasets:
            d.set_channel_name(old_channel_name, new_channel)

    def _open_data(self, channel):
        channel = self._get_channel_name(channel)
        return pd.concat([d._open_data(channel) for d in self.datasets]) #open_data to avoid storing the data in each dataset

    def __str__(self):
        return f"{[d.ds_name for d in self.datasets]} {self.channel_names}"

# util functions
def get_DS_name(path, filter):
    # must contain a file ending by _config.json
    if isinstance(filter, str):
        _filter = lambda file_name:filter in file_name
    else:
        _filter = filter
    if isdir(path):
        for f in listdir(path):
            if f.endswith("_config.json") and (filter is None or _filter(f)) and isfile(join(path, f)):
                return f[:-12]
    return None
