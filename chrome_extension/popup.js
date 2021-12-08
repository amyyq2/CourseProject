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
    var positive = 98
    var negative = 360
    var neutral = 190
    var videos = document.getElementsByClassName("yt-simple-endpoint style-scope ytd-grid-video-renderer")
    var batch_size = 5
    let batch_num = 0
    links = []
    for (let video of videos) {
      links.push(video.href)
      if (links.length == batch_size) {
        fetch('http://localhost:8080', {
        headers: {'content-length': 100},
        method: 'POST',
        body: JSON.stringify(links)
      }).then(r => r.text()).then(result => {
        sentiment_text = (result.substring(1, result.length - 1)).split(",")
        var sentiment_nums = []
        for (let i = 0; i < sentiment_text.length; i++) {
          sentiment_nums.push(parseFloat(sentiment_text[i], 10))
        }
        console.log(sentiment_nums)

        for (let i = 0; i < sentiment_nums.length; i++) {
          // The more postive the sentiment, the darker the green
          // The more negative the sentiment, the darker the red
          if (sentiment_nums[i] >= 0.05 && sentiment_nums[i] < 0.4) {
            l = 0.7
          } else if (sentiment_nums[i] >= 0.4 && sentiment_nums[i] < 0.65) {
            l = 0.5
          } else if (sentiment_nums[i] >= 0.65) {
            l = 0.3
          } else if (sentiment_nums[i] < 0.05 && sentiment_nums[i] > -0.05) {
            l = 0.5
          } else if (sentiment_nums[i] < -0.05 && sentiment_nums[i] > -0.055) {
            l = 0.5
          } else if (sentiment_nums[i] <= 0.055) {
            l = 0.7
          }

          var video_color = 0
          var h = 0
          if (sentiment_nums[i] > 0.05) {
            h = positive
          } else if (sentiment_nums[i] < -0.05) {
            h = negative
          } else {
            h = neutral
          }
          var s = 100

          const a = s * Math.min(l, 1 - l) / 100;
          const f = n => {
            const k = (n + h / 30) % 12;
            const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1);
            return Math.round(255 * color).toString(16).padStart(2, '0');   // convert to Hex and prefix "0" if needed
          };
          video_color = `#${f(0)}${f(8)}${f(4)}`;

          videos[i+(batch_num*batch_size)].style.backgroundColor = video_color
        }
        batch_num++
      })
      links = []
      }
    }
  });
}
