/**
 * Collapsible sidebar sections: a chevron on each caption opens or closes the list under it.
 * The section that holds the current page starts open; open/closed choices last for the session.
 * (Pages with sub-pages keep furo's own expander.)
 */
document.addEventListener('DOMContentLoaded', function () {
  var tree = document.querySelector('.sidebar-tree');
  if (!tree) return;

  var storageKey = 'sidebar-collapsed';
  var collapsed = {};
  try {
    var saved = sessionStorage.getItem(storageKey);
    if (saved) collapsed = JSON.parse(saved);
  } catch (e) {}

  function save() {
    try {
      sessionStorage.setItem(storageKey, JSON.stringify(collapsed));
    } catch (e) {}
  }

  var CHEVRON = '<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true">' +
    '<path d="M6 3.5 10.5 8 6 12.5" fill="none" stroke="currentColor" stroke-width="1.75" ' +
    'stroke-linecap="round" stroke-linejoin="round"/></svg>';

  tree.querySelectorAll('.caption').forEach(function (cap) {
    var list = cap.nextElementSibling;
    if (!list || list.tagName !== 'UL') return;

    var label = (cap.textContent || '').trim();
    var id = label.replace(/\s+/g, '-') || 'section';
    var open = collapsed[id] === undefined ? list.classList.contains('current') : !collapsed[id];

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'sidebar-section-toggle';
    btn.innerHTML = CHEVRON;

    function render() {
      list.classList.toggle('sidebar-collapsed', !open);
      btn.setAttribute('aria-expanded', String(open));
      btn.setAttribute('aria-label', (open ? 'Collapse ' : 'Expand ') + label);
    }

    btn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      open = !open;
      collapsed[id] = !open;
      save();
      render();
    });

    cap.classList.add('sidebar-caption-with-toggle');
    cap.appendChild(btn);
    render();
  });
});
