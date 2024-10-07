# SETUP RASPBERRY-PI

Install an preferred OS

## Install Display Drivers
```
sudo rm -rf LCD-show 
git clone  https://github.com/goodtft/LCD-show.git  
cd LCD-show/
chmod +x LCD5-show
sudo ./LCD5-show 90
```

## Clone the Repository
```
git clone --filter=blob:none --no-checkout https://github.com/Buddhi19/EE356-SmartCalculator.git SmartCalculator
cd SmartCalculator
git sparse-checkout set --cone
git checkout main
git sparse-checkout set RaspberryPi
```

## Install Dependencies
```
sudo apt install python3-matplotlib
sudo apt install python3-numpy
sudo apt install python3-sympy
sudo apt install python3-scipy
```
### Install Open-CV
1. Expand File System
```
sudo raspi-config
```
- Navigate to Advanced Options and press enter
- Navigate to A1 Expand Filesystem and press enter

2. Install Image I/O Packages
```
sudo apt-get install libpng-dev
```
3. Install the GTK Development Library
```
sudo apt-get install libgtk2.0-dev
```
4. Additional Dependencies for OpenCV Optimization
```
sudo apt-get install libatlas-base-dev gfortran
```
5. Install Open-CV
```
apt list python*opencv*
sudo apt install python3-opencv
```
6. Verify
```
apt show python3-opencv
```

## Display Command
```
export DISPLAY=:0
```