$(document).ready(function() {
    $('#login').click(function() {
        // for ebay login
        var user = $('#ebayUser').val();
        var pass = $('#ebayPassword').val();
        chrome.tabs.executeScript(null, {
            code: 'document.querySelector("#userid").value="' + user + '";' +
                'document.querySelector("#pass").value="' + pass + '";' +
                'document.querySelector("#sgnBt").click();'
        });
        window.close();
    });
});
