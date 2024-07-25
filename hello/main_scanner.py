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
    alert_level_bleak_GATT_Characteristic = None
    
    # https://bleak.readthedocs.io/en/latest/api/index.html#bleak.backends.device.BLEDevice
    for device_idx, ble_device in enumerate(devices):
        
        # DEBUG
        print("")
        print(ble_device)
        
        print(device_idx+1, ") BLE Device.address:", ble_device.address)
        print(device_idx+1, ") BLE Device.name:", ble_device.name)
        
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
                
                # https://bleak.readthedocs.io/en/latest/api/index.html#bleak.backends.characteristic.BleakGATTCharacteristic
                bleak_GATT_service_characteristics = bleak_GATT_service.characteristics
                for characteristic_idx, bleak_GATT_Characteristic in enumerate(bleak_GATT_service_characteristics):
                    print("    ", characteristic_idx+1, ")", "Handle:", bleak_GATT_Characteristic.handle, "Description: ", bleak_GATT_Characteristic)
                    
                    if bleak_GATT_Characteristic.handle == 11:
                        alert_level_bleak_GATT_Characteristic = bleak_GATT_Characteristic
                    
        
                if alert_level_bleak_GATT_Characteristic is not None:
                    print("")
                    print("target characteristic (Alert Level) found!")
                    
                    print("char descriptors ...")
                    for char_descriptor_idx, char_descriptor in enumerate(alert_level_bleak_GATT_Characteristic.descriptors):
                        print(char_descriptor_idx, ")", char_descriptor)
                    print("char descriptors done.")
                    
                    MY_CHARACTERISTIC_UUID = "00002a06-0000-1000-8000-00805f9b34fb"
                    for x in range(3):
                        
                        # USER LED1 will blink
                        print("Alert Level 1")
                        await client.write_gatt_char(alert_level_bleak_GATT_Characteristic, b'\x01', response=False)
                        await asyncio.sleep(5)
                        
                        # USER LED1 constantly on
                        print("Alert Level 2")
                        await client.write_gatt_char(alert_level_bleak_GATT_Characteristic, b'\x02', response=False)
                        await asyncio.sleep(5)
                        
                        # USER LED1 off
                        print("Alert Level 0")
                        await client.write_gatt_char(alert_level_bleak_GATT_Characteristic, b'\x00', response=False)
                        await asyncio.sleep(5)
                    
            await client.disconnect()
        
        
        
                    
asyncio.run(main())