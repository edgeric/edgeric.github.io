/**
 * Add expand/collapse button to each sidebar caption (大标题).
 * Clicking the button toggles the section under the caption.
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

  function makeButton(isExpanded) {
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'sidebar-toggle';
    btn.setAttribute('aria-label', isExpanded ? 'Collapse' : 'Expand');
    btn.innerHTML = isExpanded ? '\u25BC' : '\u25B6'; // ▼ / ▶
    return btn;
  }

  function setButtonState(btn, expanded) {
    btn.innerHTML = expanded ? '\u25BC' : '\u25B6';
    btn.setAttribute('aria-label', expanded ? 'Collapse' : 'Expand');
  }

  /* Case 1: Caption (p.caption or .caption) followed by ul */
  var captions = tree.querySelectorAll('.caption, p.caption');
  captions.forEach(function (cap) {
    var next = cap.nextElementSibling;
    if (!next || next.tagName !== 'UL') return;

    var id = (cap.textContent || '').trim().replace(/\s+/g, '-') || 'section';
    var isExpanded = collapsed[id] === undefined ? false : !collapsed[id];

    var btn = makeButton(isExpanded);
    cap.classList.add('sidebar-caption-with-toggle');
    cap.appendChild(btn);

    if (!isExpanded) next.classList.add('sidebar-collapsed');

    btn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      isExpanded = next.classList.toggle('sidebar-collapsed');
      isExpanded = !next.classList.contains('sidebar-collapsed');
      setButtonState(btn, isExpanded);
      collapsed[id] = !isExpanded;
      save();
    });
  });

  /* Case 2: First-level li that has a direct child ul (nested list) */
  var topLevel = tree.querySelector(':scope > ul');
  if (topLevel) {
    [].forEach.call(topLevel.children, function (li) {
      var childUl = li.querySelector(':scope > ul');
      if (!childUl) return;

      var link = li.querySelector(':scope > .reference, :scope > a.reference');
      var id = (link && link.textContent) ? link.textContent.trim().replace(/\s+/g, '-') : 'item-' + Math.random().toString(36).slice(2);
      var isExpanded = collapsed[id] === undefined ? false : !collapsed[id];

      var btn = makeButton(isExpanded);
      if (!isExpanded) childUl.classList.add('sidebar-collapsed');
      li.classList.add('sidebar-li-with-toggle');
      if (link) link.parentNode.insertBefore(btn, link);
      else li.insertBefore(btn, childUl);

      btn.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        childUl.classList.toggle('sidebar-collapsed');
        isExpanded = !childUl.classList.contains('sidebar-collapsed');
        setButtonState(btn, isExpanded);
        collapsed[id] = !isExpanded;
        save();
      });
    });
  }
});
