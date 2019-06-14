import cos_backend
import json


def main(args):
    config = args['config']
    cos = cos_backend.COSBackend(config['ibm_cos'])

    i = 0
    result = {}

    while i < args['n_partitions']:
        file_list = cos.list_objects(args['bucket'], str(i+1)+args['file_name'])

        if len(file_list) != 0:
            map_result = json.loads(cos.get_object(args['bucket'], str(i+1)+args['file_name']+'.map').decode('latin-1'))
            cos.delete_object(args['bucket'], str(i+1)+args['file_name']+'.map')

            for item in map_result.keys():
                if item in result:
                    result[item] = result[item] + map_result[item]
                else:
                    result[item] = map_result[item]

            i += 1

    cos.put_object(args['bucket'], args['file_name']+'.reduce', json.dumps(result))

    return result
