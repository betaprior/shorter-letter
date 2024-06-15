document.addEventListener('DOMContentLoaded', function() {
    const redirectButton = document.getElementById('redirectButton')
    if (redirectButton) {
        redirectButton.addEventListener('click', function() {
            chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
                const activeTab = tabs[0]
                const currentUrl = activeTab.url
                const apiUrl = `https://albumentations.ai?url=${encodeURIComponent(currentUrl)}`
                chrome.tabs.update(activeTab.id, { url: apiUrl })
            })
        })
    }
})
