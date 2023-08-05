# digitreck-python
**digitreck-python** library enables Python applications to connect to digiTreck servers in a fast and convenient way. It enables using digiTreck APIs as methods alongwith header and checksum management.

## 1. Adding Dependency
Easiest way to integrate digitreck library to your app is through **pip**
```script
pip install digitrecklib
```

## 2. Initialize the Library
To initialize the library, get Project API Key and Private key from the dashboard.
```python
config = {
  Config.SERVER_KEY: REPLACE_WITH_API_KEY_FROM_PROJECT, 
  Config.PRIVATE_KEY: REPLACE_WITH_SECRET_SALT_FROM_PROJECT
}
requester = Digitreck(config).getInstance()
```

## 3. Next Steps
Congratulations! You have successfully performed the basic integration. Now lets move to performing functions like location management and session management.

* ### Location Management
 **1. Device Location**
```python
device_id = DEVICE_ID

result = helper.getLocation(device_id)
```

 **2. Device Path**
```python
device_id = NAUTILUS_DEVICE_ID_1
start_date = "2017-02-20T19:34:01.326Z"
end_date = "2017-02-20T19:34:01.326Z"

result = helper.getPath(device_id, start_date, end_date)
```

 **3. Nearby Device**
```python
count = RESULT_COUNT
access_key = ACCESS_KEY
lat = LATITUDE
lng = LONGITUDE
range = RADIUS

result = helper.getNearbyDevice(count, access_key, lat, lng, range)
```

* ### Session Management
 **1. Creating a Tracking session**
```python
device_list = [
  DEVICE_ID_1, 
  DEVICE_ID_2
]

result = requester.createSessions(device_list)
```

 **2. Releasing a Tracking session**
```python
tracking_id = TRACKING_SESSION_ID

result = helper.releaseSession(tracking_id)
```
