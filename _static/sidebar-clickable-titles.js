/**
 * Make sidebar section titles clickable: link to index#anchor.
 * Child items (sub-titles) remain visible.
 */
document.addEventListener('DOMContentLoaded', function () {
  var pathname = window.location.pathname.replace(/^\//, '');
  var isIndex = !pathname || pathname === 'index.html' || pathname.endsWith('/index.html');
  var indexHref = isIndex ? '#' : (pathname.indexOf('/') >= 0
    ? pathname.split('/').slice(0, -1).map(function () { return '..'; }).join('/') + '/index.html#'
    : 'index.html#');

  var captionToAnchor = {
    'Our Projects': 'our-projects',
    'Team': 'our-team',
    'Demos': 'our-demos',
    'EdgeRIC Events': 'edgeric-events',
    'Open Source Repositories': 'open-source-repositories',
    '5G Testbed': '5g-testbed',
    'EdgeRIC Architecture': 'edgeric-architecture',
    'Publications & Tutorials': 'edgeric-tutorials',
    'Datasets': 'datasets'
  };

  function makeCaptionLink(captionEl, anchor) {
    if (!captionEl || !anchor) return;
    var text = captionEl.textContent.trim();
    var a = document.createElement('a');
    a.href = indexHref + anchor;
    a.className = 'reference internal';
    a.textContent = text;
    captionEl.textContent = '';
    captionEl.appendChild(a);
  }

  var captions = document.querySelectorAll('.sidebar-tree .caption, .sidebar-tree p.caption');
  captions.forEach(function (p) {
    var text = (p.textContent || '').trim();
    var anchor = captionToAnchor[text];
    if (anchor) {
      makeCaptionLink(p, anchor);
    }
  });
});
