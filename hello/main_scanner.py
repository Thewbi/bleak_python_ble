import asyncio
from bleak import BleakScanner, BleakClient

# python -m venv --system-site-packages venv
# venv\Scripts\activate
# Behind proxy:     pip install --proxy http://<YOUR_PROXY>:8080 bleak
# Not behind proxy: pip install bleak
#
# python main_scanner.py
#
# deactivate
async def main():
    
    devices = await BleakScanner.discover()
    
    target_ble_device = None
    
    # https://bleak.readthedocs.io/en/latest/api/index.html#bleak.backends.device.BLEDevice
    for idx, ble_device in enumerate(devices):
        
        # DEBUG
        print("")
        print(ble_device)
        
        print(idx, ") BLE Device.address:", ble_device.address)
        print(idx, ") BLE Device.name:", ble_device.name)
        
        print(type(ble_device.name))
        
        # details - The OS native details required for connecting to the device.
        ble_device_details = ble_device.details
        #print(type(ble_device_details))
        
        #unknown = ble_device_details[0]
        #print(type(unknown))
        #print(unknown)
        
        # Find Me Target
        if ble_device.name:
            
            print(ble_device.name.lower())
            print("Find Me Target".lower())
            
            if ble_device.name.lower() == "Find Me Target".lower():
                target_ble_device = ble_device
        
    if target_ble_device is not None:
        print("")
        print("target device found")
        
        async with BleakClient(target_ble_device.address) as client:
            #svcs = await client.get_services()
            #print("Services:")
            #for service in svcs:
            #    print(service)
                
            bleak_GATT_service_collection = client.services
            print(bleak_GATT_service_collection)
            
            # https://bleak.readthedocs.io/en/latest/api/index.html#bleak.backends.service.BleakGATTServiceCollection
            bleak_GATT_service_dict = bleak_GATT_service_collection.services
            print(bleak_GATT_service_dict)
            
            print("Services:")
            for service_handle, bleak_GATT_service in bleak_GATT_service_dict.items():
                
                print(service_handle, ")", bleak_GATT_service)
                
                # https://bleak.readthedocs.io/en/latest/api/index.html#bleak.backends.service.BleakGATTService
                print(bleak_GATT_service.description)
        
asyncio.run(main())