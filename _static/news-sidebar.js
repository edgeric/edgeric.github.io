// Replace TOC with News and Updates content loaded from a reusable HTML fragment
// The fragment is rendered from docs/news.md and included into index.rst inside
// a container:: news-sidebar-source (then hidden via CSS in the main content).
function replaceWithNews() {
    var tocSticky = document.querySelector('.toc-sticky');
    if (!tocSticky) return false;

    var source = document.querySelector('.news-sidebar-source');
    if (!source) return false;

    tocSticky.innerHTML =
        '<div class=\"toc-title-container\">' +
            '<span class=\"toc-title\">News and Updates</span>' +
        '</div>' +
        source.innerHTML;

    return true;
}

// Try immediately
if (!replaceWithNews()) {
    document.addEventListener('DOMContentLoaded', function() {
        if (!replaceWithNews()) {
            setTimeout(replaceWithNews, 100);
            setTimeout(replaceWithNews, 500);
        }
    });
}

window.addEventListener('load', replaceWithNews);
