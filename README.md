# DataLogX: A Framework for Automated Generation of Process Simulation Scenarios from Event Logs
**DataLogX** is a fraemwork for the automated generation of process simulation scenarios from event logs. The proposed framework allows one to elaborate real or synthetic event logs and to automatically perform two fundamental operations:
* Process Discovery: the construction of the process model in BPMN format starting from the event log.
* Parameter Estimation: estimation of the simulation parameters, necessary to configure the simulation models in a way that is consistent with the characteristics of the production process.
In particular, the framework estimates multiple parameters. These include:
* *standard parameters* typically used in simulation;
* *domain-specific parameters* tailored to the manufacturing context. The latter allow the detection of different
behaviors within the process, such as the management of *worklists*, thus ensuring that the simulation reflects real-world production dynamics more accurately.
Once this is done the next step is to use the extracted model and simulation inputs to perform new simulations of the process, even changing the simulation parameters to generate what-if scenario.

In addition to the process discovery and parameter estimation features, the proposed framework extends to the management of incomplete traces of event logs. To address this problem, the framework implements an *analysis of the intermediate starting points*, i.e. the interruption points detected within the incomplete traces. Thanks to this feature, the framework is able to automatically identify the points where a process has been interrupted, analyze them and generate new ad-hoc data to allow the continuation of the simulation starting from those points.

## Getting Started
This section will guide you through setting up the tool and running on your local machine for development and testing purposes.

### Prerequisites

Before running the tool, ensure you have the following software installed:
* **Python** (version 3.10 or higher)
* **pip**
* **Required Libraries**: Install the dependencies listed in the `requirements.txt` file.

### Installation
Follow these steps to install the framework and its dependencies:

1. Clone the repository:
   ```bash
   git clone https://github.com/bpm-diag/parameters-estimation
   cd parameters-estimation
   ```

2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the script
Once the necessary requirements are installed, you can execute the tool from a terminal specifying the input event log name and any of the following parameters:

* `--file (required)`: event log in XES format, the event log must be previously located in the `input_file` folder
* `--output (optional, default=output)`: output folder for all files generated by the framework
* `--simthreshold (optional, default=0.9)`: similarity threshold for determining resource groups and timetables
* `--eta (optional, default=0.01)`: eta value of split miner algorithm, parameter to identify rare behaviors of the process
* `--eps (optional, default=0.001)`: epsilon value of split miner algorithm, parameter to identify parallel tasks


**Example of basic execution:**

```shell
PS C:\parameters-estimation> python main.py --file log_test3.xes
```

**Example of execution updating the input parameters**

```shell
PS C:\parameters-estimation> python main.py --file log_test3.xes --simthreshold 0.9 --eta 0.01 --eps 0.001
```

## Author
[Lorenzo Russo](https://github.com/lorenzoR21)