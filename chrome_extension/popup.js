// When the button is clicked, inject setPageBackgroundColor into current page
changeColor.addEventListener("click", async () => {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: setPageBackgroundColor,
    });
  });
  
  // The body of this function will be executed as a content script inside the
  // current page
  function setPageBackgroundColor() {
    chrome.storage.sync.get("color", ({ color }) => {
      x = document.getElementsByClassName("yt-simple-endpoint style-scope ytd-grid-video-renderer")
      links = []
      for (let element of x) {
        links.push(element.href)
      }
      fetch('http://localhost:8080', {
        headers: {'content-length': 100},
        method: 'POST',
        body: JSON.stringify(links)
      }).then(r => r.text()).then(result => {
        console.log(typeof result[0])
        sentiments = (result.substring(1, result.length - 1)).split(",")
        var nums = []
        for (let i = 0; i < sentiments.length; i++) {
          nums.push(parseFloat(sentiments[i], 10))
        }
        console.log(nums)
      })
      // for (let element of x) {
      //     element.style.backgroundColor = color
      // }
      // var spawn = import("child_process");
      // // const { spawn } = require('child_process');
      // const childProcess = spawn('python', ['hello.py'])
      // childProcess.stdout.on('data', (data) => {
      //     console.log(`stdout: ${data}`)
      // });
    //   document.body.style.backgroundColor = color;
    });
  }
  
