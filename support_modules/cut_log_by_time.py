import pm4py
import pandas as pd

tag_to_identify_activities = 'concept:name'
tag_to_identify_resources = 'org:resource'
tag_to_identify_trace = 'case:concept:name'
tag_to_identify_timestamp = 'time:timestamp'
tag_to_identify_node_lifecycle = 'lifecycle:transition'
tag_to_identify_node_type = 'nodeType'

class CutLog():

    def __init__(self, log, settings, cut_time):
        self._log = log
        self._settings = settings
        self._path = settings[0]['path']
        self._name = settings[0]['namefile']

        if type(cut_time) == type(log[tag_to_identify_timestamp].min()):
            self._cut_time = cut_time
        else:
            self._cut_time = pd.to_datetime(cut_time).tz_convert('UTC')

        self._new_log = self.cut_log_by_time(self._log, self._cut_time)
        self.save_on_file(self._new_log)

    def cut_log_by_time(self, log, cut_time):
        filtered_df = log[log[tag_to_identify_timestamp] <= cut_time]
        return filtered_df

    def save_on_file(self, log):
        pm4py.write_xes(log, self._path + 'input_data/' + self._name + '_cut.xes', case_id_key=tag_to_identify_trace)



if __name__ == "__main__":
    name = "name" #insert name of event log
    path = "path" #insert path
    log = pm4py.read_xes(path + name + '.xes')

    cut_time = "2024-11-11 13:50:00+00:00" #insert cut time
    cut_time = pd.to_datetime(cut_time).tz_convert('UTC')
    
    settings = list()
    settings.append({'path': path, 'namefile': name})

    CutLog(log, settings, cut_time)
