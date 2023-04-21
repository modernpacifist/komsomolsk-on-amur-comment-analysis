# this script simplifies some of the fields into more readable format

import json


def convert_likes(raw_json):
    updated_js = []

    # converting list of likes into integer
    for j in raw_json:
        attributes = j.get('attributes')
        if attributes is None:
            continue
        submission_likes_count = len(attributes.get('submissionLikes').get('data'))
        j['submissionLikes'] = submission_likes_count
        del j['attributes']['submissionLikes']
        updated_js.append(j)

    return updated_js


def flatten_json(raw_json):
    res = []
    for y in raw_json:
        out = {}
        def flatten(x, name=''):
            # If the Nested key-value
            # pair is of dict type
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + '_')
            # If the Nested key-value
            # pair is of list type
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + '_')
                    i += 1
            else:
                out[name[:-1]] = x
    
        flatten(y)
        res.append(out)

    return res


if __name__ == '__main__':
    try:
        with open("./datasets/submissionsWithForms.json") as f:
            js = json.load(f)
    except Exception as e:
        print(e)
        exit(1)

    updated_js = convert_likes(js)
    updated_js = flatten_json(updated_js)

    with open('./datasets/submissionsWithFormsCleanLikes.json', 'w') as f:
        # json.dump(updated_js, f, ensure_ascii=False, indent=4)
        json.dump(updated_js, f, ensure_ascii=False, indent=4)
