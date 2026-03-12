/**
 * Set sidebar single combined logo img src to _static/logos/all_logos.png relative to current page.
 */
document.addEventListener('DOMContentLoaded', function () {
  var img = document.querySelector('.sidebar-school-logo-single[data-src]');
  if (!img) return;

  var pathname = window.location.pathname.replace(/^\//, '');
  var segments = pathname.split('/').filter(Boolean);
  var depth = segments.length > 1 ? segments.length - 1 : 0;
  var base = depth ? Array(depth + 1).join('../') : '';
  var logosBase = base + '_static/logos/';

  var name = img.getAttribute('data-src') || 'all_logos.png';
  img.setAttribute('src', logosBase + name);
});