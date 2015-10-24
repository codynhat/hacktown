import requests
city = 'Portland'
state='Oregon'
# payload = {'city': city,'state': state}
payload = {'location': 'Eugene, Oregon'}
r = requests.get('http://www.mapquestapi.com/geocoding/v1/address?',data={
    'key': '7N1MeC0H0uFcbyzovGkG8SPFu5SdPUjU',
    'inFormat': 'json',
    'outFormat':'json',
    'maxResults': 1,
},params=payload);

re = r.json()
latLng = re['results'][0]['locations'][0]['latLng']
print(latLng)
