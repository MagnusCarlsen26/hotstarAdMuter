// ==UserScript==
// @name         Webpage Screenshot and API Check
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Takes a screenshot of the webpage, sends it to an API, and calls a function if API returns "YES"
// @author       You
// @match        *://*/*
// @grant        GM_xmlhttpRequest
// @connect      localhost
// @connect      127.0.0.1
// @require      https://html2canvas.hertzen.com/dist/html2canvas.min.js
// ==/UserScript==

(function() {
    'use strict';

    window.addEventListener('load', function() {
        setTimeout(captureScreenshotAndProcess, 1000); // Wait an additional second for images to render
    });

    function captureScreenshotAndProcess() {
        console.log("Capturing screenshot and processing")
        html2canvas(document.documentElement).then(canvas => {

            // Convert canvas to data URL (base64 image)
            const screenshotData = canvas.toDataURL('image/png');

            // Send screenshot to API
            sendScreenshotToAPI(screenshotData);
            console.log("Screenshot captured and sent to API")
        }).catch(error => {
            console.error('Error capturing screenshot:', error);
        });
    }

    // Function to send screenshot to API
    function sendScreenshotToAPI(screenshotData) {

        const apiEndpoint = 'http://localhost:5000/upload';

        GM_xmlhttpRequest({
            method: 'POST',
            url: apiEndpoint,
            headers: {
                'Content-Type': 'application/json'
            },
            data: JSON.stringify({
                imageData: screenshotData
            }),
            onload: function(response) {
                processAPIResponse(response);
            },
            onerror: function(error) {
                console.error('Error sending screenshot to API:', error);
            }
        });
    }

    function processAPIResponse(response) {
        try {
            const data = JSON.parse(response.responseText);

            if (data.result === 'YES') customFunction();
        } catch (error) {
            console.error('Error processing API response:', error);
        }
    }

    function customFunction() {
        console.log('API returned YES! Custom function called.');
    }
})();