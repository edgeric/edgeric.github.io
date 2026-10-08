// News and Updates panel for the home page.
// docs/news.md is included into index.rst inside a `.. container:: news-sidebar-source`
// (hidden in the main content by custom.css). This script rebuilds that list as a
// timeline and puts it in furo's right-hand column in place of the page TOC.
(function () {
    var MONTHS = {
        january: 'Jan', february: 'Feb', march: 'Mar', april: 'Apr', june: 'Jun', july: 'Jul',
        august: 'Aug', sept: 'Sep', september: 'Sep', october: 'Oct', november: 'Nov',
        december: 'Dec'
    };

    // "April 2024" -> "Apr 2024", "Sept 2023" -> "Sep 2023"
    function normalizeDate(text) {
        return text.trim().replace(/[A-Za-z]+/, function (m) {
            return MONTHS[m.toLowerCase()] || m;
        });
    }

    // One news.md item, "**Mar 2026** - text", becomes a date label and the text
    // (keeping any links or emphasis in the text).
    function buildEntry(li) {
        var body = (li.querySelector('p') || li).cloneNode(true);
        var strong = body.querySelector('strong');
        var date = '';
        if (strong) {
            date = normalizeDate(strong.textContent);
            strong.parentNode.removeChild(strong);
        }
        var walker = document.createTreeWalker(body, NodeFilter.SHOW_TEXT);
        var first = walker.nextNode();
        while (first && !first.nodeValue.trim()) {
            first = walker.nextNode();
        }
        if (first) {
            first.nodeValue = first.nodeValue.replace(/^\s*[-–—:]\s*/, '');
        }

        var entry = document.createElement('li');
        entry.className = 'news-entry';
        if (date) {
            var when = document.createElement('span');
            when.className = 'news-when';
            when.textContent = date;
            entry.appendChild(when);
        }
        var what = document.createElement('div');
        what.className = 'news-what';
        what.innerHTML = body.innerHTML.trim();
        entry.appendChild(what);
        return entry;
    }

    function buildPanel(source) {
        var panel = document.createElement('section');
        panel.className = 'news-panel';
        panel.setAttribute('aria-label', 'News and updates');

        var title = document.createElement('div');
        title.className = 'news-panel-title';
        title.textContent = 'News & Updates';
        panel.appendChild(title);

        var list = document.createElement('ol');
        list.className = 'news-timeline';
        source.querySelectorAll('li').forEach(function (li) {
            list.appendChild(buildEntry(li));
        });
        panel.appendChild(list);
        return panel;
    }

    function replaceWithNews() {
        var tocSticky = document.querySelector('.toc-sticky');
        var source = document.querySelector('.news-sidebar-source');
        if (!tocSticky || !source) {
            return false;
        }
        if (!tocSticky.querySelector('.news-panel')) {
            tocSticky.innerHTML = '';
            tocSticky.appendChild(buildPanel(source));
        }
        return true;
    }

    if (!replaceWithNews()) {
        document.addEventListener('DOMContentLoaded', replaceWithNews);
        window.addEventListener('load', replaceWithNews);
    }
})();
