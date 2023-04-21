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


if __name__ == '__main__':
    try:
        with open("./datasets/submissionsWithForms.json") as f:
            js = json.load(f)
    except Exception as e:
        print(e)
        exit(1)

    updated_js = convert_likes(js)

    # for j in js:
    #     attributes = j.get('attributes')
    #     if attributes is None:
    #         continue
    #     submission_likes_count = len(attributes.get('submissionLikes').get('data'))
    #     j['attributes']['submissionLikes'] = submission_likes_count
    #     updated_js.append(j)

    # json.dumps()
    with open('./datasets/submissionsWithFormsCleanLikes.json', 'w') as f:
        json.dump(updated_js, f, ensure_ascii=False, indent=4)
