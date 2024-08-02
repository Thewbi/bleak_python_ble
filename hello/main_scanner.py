import sys
import asyncio
from bleak import BleakScanner, BleakClient

from ctypes import *

# uint16_t checksum = 0;
# 	for (int i = 0; i < (length-3); i++)
# 	{
# 		checksum += buffer[i];
# 	}
# 	*checksum_1 = (checksum >> 7) | 0x80;
# 	*checksum_2 = (checksum >> 0) | 0x80;
 
def compute_checksum(data: bytearray):
    cs = 0    
    for idx in range(len(data)-3):
        cs += data[idx]
        #print("cs=", hex(cs), "byte=", hex(data[idx]))
        
    #shift_left_seven = (cs >> 7)
    #print("shift_left_seven=", hex(shift_left_seven))
    
    #print("shift_left_seven_80=", hex(shift_left_seven | 0x80) )
        
    checksum_high = (cs >> 7) & 0xFF | 0x80;
    checksum_low  = (cs >> 0) & 0xFF | 0x80;
    
    #print("checksum_high=", hex(checksum_high))
    #print("checksum_low=", hex(checksum_low))
    
    return checksum_high, checksum_low

def notification_handler(sender: int, data: bytearray):
    print("notification_handler")
    #"""Simple notification handler which prints the data received."""
    #data1 = list(data)
    #data2 = ((data1[1]+data1[2]*256)*0.005)
    #print("{0}: {1}".format(sender, data2))
    print(sender)
    #print(data)
    
    for byte in data:
        print("[" + hex(byte) + "]")
        
    checksum_low, checksum_high = compute_checksum(data)
    
    data_len = len(data)
    
    if data[data_len - 3] != checksum_low or data[data_len - 2] != checksum_high:
        print("Checksum incorrect!")
    else:
        print("Checksum correct!")
        
        target_address = data[1]
        if target_address == 0x32:
            print("TargetAddress", hex(target_address), "Terminal")
            
        command = data[2]
        if command == 0xB8:
            print("Command", hex(command), "TYPE_AND_VERSION_RESPONSE")
        
        product_type = data[3]
        product_type = product_type & 0x7F
        if product_type == 0x04:
            print("ProductType", hex(product_type), "RevolvingDoor")
            
        product_code = data[4]
        product_code = product_code & 0x7F
        if product_code == 0x3D:
            print("ProductType", hex(product_type), "DCU6 + DCU610 + DCU610 REVO PRIME")
            
        product_variant = data[5]
        product_variant = product_variant & 0x7F
        if product_variant == 0x00:
            print("ProductVariant", hex(product_variant), "Variant 0")
            
        hardwareRevision = (data[6] & 0x7F)
        print("hardwareRevision", hex(hardwareRevision), chr(hardwareRevision))
        
        assemblyVersion = (data[7] & 0x7F)
        print("assemblyVersion", hex(assemblyVersion), chr(assemblyVersion))
  
        softwareVersion = (data[8] & 0x7F)
        print("softwareVersion", hex(softwareVersion), chr(softwareVersion))
  
        softwareRevision = (data[9] & 0x7F)
        print("softwareRevision", hex(softwareRevision), chr(softwareRevision))
  
        softwareSubVersion = (data[10] & 0x7F)
        print("softwareSubVersion", hex(softwareSubVersion), chr(softwareSubVersion))
        

# cd C:\aaa_se\python\bleak_python_ble\hello
# python -m venv --system-site-packages venv
# venv\Scripts\activate
# Behind proxy:     pip install --proxy http://<YOUR_PROXY>:8080 bleak
# Not behind proxy: pip install bleak
#
# python main_scanner.py
#
# deactivate
async def main():
    
    # # 02 32 B8 84 BD 80 C1 B0 B1 B0 F6 8C F5 03
    # temp_data = [0x02, 0x32, 0xB8, 0x84, 0xBD, 0x80, 0xC1, 0xB0, 0xB1, 0xB0, 0xF6, 0x8C, 0xF5, 0x03]

    # # convert list to bytearray
    # byte_array = bytearray(temp_data)
    
    # checksum_low, checksum_high = compute_checksum(byte_array)
    
    # data_len = len(byte_array)
    
    # if byte_array[data_len - 3] != checksum_low or byte_array[data_len - 2] != checksum_high:
    #     print("Checksum incorrect!")
    #     sys.exit()
    # else:
    #     print("Checksum correct!")
    
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
                
    if target_ble_device is None:
        print("")
        print("[ABORT] target device not found! Aborting application!")
        
    if target_ble_device is not None:
        print("")
        print("target device found. Please stand by ...")
        
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
                
                print("---------------------------------------------------------------")
                print(service_handle, ")", bleak_GATT_service)
                
                # https://bleak.readthedocs.io/en/latest/api/index.html#bleak.backends.service.BleakGATTService
                print(bleak_GATT_service.description)
                
                # https://bleak.readthedocs.io/en/latest/api/index.html#bleak.backends.characteristic.BleakGATTCharacteristic
                bleak_GATT_service_characteristics = bleak_GATT_service.characteristics
                for characteristic_idx, bleak_GATT_Characteristic in enumerate(bleak_GATT_service_characteristics):
                    
                    # DEBUG output the characteristic
                    print("    ", characteristic_idx+1, ")", "Handle:", bleak_GATT_Characteristic.handle, "Description: ", bleak_GATT_Characteristic.description, "Object:", bleak_GATT_Characteristic, "servive_uuid:", bleak_GATT_Characteristic.service_uuid, "uuid:", bleak_GATT_Characteristic.uuid, "properties:", bleak_GATT_Characteristic.properties)
                    
                    #if bleak_GATT_Characteristic.handle == 11:
                    #    alert_level_bleak_GATT_Characteristic = bleak_GATT_Characteristic
                    
                    if bleak_GATT_Characteristic.uuid.lower() == "349efa33-ef17-481e-bc4f-4f67b1a90d0d".lower():
                        type_and_version_bleak_GATT_Characteristic = bleak_GATT_Characteristic
                        
                    if bleak_GATT_Characteristic.uuid.lower() == "31E32CA0-F17B-498C-A19D-01D8B33F2257".lower():
                        notify_device_service_GATT_Characteristic = bleak_GATT_Characteristic
                        
            # notify
            if notify_device_service_GATT_Characteristic is not None:
                print("Subscribe to the notification")
                await client.start_notify(notify_device_service_GATT_Characteristic, notification_handler)
                 
            # GCP Type and Version
            if type_and_version_bleak_GATT_Characteristic is not None:
                for x in range(3):                        
                    await client.write_gatt_char(type_and_version_bleak_GATT_Characteristic, b'\x01', response=False)
                    await asyncio.sleep(5)
    
            # Alert level from the "Find Me" demo application
            if alert_level_bleak_GATT_Characteristic is not None:
                print("")
                print("target characteristic (Alert Level) found!")
                
                print("char descriptors ...")
                for char_descriptor_idx, char_descriptor in enumerate(alert_level_bleak_GATT_Characteristic.descriptors):
                    print(char_descriptor_idx, ")", char_descriptor)
                print("char descriptors done.")
                
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