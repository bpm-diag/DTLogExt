import pm4py
import pandas as pd

# log with only start type event (so no end, assign, ecc)
log = pm4py.read_xes('input_file/log_text3.xes')
bpmn_model_path = 'path of bpmn model'

# log without loop (so I delete near duplicate events in the log, delete self-loops in the log), for next evaluations because in petri net no consider self loops
# the bpmn model by spliminer keeps track of self loops, if there are in the log
prec_row = None
i = 0
self_loops_activities = {}
self_loops_count = {}
log_noloop_app = []
for index, row in log.iterrows():
    if prec_row is not None:
        if prec_row['case:concept:name'] == row['case:concept:name']:
            if prec_row['concept:name'] == row['concept:name']:
                if i in self_loops_count:
                    self_loops_activities[i] = [[row['case:concept:name']], [row['concept:name']]]
                    self_loops_count[i] += 1
                else:
                    self_loops_count[i] = 0
                    self_loops_activities[i] = [[row['case:concept:name']], [row['concept:name']]]
                    self_loops_count[i] += 1
            else:
               prec_row = row
               i+=1
               log_noloop_app.append(row)
        else:
            prec_row = row 
            i+=1
            log_noloop_app.append(row)
    else:
        prec_row = row
        log_noloop_app.append(row)

self_loops = []
if not self_loops_activities:
    log_noloop = log
else:
    # log without self loops
    log_noloop = pd.DataFrame(log_noloop_app)
    log_noloop.reset_index(drop=True, inplace=True)

    for j in range(i):
        if j in self_loops_activities:
            self_loops.append((self_loops_activities[j][0][0], self_loops_activities[j][1][0], self_loops_count[j]+1))

print("---METRICS WITH SPLIT MINER ALGORITHM---")
bpmn_model = pm4py.read_bpmn(bpmn_model_path)
petri_net, initial_marking, final_marking = pm4py.convert_to_petri_net(bpmn_model)
#pm4py.write_pnml(petri_net, initial_marking, final_marking, 'output file.pnml')
#pm4py.save_vis_petri_net(petri_net, initial_marking, final_marking, 'output file.png')

# Fitness value and Precision value
fitness_alignments = pm4py.fitness_alignments(log_noloop, petri_net, initial_marking, final_marking)
print("Fitness value: ", fitness_alignments)
precision_alignments = pm4py.precision_alignments(log_noloop, petri_net, initial_marking, final_marking, activity_key='concept:name', case_id_key='case:concept:name', timestamp_key='time:timestamp')
print("Precision value: ", precision_alignments)

# Replay traces over the model
print("---REPLAY TRACES OVER THE MODEL WITH ALIGNEMNT---")
alignment_output = pm4py.conformance_diagnostics_alignments(log_noloop, petri_net, initial_marking, final_marking, activity_key='concept:name', case_id_key='case:concept:name', timestamp_key='time:timestamp')

conformance_traces = []
non_conformance_traces = []
threshold = 0.6
for t in alignment_output:
    if t['fitness'] >= threshold:
        conformance_traces.append(t)
    else:
        non_conformance_traces.append(t)
min_fitness_trace = min(alignment_output, key=lambda x: x['fitness'])
print("Total number of traces: ", len(alignment_output))
print(f"Total number of conformance traces (fitness > {threshold}): {len(conformance_traces)}")
print(f"Total number of non conformance traces (fitness <= {threshold}): {len(non_conformance_traces)}")
print(f"Min fitness trace: {min_fitness_trace}")


