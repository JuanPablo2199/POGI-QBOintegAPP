import requests
from django.conf import settings
import http.client
import json
import sys

def qbo_api_call(access_token, realm_id):
        pogi_url = "" # Insert your Pogi server URL here
        user_id = ""  # Insert your Pogi user ID here
        user_pwd = "" # Insert your Pogi password here

        if not user_id or not user_pwd:
            print("You'll need a valid URL, user id and password to connect to PogiAPI")
            sys.exit()


        print("GET the version info")
        version_rs = requests.get(pogi_url, params={ "op": "version" })

        # Check the return status, and print the response text
        if (version_rs.status_code == 200):
            print(version_rs.text)
        else:
            print('Something went wrong')

        print("Authenticate via username and password (returns token)")
        # POST auth
        token_rs = requests.post(pogi_url, params={ "op": "token-get", "userId": user_id, "password": user_pwd })

        # Check the return status, and print the response text
        if (token_rs.status_code == 200):
            print(token_rs.text)
        else:
            print('Something went wrong')


        print("Store Token from response")
        token_data = token_rs.json()
        print(token_data, token_data["token"])
        if "token" in token_data:
            token = token_data["token"]
            print("Token: " + token)
        elif "error" in token_data:
            print("Error: " + token_data["error"])
        else:
            print("Unknown error encountered")


        print("Get inventory history list")
        inventory_params = {
            "op": "history",
            "token": token,
            "fromDate": "",
            "fromTime": "",
            "toDate": "",
            "toTime": "",
            "marker": "",
            "event": "present",
            "zone": "",
            "limit": 1000,
            "offSet": 0,
            "currentLocation": "on",
            "namedOnly": "",
            "tagAssetSearchType": "tag",
            "tagAndAssetSearchType": "tag",
            "tagAndAsset": "",
            "orderColumn": "update_date",
            "orderDirection": "DESC"
        }
        inventory_rs=requests.post(pogi_url, params=inventory_params)
        json_data1 = json.loads(inventory_rs.text)
        print(json_data1)
        print(json_data1['count'])
        print(len(json_data1['data']))
        print("Loop through the items")

        #return requests.post(pogi_url, params=inventory_params)

        """[summary]

        """
        if settings.ENVIRONMENT == 'production':
                base_url = settings.QBO_BASE_PROD
        else:
                base_url =  settings.QBO_BASE_SANDBOX

        route = '/v3/company/{0}/query?minorversion=14'.format(realm_id)
        auth_header = 'Bearer {0}'.format(access_token)
        payload = "select * from item startposition 1 "
        headers = {
            'Authorization': auth_header,
            'Accept': 'application/json',
            'Content-Type': 'application/text'

        }
        response1 = requests.post('{0}{1}'.format(base_url, route), data=payload, headers=headers)
        json_data = json.loads(response1.text)
        print(json_data)
        print("xxx")
        print("Loop through the items")

        json1 = json.dumps(json_data,sort_keys = True)
        json2 = json.dumps(json_data1,sort_keys = True)
        print(json1==json2)
        print(len(inventory_rs.json()['data']))
        for item in json_data1['data']:
            for data in json_data['QueryResponse']['Item']  :
                if item['tag_id'] == data['Name']:

                    route = '/v3/company/{0}/item?minorversion=4'.format(realm_id)
                    auth_header = 'Bearer {0}'.format(access_token)
                    headers = {
                        'Authorization': auth_header,
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    }

                    payload = json.dumps({
                      "Name": data['Name'],
                      "Active": data['Active'],
                      "FullyQualifiedName": data['FullyQualifiedName'],
                      "Taxable": data['Taxable'],
                      "UnitPrice": data['UnitPrice'],
                      "Type": data['Type'],
                      "IncomeAccountRef": {
                        "value": data['IncomeAccountRef']['value'],
                        "name": data['IncomeAccountRef']['name']
                      },
                      "PurchaseCost": data['PurchaseCost'],
                      "ExpenseAccountRef": {
                        "value": data['ExpenseAccountRef']['value'],
                        "name": data['ExpenseAccountRef']['name']
                      },
                      "AssetAccountRef": {
                        "value":data['AssetAccountRef']['value'],
                        "name": data['AssetAccountRef']['name']
                      },
                      "TrackQtyOnHand": data['TrackQtyOnHand'],
                      "QtyOnHand": 120,
                      "InvStartDate": data['InvStartDate'],
                      "domain": data['domain'],
                      "sparse": data['sparse'],
                      "Id": data['Id'],
                      "SyncToken": data['SyncToken']
                    })
                    response = requests.post('{0}{1}'.format(base_url, route), data=payload, headers=headers)
                    print(response.status_code)
                    print(response.text)
        else:
                    for item in json_data1['data']:
                            route = '/v3/company/{0}/item?minorversion=4'.format(realm_id)
                            auth_header = 'Bearer {0}'.format(access_token)
                            headers = {
                                'Authorization': auth_header,
                                'Accept': 'application/json',
                                'Content-Type': 'application/json'
                            }

                            payload = json.dumps({
                               "Name": item['tag_id'],
                               "IncomeAccountRef": {
                                 "value": "79",
                                 "name": "Sales of Product Income"
                               },
                               "ExpenseAccountRef": {
                                 "value": "80",
                                 "name": "Cost of Goods Sold"
                               },
                               "AssetAccountRef": {
                                 "value": "81",
                                 "name": "Inventory Asset"
                               },
                               "Type": "Inventory",
                               "TrackQtyOnHand": True,
                               "QtyOnHand": 10,
                               "InvStartDate": "2015-01-01"
                            })
                            response = requests.post('{0}{1}'.format(base_url, route), data=payload, headers=headers)
                            print(response.status_code)
                            print(response.text)


