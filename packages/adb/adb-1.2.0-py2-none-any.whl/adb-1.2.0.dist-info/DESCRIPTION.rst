This repository contains a pure-python implementation of the Android
ADB and Fastboot protocols, using libusb1 for USB communications.

This is a complete replacement and rearchitecture of the Android
project's ADB and fastboot code available at
https://github.com/android/platform_system_core/tree/master/adb

This code is mainly targeted to users that need to communicate with
Android devices in an automated fashion, such as in automated
testing. It does not have a daemon between the client and the device,
and therefore does not support multiple simultaneous commands to the
same device. It does support any number of devices and never
communicates with a device that it wasn't intended to, unlike the
Android project's ADB.


