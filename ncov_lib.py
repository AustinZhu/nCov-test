# -*- coding: utf-8 -*-

import requests
import json

class nCov:
    def __init__(self):
        pass

    def get_data(self):
        """
        Get the latest data from DXY
        save data in json file
        """
        response = requests.get("https://lab.isaaclin.cn/nCoV/api/area", {'latest':1})
        data = response.json()
        with open('db/data.json', 'w') as f:
            json.dump(data, f)
        f.close()

    def get_coordinate(self):
        """
        Get coordinates of countries and regions from overpassAPI
        return list object containing dicts with name, confirmed_count, lat, and lon
        """
        overpass_url = "http://overpass-api.de/api/interpreter"
        query_header = "[out:json][timeout:300];"
        query_body = ""
        query_footer = "out;"
        formatter = "node['name:en'=\"{}\"]['place'=];"
        return_list = list()

        with open('db/data.json', 'r') as fin:
            result = json.load(fin)["results"]
        fin.close()
        for record in result:
            elements = dict()
            country = record["provinceEnglishName"]
            print(country)
            elements["regionName"] = country
            elements["totalConfirmed"] = record["confirmedCount"]

            query_body = formatter.format(country)
            overpass_query = query_header + query_body + query_footer
            try:
                response = requests.get(overpass_url,{"data":overpass_query})
                json_object = response.json()
                data = json.loads(json.dumps(json_object))
                lat, lon = (data["elements"][0])["lat"], (data["elements"][0])["lon"]
                elements["lat"] = lat
                elements["lon"] = lon
            except:
                continue
            else:
                print(elements["regionName"])
                return_list.append(elements)
        return return_list

    def _weight(self, patient_count):
        if patient_count == 1:
            weight = 0.1
        elif patient_count > 1 and patient_count <= 10:
            weight = 0.02 * (patient_count + 10)
        elif patient_count > 10 and patient_count <= 100:
            weight = 0.002 * (patient_count + 200)
        elif patient_count > 100 and patient_count <= 1000:
            weight = 0.0002 * (patient_count + 3000)
        elif patient_count > 1000 and patient_count <= 10000:
            weight = 0.00002 * (patient_count + 40000)
        elif patient_count > 10000:
            weight = 1
        return weight

    def out_json(self):
        query_result = dict()
        query_result["data"] = self.get_coordinate()
        fout = open('db/skimmedData.json', 'w')
        json.dump(query_result, fout)
        fout.close()

    def out_js(self):
        fin = open('db/skimmedData.json', 'r')
        data = json.load(fin)["data"]
        fin.close()

        body = ""
        head = "var addressPoints = ["
        foot = "[0,0,0]];"
        for location in data:
            js_list = list()
            js_list.append(location["lat"])
            js_list.append(location["lon"])
            js_list.append(self._weight(location["totalConfirmed"]))
            body = body + str(js_list) + ','
        fout = open('db/pt.js', 'w')
        fout.write(head+body+foot)
        fout.close()