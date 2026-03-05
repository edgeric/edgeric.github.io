// Replace TOC with News and Updates - works with both localhost and file://
function replaceWithNews() {
    var tocSticky = document.querySelector('.toc-sticky');
    if (tocSticky) {
        tocSticky.innerHTML = 
            '<div class="toc-title-container">' +
                '<span class="toc-title">News and Updates</span>' +
            '</div>' +
            '<div class="news-updates-sidebar">' +
                '<ul class="news-list">' +
                    '<li class="news-item">' +
                        '<span class="news-date">Mar 2026</span>' +
                        '<p>Stay tuned for upcoming events!</p>' +
                    '</li>' +
                    '<li class="news-item">' +
                        '<span class="news-date">Feb 2026</span>' +
                        '<p>Check out our latest updates!</p>' +
                    '</li>' +
                '</ul>' +
            '</div>';
        return true;
    }
    return false;
}

// Try immediately
if (!replaceWithNews()) {
    // Try on DOMContentLoaded
    document.addEventListener('DOMContentLoaded', function() {
        if (!replaceWithNews()) {
            // Fallback: try after a short delay (for file:// protocol)
            setTimeout(replaceWithNews, 100);
            setTimeout(replaceWithNews, 500);
        }
    });
}

// Also try on window load as final fallback
window.addEventListener('load', replaceWithNews);
