# CourseProject: Chrome Extension that analyzes the sentiment of comments on a page of Youtube videos

## Getting Started

Install ChromeDriver:
- Download here: https://chromedriver.chromium.org/getting-started
- Follow this tutorial: https://www.swtestacademy.com/install-chrome-driver-on-mac/

### Dependencies (Run these commands in terminal in the repo after you clone it)
Install selenium:
- ```pip install selenium```

Install pandas:
- ```pip install pandas```

Install vaderSentiment:
- ```pip install vaderSentiment```

Install nltk:
- ```pip install nltk```

## To execute the code
### Initial Steps
1) Clone this repository in a location you will remember. 
2) Open up a Chrome browser

### Add the Rice extension to Chrome
1) Click on the extensions button in the top right corner. 
   - <img width="412" alt="Screen Shot 2021-12-08 at 1 18 06 PM" src="https://user-images.githubusercontent.com/55038545/145270225-e9d9fe54-6344-46ad-9d14-cf9bbf024d15.png">
2) Click on "Manage Extensions". This should open another tab.
3) You should toggle the "Developer Mode" in the top right corner of the page. 
   - <img width="209" alt="Screen Shot 2021-12-08 at 1 23 44 PM" src="https://user-images.githubusercontent.com/55038545/145271034-02eca780-4ea1-4c8c-9add-06ee29823ecd.png">      
4) Click "Load unpacked".
   - <img width="495" alt="Screen Shot 2021-12-08 at 1 23 34 PM" src="https://user-images.githubusercontent.com/55038545/145271216-8b4e94ea-f4fa-43f1-8f05-f5b41b298588.png">
5) Navigate to the repository that you cloned and then click into the folder called "chrome_extension". Click the blue select button
6) Now you should see this in your extensions
   - <img width="418" alt="Screen Shot 2021-12-08 at 1 28 00 PM" src="https://user-images.githubusercontent.com/55038545/145271596-5a68ee55-42a1-4f83-a209-ad74782523d0.png">
7) You need to now click on the extensions button again in the top right corner and pin Rice to your browser bar.
   - <img width="320" alt="Screen Shot 2021-12-08 at 1 28 42 PM" src="https://user-images.githubusercontent.com/55038545/145271711-75ea32a0-7bf4-4528-9a30-5546cd22c8be.png">

### Try the extension out!
1) Open up a Chrome browser to any youtube channel. Navigate to the videos tab of the channel. Your url should look something like "youtube.com/c/username/videos"
2) Open the terminal and navigate to the repository you cloned. You should be in /path/to/CourseProject
3) Run the server by running this line of code in the terminal
   ```python3 comments_scraping.py```
4) Once you see the message "Server started http://localhost:8080", go to your chrome tab with the youtube channel videos
5) Click on the Rice extension icon in the top right corner. You should see a square with a button in the middle.
   - <img width="97" alt="Screen Shot 2021-12-08 at 1 35 22 PM" src="https://user-images.githubusercontent.com/55038545/145272541-37f4ee23-0029-450f-9e87-f2c836f9e1df.png">
6) Click the center button and wait for your results! Give it at least 1.5 minutes to ensure it works. 



NOTE: User of extension must restart server code every time the channel is refreshed or navigated to a new channel. They can do this by:
1) ^C
2) ```python3 comments_scraping.py```
