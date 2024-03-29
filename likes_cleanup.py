# this script simplifies some of the fields into more readable format

import json

from russiannames.parser import NamesParser


NAMEPARSER = NamesParser()


def convert_likes(raw_json):
    updated_js = []

    # converting list of likes into integer
    for j in raw_json:
        attributes = j.get('attributes')
        if attributes is None:
            continue
        submission_likes_count = len(attributes.get('submissionLikes').get('data'))
        j['SubmissionLikes'] = submission_likes_count
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


def rename_field(raw_json, old_field_name, new_field_name):
    if not all([old_field_name, new_field_name]):
        return raw_json
    res = []
    for i in raw_json:
        i[new_field_name] = i.pop(old_field_name)
        res.append(i)
    return res


def delete_field(raw_json, field_name):
    if not field_name:
        return raw_json
    res = []
    for i in raw_json:
        if not field_name in i:
            res.append(i)
            continue
        del i[field_name]
        res.append(i)
    return res


def drop_fields_except(raw_json, fields_to_keep):
    res = []
    for i in raw_json:
        new_dict = {key: value for key, value in i.items() if key in fields_to_keep}
        res.append(new_dict)
    return res


def add_gender_field(raw_json):
    res = []
    for i in raw_json:
        i['Gender'] = NAMEPARSER.parse(i.get('ContactName')).get('gender')
        res.append(i)
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
    updated_js = rename_field(updated_js, "attributes_feature_properties_data_type", "Category")
    updated_js = rename_field(updated_js, "attributes_feature_properties_data_description", "Description")
    updated_js = rename_field(updated_js, "attributes_feature_properties_data_participation", "Participation")
    updated_js = rename_field(updated_js, "attributes_feature_properties_data_money", "Money")
    updated_js = rename_field(updated_js, "attributes_feature_properties_data_age", "Age")
    updated_js = rename_field(updated_js, "attributes_feature_properties_data_contactName", "ContactName")
    updated_js = rename_field(updated_js, "attributes_feature_properties_data_time", "LiveTime")
    updated_js = rename_field(updated_js, "attributes_feature_type", "FeatureType")
    updated_js = rename_field(updated_js, "attributes_feature_geometry_type", "GeometryType")
    updated_js = rename_field(updated_js, "attributes_feature_geometry_coordinates_0", "CoordinatesLongitude")
    updated_js = rename_field(updated_js, "attributes_feature_geometry_coordinates_1", "CoordinatesLatitude")
    updated_js = rename_field(updated_js, "attributes_createdAt", "CreatedAt")
    updated_js = add_gender_field(updated_js)

    fields_to_keep = ["id", "SubmissionLikes", "Category", "Description", "Participation", "Money", "Age", "ContactName", "LiveTime", "FeatureType", "GeometryType", "CoordinatesLongitude", "CoordinatesLatitude", "CreatedAt", "Gender"]
    updated_js = drop_fields_except(updated_js, fields_to_keep)

    with open('./datasets/CleanSubmissionsWithForms.json', 'w') as f:
        json.dump(updated_js, f, ensure_ascii=False, indent=4)

