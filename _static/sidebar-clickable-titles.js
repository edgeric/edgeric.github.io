/**
 * Make sidebar section titles clickable: link to index#anchor and hide child page links.
 */
document.addEventListener('DOMContentLoaded', function () {
  var pathname = window.location.pathname.replace(/^\//, '');
  var isIndex = !pathname || pathname === 'index.html' || pathname.endsWith('/index.html');
  var indexHref = isIndex ? '#' : (pathname.indexOf('/') >= 0
    ? pathname.split('/').slice(0, -1).map(function () { return '..'; }).join('/') + '/index.html#'
    : 'index.html#');

  var captionToAnchor = {
    'Our Team': 'our-team',
    'Demos': 'our-demos',
    'Our Projects': 'our-projects',
    'EdgeRIC Events': 'edgeric-events',
    '5G Testbed': '5g-testbed',
    'EdgeRIC Architecture': 'edgeric-architecture',
    'EdgeRIC Tutorials': 'edgeric-tutorials',
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

  function hideNextUl(captionEl) {
    var next = captionEl.nextElementSibling;
    if (next && next.tagName === 'UL') next.style.display = 'none';
  }

  var captions = document.querySelectorAll('.sidebar-tree .caption, .sidebar-tree p.caption');
  captions.forEach(function (p) {
    var text = (p.textContent || '').trim();
    var anchor = captionToAnchor[text];
    if (anchor) {
      makeCaptionLink(p, anchor);
      hideNextUl(p);
    }
  });
});
