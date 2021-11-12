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
      
      for (let element of x) {
          element.style.backgroundColor = color
      }
    //   document.body.style.backgroundColor = color;
    });
  }
  