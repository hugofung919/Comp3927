from django.shortcuts import render

# Create your views here.
# Json
import json
from datetime import date, timedelta
import requests
import collections
import operator

# Getting date ( Today -1)
today = date.today()
yesterday = today - timedelta(days=1)
date = yesterday.strftime("%d/%m/%Y")
# print(d1)

# Getting the Centres capacity
json1 = {
    "resource": "http://www.chp.gov.hk/files/misc/occupancy_of_quarantine_centres_eng.csv",
    "section": 1,
    "format": "json",
    "sorts": [[8, "desc"]],
    "filters": [[1, "eq", [date]]]
}
json_string = json.dumps(json1)
r = requests.get('https://api.data.gov.hk/v2/filter?q=' + json_string)
a = r.json
# print(type(a))
r1 = json.loads(r.text)
# web after endcode
# print(r.url)

# Getting the total units in use and available
sum_data = sum(d.get('Capacity (unit)', 0) for d in r1)
sum_data2 = sum(d.get('Ready to be used (unit)', 0) for d in r1)
# checking the data type
# print(type(sum_data))
# print(sum_data)
# print(sum_data2)

# Getting the highest units available
sum_data3 = r1[0]
# print(sum_data3)

# centrename
name = sum_data3.get('Quarantine centres')
# print(name)
units = sum_data3.get('Ready to be used (unit)')
# print(units)

# Getting the Number of persons quarantined
ppl = sum(d.get("Current person in use", 0) for d in r1)
# print(ppl)


######
# Getting the Non-close contacts
json2 = {
    "resource": "http://www.chp.gov.hk/files/misc/no_of_confines_by_types_in_quarantine_centres_eng.csv",
    "section": 1,
    "format": "json",
    "sorts": [[6, "desc"]],
    "filters": [[1, "eq", [date]]]
}
json_string1 = json.dumps(json2)
rr = requests.get('https://api.data.gov.hk/v2/filter?q=' + json_string1)
aa = rr.json
# print(type(a))
rr1 = json.loads(rr.text)
# print(rr.url)
# print(rr.text)

# get the data dict and data
case_data = rr1[0]
ppl2 = case_data.get("Current number of close contacts of confirmed cases")


# print(ppl2)

# context = {"data": [
#     {"date": date}, {'sum_data': sum_data},
#     {'sum_data2': sum_data2}, {"name": name}, {"units": units}]}
# print(context)


def dashboard1(request):
    context = {"data": [
        {"date": date}, {'sum_data': sum_data},
        {'sum_data2': sum_data2}, {"name": name}, {"units": units},
        {"Connected": True}, {"has_data": True},
        {"quarantined": ppl}, {"quarantined2": ppl2}]}
    return render(request, 'dashboard1.html', context=context)


def dashboard2(request):
    context = {"data": [
        {"date": date}, {'sum_data': sum_data},
        {'sum_data2': sum_data2}, {"name": name}, {"units": units},
        {"Connected": True}, {"has_data": True},
        {"quarantined": ppl}, {"quarantined2": ppl2}]}
    return render(request, 'dashboard2.html', context=context)

def dashboard3(request):
    if ppl == ppl2:
        context = {"data": [
            {"date": date}, {'sum_data': sum_data},
            {'sum_data2': sum_data2}, {"name": name}, {"units": units},
            {"Connected": True}, {"has_data": True},
            {"quarantined": ppl}, {"quarantined2": ppl2},
            {"count_consistent": True}
        ]}
        return render(request, 'dashboard3.html', context=context)
    else:
        context = {"data": [
            {"date": date}, {'sum_data': sum_data},
            {'sum_data2': sum_data2}, {"name": name}, {"units": units},
            {"Connected": True}, {"has_data": True},
            {"quarantined": ppl}, {"quarantined2": ppl2},
            {"count_consistent": False}
        ]}
        return render(request, 'dashboard3.html', context=context)
