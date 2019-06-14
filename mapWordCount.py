import cos_backend
import json
import re


def main(args):
    config = args['config']
    cos = cos_backend.COSBackend(config['ibm_cos'])
    line = cos.get_object(args['bucket'], args['file_name'],
                          extra_get_args={'Range': 'bytes=' + str(args['start']) + '-' + str(args['end'])}
                          ).decode('latin-1').lower()
    line = re.sub(r'[-,;.:?¿!¡\'\(\)\[\]\"*+-_<>#$€&^%|]', " ", line).split()

    result = {}

    for word in line:
        if word in result.keys():
            result[word] += 1
        else:
            result[word] = 1

    cos.put_object(args['bucket'], str(args['partition']) + args['file_name'] + '.map', json.dumps(result))

    return {"status": "ok"}
