# simple-selenium-sgx-crawler
By: Kong Sheng How

#### Prerequisite:
1.	Google Chrome Version 83.0.4103.97
2.	[Chrome Driver 83.0.4103.39](https://chromedriver.chromium.org/) (select compatible version)
3.	Python Selenium Package (“pip install selenium”)

#### Project Objective:
1.	Python program to download data from https://www2.sgx.com/research-education/derivatives with command line options

#### Project Detail:
This project will use web crawler (selenium) to crawl for the respective files/data needed with Google Chrome. Include the python script and chromedriver.exe in the same folder as the python script will specify the location of chromedriver.exe.

#### Command Line Options:
User can define runtime behavior, what data and how many data to download through command line options. 
The command line options provided are:

| Option | Description |
| ------ | ----------- |
| `-wt / --waittime [float]` | Time for selenium web driver to wait for missing element(s) implicitly (Default: 5 seconds) |
| `--type-of-data [string]` | Type of data to retrieve (Default: all), Options: {Tick, TickData_structure, TC, TC_structure, All} |
| `--number-of-dates [int]` | Number of dates to retrieve (Default: -1, for all available dates), Options: {-1, 1, 2, 3, 4} |
| `--headless-mode` | Headless mode (Run in background without opening the browser) |

** `--headless-mode` is not recommended as the browser in that mode will download only 1 file if the the files to be downloaded are of the same name. (e.g. TC_structure.dat or Tick_structure.dat)

##### Example of commands:

`python SGX.py -wt 10 --type-of-data tick --number-of-dates 2`

`python SGX.py -wt 7 --number-of-dates 1 --headless`


#### To run this project in an Linux Cloud Instances

1. Create a Linux Instance, update the system, Install Pip for Python3 and Unzip
```
sudo apt update
sudo apt install python3-pip
sudo apt install unzip
```

2. Install Required Python Modules
```
pip3 install selenium
pip3 install crontab
```

3. Download Google Chrome and ChromeDriver for Linux
```
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt-get update 
sudo apt-get install google-chrome-stable

wget https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver

sudo mv -f chromedriver /usr/local/share/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver
```
