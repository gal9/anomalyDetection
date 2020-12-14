# Anomaly detection for streaming data

## Usage
`python main.py [-h] [-c CONFIG] [--f]`

| Short   |      Long     |  Description |
|----------|-------------|------|
| `-h` | `--help` | show help |
| `-c CONFIG` | `--config CONFIG` | name of the config file located in configuration folder (example: `config.json`) |
| `-f` | `--file` | If this flag is used the program will read data from file specified in config file instead of kafka stream|

## Architecture
The anomaly detection program consists of three main types of components:
1. Consumer component
2. Anomaly detection component
3. Output component
Each component has many implementations that are interchangeable. Which ones are used depends on the task the program is solving.
There is also an optional Visualization component which doesn't effect the general workflow and is used for streaming data visualization.

### Configuration file
The program is configured through configuration file specified with -c flag (located in configuration folder). It is a JSON file with the following structure:
```
{
    ...
    consumer configuration
    ...
    "anomaly_detection_alg": "anomaly detection algorithm",
    "anomaly_detection_conf": {
        ...
        anomaly detection configuration
        ...
        "output": ["list of output components"],
        "output_conf": ["list of output components configurations"],
        "visualization": ["list of visualization components"], # optional
        "visualization_conf":["list of visualization components configurations"] # optional
    }
}
```
The specific configurations for components will be presented in following chapters
For more details see example configuration files in configuration folder.

### Consumer
Consumer components differ in where the data is read from.
1. **Kafka consumer:** Data is read from kafka stream from a specified topic. The conciguration file must specify following parameters:
   * bootstrap_servers: Kafka server. (example: ["localhost:9092"])
   * auto_offset_reset": TODO (example: "latest")
   * enable_auto_commit": TODO (example: "True")
   * group_id": TODO (example "my-group")
   * value_deserializer": TODO (example "lambda x: loads(x.decode('utf-8'))")
   * topics": A list of topics streaming the data. (example ["anomaly_detection"])

2. **File consumer:** Data is read from a csv or JSON file. The csv must have a "test_value" column with the signal on which we are searching for anomalies and optionaly a "timestamp" column. The JSON file must be of shape `{"data": [{"timestamp": ..., "test_value": ..., "other_values": [...]}]}`. The configuration file must specify the following parameters:
   * file_name: The name of the file with the data, located in data/consumer/ directory. (example: "sin.csv")

### Output
Output component differs in where the data is outputted to. more than one output conmonent can be specified. It recieves three arguments from the anomaly detection component: value (the last value of the stream), timestamp and status (wether data is anomalous).
1. **Terminal output:** Timestamp, value and status are outputed to the terminal. It does not require any parameters in the configuration file.

2. **Kafka output:** Value is outputed to separate kafka topic. It requires the following argments in the config file:
    * output_topic: Name of the topic where the data will be stored (example: "anomaly_detection_EMA")
    * output_metric: Name of the stored metric. The data will be stored in the output topic under this key. (example: "EMA")\
    Example of use: config4.json in config folder.

3. **File output:** Data is outputed to a csv, JSON or txt file. It requires the following arguments in the config file:
   * file_name: The name of the file for output located in the log/ directory. (example: "output.csv")
   * mode: Wether we want to overwrite the file or just append data to it. (example: "a")

### Visualization
An optional conponent intendet to visualize the inputted stream. 
1. **Graph visualization:** The data is represented as points on graph. All anomaly detection component plot the test_value values and some plot additional values like running average, standard deviation... It requires the following arguments in the config file:
   * num_of_points: Maximum number of points of the same line that are visible on the graph at the same time. (example: 50)
   * num_of_lines: Number of lines plotted on the graph. (TODO: it depends on the anomaly detection algorithm so in future this component will be removed) (example: 4)
   * linestyles: A list, specifying the styles of the lines plotted. (example: ["wo", "r-", "b--", "b--"])

2. **Histogram visualization:** It visualizes the quantity of values, from test_value stream. It requires the following arguments in the config file:
   * num_of_bins: TODO (example: 50)
   * range: The interval shown on the histogram. (example: [0, 10])

### Anomaly detection
The component that does the actual anomaly detection. It recieves data from a consumer component and sends output to output components. 
1. **Border check:** A simple component that checks if the test_value falls within the specified interval and also gives warnings if it is close to the border. It requires the following arguments in the config file:
   * warning_stages: A list of floats from interval [0, 1] which represent different stages of warnings (values above 1 are over the border). (example: [0.7, 0.9])
   * UL: Upper limit of the specified interval. (example: 4)
   * LL: Lower limit of the specified interval. (example: 2)

2. **EMA:** Calculates the exponential moving average of test values. It recieves data from a consumer component and sends output to output components. 
EMA is calculated using past EMA values and the newest test value, giving more weigth to newer data. It is calculated in the following way:
EMA_latest = test_value x smoothing + EMA_last x (1 - smoothing).\
It requires the following arguments in the config file:
   * N : Parameter from which the smoothing is calculated - roughly translates to how many latest test values contribute to the EMA (example: 5)