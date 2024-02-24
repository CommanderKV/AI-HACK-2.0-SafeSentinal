
// Define sets for good and bad websites
const goodWebsites = new Set([
    'example.com',
    'stackoverflow.com',
    'google.com'
]);

const badWebsites = new Set([
    'malicious.com'
]);
const siteWebsite=new Set([
    'commanderkv.github.io/AI-HACK-2.0-SafeSentinal/'
])

// Function to check if a URL contains part of a website's URL
function checkContainsWebsite(url, websitesSet) {
    for (const website of websitesSet) {
        if (url.includes(website)) {
            return true;
        }
    }
    return false;
}

// Get all anchor elements on the page
const allLinks = document.querySelectorAll('a');

// Iterate through each link and apply color based on good or bad website
allLinks.forEach(link => {
    if(checkContainsWebsite(link.href, siteWebsite)){
        //link.style.color = 'white';
        /*link.addEventListener('mouseover', () => {
            // Change the button's background color
            link.style.backgroundColor = 'blue';
        });*/
    }
    else if (checkContainsWebsite(link.href, goodWebsites)) {
        link.style.color = 'green';
    } else if (checkContainsWebsite(link.href, badWebsites)) {
        link.style.color = 'red';
    } else{
        link.style.color = 'khaki';
    }
});

// Function to handle link click event
function handleLinkClick(event) {
    const link = event.target;
    let confirmed = false;

    if (checkContainsWebsite(link.href, goodWebsites)) {
        confirmed=true;
    }
    else if (checkContainsWebsite(link.href, badWebsites)) {
        confirmed = window.confirm('This website is potentially malicious. We DO NOT recoment you visiting this website: ' + link.href );
    }else if(checkContainsWebsite(link.href, siteWebsite)){
        confirmed=true;
    }
    else{
        confirmed = window.confirm('This website is not in our list. Are you sure you want to visit ' + link.href + '?');
    }

    if (!confirmed) {
        event.preventDefault(); // Prevent the default action (following the link)
    }
}

// Attach event listener to each link
allLinks.forEach(link => {
    link.addEventListener('click', handleLinkClick);
});
