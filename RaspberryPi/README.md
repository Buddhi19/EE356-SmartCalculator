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
git clone --filter=blob:none --no-checkout https://github.com/Buddhi19/EE356-SmartCalculator.git
cd RaspberryPi
git sparse-checkout set --cone
git checkout main
git sparse-checkout set RaspberryPi
```