def qbo_create_api(access_token, realm_id):
    """[summary]

    """

    if settings.ENVIRONMENT == 'production':
        base_url = settings.QBO_BASE_PROD
    else:
        base_url =  settings.QBO_BASE_SANDBOX

    route = '/v3/company/{0}/item?minorversion=14'.format(realm_id)
    auth_header = 'Bearer {0}'.format(access_token)
    headers = {
        'Authorization': auth_header,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    payload = json.dumps({
      "Name": "E2003A8B511C3309C2C33A38",
      "IncomeAccountRef": {
        "value": "79",
        "name": "Sales of Product Income"
      },
      "ExpenseAccountRef": {
        "value": "80",
        "name": "Cost of Goods Sold"
      },
      "AssetAccountRef": {
        "value": "81",
        "name": "Inventory Asset"
      },
      "Type": "Inventory",
      "TrackQtyOnHand": True,
      "QtyOnHand": 13,
      "InvStartDate": "2015-01-01"
    })
    response = requests.post('{0}{1}'.format(base_url, route), data=payload, headers=headers)
    print(response.status_code)
    print(response.text)
    #return requests.put('{0}{1}'.format(base_url, route), data=payload, headers=headers)

def getpush_api():
    pogi_url = "https://pogi-alpha.simplyrfid.com/api" # Insert your Pogi server URL here
    user_id = "johnpaul.pineda@simplyrfid.com"  # Insert your Pogi user ID here
    user_pwd = "ThisIsMySecurePassword33!" # Insert your Pogi password here

    if not user_id or not user_pwd:
        print("You'll need a valid URL, user id and password to connect to PogiAPI")
        sys.exit()


    print("GET the version info")
    version_rs = requests.get(pogi_url, params={ "op": "version" })

    # Check the return status, and print the response text
    if (version_rs.status_code == 200):
        print(version_rs.text)
    else:
        print('Something went wrong')

    print("Authenticate via username and password (returns token)")
    # POST auth
    token_rs = requests.post(pogi_url, params={ "op": "token-get", "userId": user_id, "password": user_pwd })

    # Check the return status, and print the response text
    if (token_rs.status_code == 200):
        print(token_rs.text)
    else:
        print('Something went wrong')


    print("Store Token from response")
    token_data = token_rs.json()
    print(token_data, token_data["token"])
    if "token" in token_data:
        token = token_data["token"]
        print("Token: " + token)
    elif "error" in token_data:
        print("Error: " + token_data["error"])
    else:
        print("Unknown error encountered")


    print("Get inventory history list")
    inventory_params = {
        "op": "history",
        "token": token,
        "fromDate": "",
        "fromTime": "",
        "toDate": "",
        "toTime": "",
        "marker": "",
        "event": "present",
        "zone": "JP Test",
        "limit": "",
        "offSet": 0,
        "currentLocation": "on",
        "namedOnly": "",
        "tagAssetSearchType": "tag",
        "tagAndAssetSearchType": "tag",
        "tagAndAsset": "",
        "orderColumn": "update_date",
        "orderDirection": "DESC"
    }
    return requests.post(pogi_url, params=inventory_params)
