# Pebble App Portion

## Pair your computer with your Pebble Time
* Enable BlueTooth is on your Pebble Time
* Ensure your Pebble Time is not paired with another device. You may need to disable BlueTooth on your phone.
* Enable BlueTooth on your computer
* Follow the steps to pair your computer with your Pebble Time. Actual steps will depend on you operating system
* Find the device file for your Pebble Time on your computer. On OS X, this is similar to `/dev/cu.PebbleTimeXXXX-SerialPo` or `/dev/cu.PebbleXXXX-SerialPortSe`

## Build application
```
pebble build
```

## Install application
```
pebble install --serial <PEBBLE_TIME_DEVICE_FILE>
```
