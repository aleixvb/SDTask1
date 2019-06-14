# SDTask1
### Introduction
Contains the files from Distributed Systems first task. The goal of this task is to understand and use communication models and middleware concepts and implement the MapReduce model. 

MapReduce is a programming model and implementation to enable the parallel processing of huge amounts of data. In a nutshell, it breaks a large dataset into smaller chunks to be processed separately on different worker nodes and automatically gathers the results across the multiple nodes to return a single result.

As it name suggests, it allows for distributed processing of the map() and reduce() functional operations, which carry out most of the programming logic.

Here you can see the general process of MapReduce for counting the frequence of each word, what is known as Wordcount. Each map phase receives its input and prepares intermediary key as pairs of (key,value), where the key is the actual word and the value is the word's current frequency, namely 1. Shuffling phase guarantees that all pairs with the same key will serve as input for only one reducer, so in reduce phase we can very easily calculate the frequency of each word.
![alt text](https://www.todaysoftmag.com/images/articles/tsm33/large/a11.png)

### Configuration & Execution
To run the project, your system should have installed Python3, IBM Cloud Functions Client, and the following packages:
```
pip3 install boto3
pip3 install ibm-cos-sdk
```
Once this is done, we can proceed to run the following script in the project directory:
```
./startCF
```
Finally, we can run the application using this next line:
```
pyhton3 orchestrator.py DATASET NUMBER_OF_MAPS
```
**Note:** To run the project successfully, the user must have the IBM configuration file correctly edited to connect to his COS and CF.
