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
