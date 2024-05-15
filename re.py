# import csv
# import xml.etree.ElementTree as ET
# import json
# from deepdiff import DeepDiff
# import xmltodict

# from ordered_set import OrderedSet

# xml_src = "/Users/ranjithrreddyabbidi/ranjith/xml1.xml"
# xml_target = "/Users/ranjithrreddyabbidi/ranjith/xml2.xml"
# xml_final_op = f'/Users/ranjithrreddyabbidi/ranjith'
# print("DEBUGGG")
# tree=ET.parse(xml_src)

# root=tree.getroot()

# tree1=ET.parse(xml_target)

# root1=tree1.getroot()
# xmlstr1 = ET.tostring (root, encoding='utf-8', method='xml').decode() 
# xmlstr2 = ET.tostring (root1, encoding='utf-8', method='xml').decode() 

# xmlstr1 = xmlstr1.replace('ns0:','')
# xmlstr2=xmlstr2.replace('ns0:','')

# print("DEBUGGG")

# def serialize(obj):
#     if isinstance(obj, OrderedSet):
#         return list(obj)
#     elif isinstance(obj, dict):
#         return {key: serialize(value) for key, value in obj.items()}
#     elif isinstance(obj, (list, tuple)):
#         return [serialize(item) for item in obj]
#     return obj

# src_json = xmltodict.parse (xmlstr1)
# print("DEBUGGG")
# target_json=xmltodict.parse(xmlstr2)
# print(src_json)
# print (target_json)
# diff=DeepDiff(src_json,target_json)
# print("*"*100)
# print (diff)
# print(json.dumps(diff, default=serialize))

# data_str = json.dumps(diff, default=serialize)

# try:
#     # Try to load the string as JSON
#     data = json.loads(data_str)
# except json.JSONDecodeError:
#     # If it's not in JSON format, assume it's already a dictionary
#     data = eval(data_str)

# output = {}
# for key, value in data.items():
#     if key == 'dictionary_item_added':
#         tagname = value[0].split("'")[-2]
#         output['tagname'] = f'<{tagname}>'
#         output['eod'] = None
#         output['Except'] = None
#         output['test-result'] = 'fail'
#     else:
#         nested_key = list(value.keys())[0]  # Get the nested key
#         tagname = nested_key.split("'")[-2]  # Extract the tagname from the nested key
#         output['tagname'] = f'<{tagname}>'
#         output['eod'] = value[nested_key]['new_value']
#         output['Except'] = value[nested_key]['old_value']
#         output['test-result'] = 'fail'


# print(output)
# ###################################################################



import re

input_string = "root['TxDtls']['RcncltnRpt'][1]['MtchgCrit']['TxMtchgCrit']['PltfmIdr']['Val1']"

# Define a regular expression pattern to match and capture the desired substring
pattern = r"'MtchgCrit'\]\['([^']+)'\]\['([^']+)'\]\['([^']+)'\](.*)"

# Search for the pattern in the input string
match = re.search(pattern, input_string)

if match:
    groups = match.groups()
    output_string = "<" + "><".join(groups[:-1]) + ">"
    print(output_string)
else:
    print("Pattern not found")


# {"dictionary_item_added": ["root['TxDtls']['RcncltnRpt'][1]['MtchgCrit']['CtrctMtchgCrit']['ISIN']"], "values_changed": {"root['TxDtls']['RcncltnRpt'][1]['MtchgCrit']['TxMtchgCrit']['PltfmIdr']['Val1']": {"new_value": "AAP", "old_value": "AAPA"}}}




# if key == 'dictionary_item_added':

# 	result = {tagname :'<CtrctMtchgCrit><ISIN>'
# 	eod : null
# 	Except : 
# 	test-result : fail}
# else:
# 	result = {tagname :'<TxMtchgCrit><PltfmIdr><Val1>'
# 	eod : AAP
# 	Except : AAPA
# 	test-result : fail}

from datetime import datetime, timedelta
from django.db.models import Max
from rest_framework.response import Response

# Retrieve jurisdiction from the request data
jurisdiction = request.data.get('jurisdiction')

try:
    res = []
    # Calculate the datetime for 48 hours ago
    last_hour_date_time = datetime.now() - timedelta(hours=48)

    # Query to get the latest creation date for each JSON within the last 48 hours
    latest_dates = SFComparePath.objects.filter(created_date__gte=last_hour_date_time) \
        .values('JSON') \
        .annotate(latest_date=Max('created_date'))

    # Fetch all records created within the last 48 hours
    all_records = SFComparePath.objects.filter(created_date__gte=last_hour_date_time) \
        .order_by('-created_date')

    # Create a dictionary to map each JSON to its latest creation date
    latest_date_dict = {item['JSON']: item['latest_date'] for item in latest_dates}

    # Iterate over all records to determine their status
    for record in all_records:
        latest_date = latest_date_dict.get(record.JSON)
        latest_str = "latest" if record.created_date == latest_date else "old"
        res.append({"req_id": record.req_id, "file": record.JSON, "status": latest_str})

    print(res)
    return Response({"detail": res}, status=200)

except Exception as e:
    import traceback
    traceback.print_exc()
    return Response({"detail": "An error occurred"}, status=500)


###############################################################
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.db.models import Max

try:
    res = []
    interval_hours = 24
    total_hours = 100

    # Calculate the number of intervals based on total hours and interval length
    num_intervals = total_hours // interval_hours

    # Start from the most recent interval and go back
    for i in range(num_intervals):
        start_time = datetime.now() - timedelta(hours=(i+1)*interval_hours)
        end_time = datetime.now() - timedelta(hours=i*interval_hours)

        # Fetch files created within the current interval
        files_within_interval = SFComparePath.objects.filter(created_date__gte=start_time, created_date__lt=end_time)
        
        # Find the latest creation date for each JSON file within the current interval
        latest_dates = files_within_interval.values('JSON').annotate(latest_date=Max('created_date'))
        latest_date_dict = {item['JSON']: item['latest_date'] for item in latest_dates}

        # Categorize files within the current interval
        for file in files_within_interval:
            latest_date = latest_date_dict.get(file.JSON)
            status = "latest" if latest_date and file.created_date == latest_date else "old"
            
            res.append({
                "req_id": file.req_id,
                "file": file.JSON,
                "created_date": file.created_date.strftime("%Y-%m-%d %H:%M"),  # Format the date if needed
                "status": status
            })

    print(res)
    return JsonResponse({"detail": "response"}, status=200)

except Exception as e:
    import traceback
    traceback.print_exc()
    return JsonResponse({"detail": str(e)}, status=500)


