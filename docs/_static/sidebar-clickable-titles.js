/**
 * Make sidebar section titles "Our Team" and "Demos" clickable:
 * link directly to index#our-team / index#our-demos, and hide the child page links
 * so no redirect pages are used.
 */
document.addEventListener('DOMContentLoaded', function () {
  var pathname = window.location.pathname.replace(/^\//, '');
  var isIndex = !pathname || pathname === 'index.html' || pathname.endsWith('/index.html');
  var indexHref = isIndex ? '#' : (pathname.indexOf('/') >= 0
    ? pathname.split('/').slice(0, -1).map(function () { return '..'; }).join('/') + '/index.html#'
    : 'index.html#');

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
    if (text === 'Our Team') {
      makeCaptionLink(p, 'our-team');
      hideNextUl(p);
    } else if (text === 'Demos') {
      makeCaptionLink(p, 'our-demos');
      hideNextUl(p);
    }
  });
});
