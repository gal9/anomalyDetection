import csv
import json
from time import sleep
from json import dumps
from kafka import KafkaProducer
import numpy as np
from datetime import datetime

#Define producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))



#Send random data to topic - sine with noise in range 2-4

tab_data = [3, 4, 4, 4, 4, 5, 5, 5]
tab_data_csv = []

for e in range(9):
    timestamp = e
    # Normal distribution
    ran = float(np.random.normal(0, 0.1))

    # Sin with normal distribution error
    #ran = float(np.random.normal(0, 0.01) + np.sin(0.01*e))
    
    
    if(e%10 == 0):
        ran += 0.4
    data = {"test_value" : [tab_data[e]],
			"timestamp": str(datetime.now())}
    data_csv = {"test_value" : 3 + ran,
            "second": e,
			"timestamp": str(datetime.now())}
    #tab_data.append(data)
    tab_data_csv.append(data_csv)
	
    producer.send('anomaly_detection1', value=data)
    sleep(1) #one data point each second

"""with open("../data/consumer/sin.json", "w") as f:
    d = {"data": tab_data}
    json.dump(d, f)
"""
"""with open("../data/consumer/sin.csv", "w", newline="") as csv_file:
        fieldnames = ["timestamp", "test_value", "second"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tab_data_csv)
"""
