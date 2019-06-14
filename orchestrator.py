import yaml
import cos_backend
import ibm_cf_connector
import sys
import time


def invoke_countingword(data, cf):
    data["start"] = 0
    data["end"] = data['part_size']

    i = 0

    while i < data['n_partitions']:
        data['partition'] = i + 1
        cf.invoke('mapCountingWords', data)

        data["start"] = data["end"] + 1
        data["end"] += data['part_size']

        if i == data['n_partitions'] - 1:
            data["end"] += data['final_size']
        i += 1


def invoke_wordcount(data, cf):
    data["start"] = 0
    data["end"] = data['part_size']

    i = 0

    while i < data['n_partitions']:
        data['partition'] = i + 1
        cf.invoke('mapWordCount', data)

        data["start"] = data["end"] + 1
        data["end"] += data['part_size']

        if i == data['n_partitions'] - 1:
            data["end"] += data['final_size']
        i += 1


def main():
    try:
        with open('.ibm_cloud_config', 'r') as config_file:
            config = yaml.safe_load(config_file)

    except:
        print("Configuration file 'ibm-cloud_config' not found.\n")
        exit(1)

    if len(sys.argv) != 3:
        print("Usage:\n\torchestrator.py INPUT_FILE PARTITIONS\n")
        exit(2)

    try:
        int(sys.argv[2])
    except ValueError:
        print("Wrong parameter format.\nUsage:\n\torchestrator.py INPUT_FILE PARTITIONS\n")
        exit(3)

    if int(sys.argv[2]) < 1:
        print("The number of partitions must be greater than 0.\n")
        exit(4)

    cos = cos_backend.COSBackend(config['ibm_cos'])
    cf = ibm_cf_connector.CloudFunctions(config['ibm_cf'])

    file_name = sys.argv[1]
    partitions = int(sys.argv[2])

    data = {}
    data['config'] = config
    data['n_partitions'] = partitions
    data['file_name'] = file_name
    data['bucket'] = 'sdtp1'
    data['file_size'] = int(cos.head_object(data['bucket'], file_name))
    data['part_size'] = int(data['file_size'] / data['n_partitions'])
    data['final_size'] = int(data['file_size'] % data['n_partitions'])

    start_time = time.time()
    invoke_countingword(data, cf)
    cf.invoke_with_result('reduce', data)
    final_time = time.time()

    print('Counting Words execution time: ' + '{:.3f}'.format(final_time - start_time))
    cos.delete_object(data['bucket'], data['file_name'] + '.reduce')

    start_time = time.time()
    invoke_wordcount(data, cf)
    cf.invoke_with_result('reduce', data)
    final_time = time.time()

    print('Word Count execution time: ' + '{:.3f}'.format(final_time - start_time))

    exit(0)


if __name__ == "__main__":
    main()
