# Setup
1. Download python from [python.org](https://www.python.org/downloads/)
2. Now install relevant libraries, with the command `py -m pip install selenium numpy pandas jinja2 openpyxl`, paste them in command prompt (Press search and type CMD)
3. Next, find out the version of google chrome you've installed by clicking on `3 dots` on top right of chrome, then `help`, then `About Google Chrome`. You should see something like `Version 96.0.4664.110 (Official Build) (x86_64)`
4. Now download chromedriver from [chromedriver.chromium.org](https://chromedriver.chromium.org/) of the same version as Chrome you found in step 3. 
5. Now download this repo by clicking on `code` then `Download Zip`. Post downloading, unzip the folder and place the chromedriver in the same unzipped folder
6. Setup is all done, now you've to set your username and password inside the code, open `scraper.py` using any text editor (notepad), and go to line 18 and 19, and set your username and password. 
7. Also you've to setup the location of file where you'll store the scraped data, set that on line 21. Lastly, set location of log file, which is generated for debugging/checking code, on line 22


FAQ: 

1. Program crashes after starting
    1. Check if chrome has updated, you will have to update chromedriver as well
    2. Check if file paths are correctly set
2. Some of the outputs are blank in the generated CSV
    1. Make sure you've good internet connection

Please generate an issue if you still have issues (click on issue tab on the top). Make sure you paste output from scraper.log for debugging. 