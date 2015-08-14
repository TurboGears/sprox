<%
attr_keys = list(w.attrs.keys())
if 'id' in attr_keys:
    attr_keys.remove('id')
if 'class' in attr_keys:
    attr_keys.remove('class')
%>

<%namespace name="tw" module="tw2.core.mako_util"/>\
<div ${tw.attrs(attrs=w.attrs)}>
    <a href="#" class="subdocuments-add" onclick="return (function(btn) { var el=btn.parentNode.lastChild; while(el.nodeType !== 1) { el = el.previousSibling; } el.style.display = 'block'; return false; })(this)">Add</a>
    % for c in w.children:
        % if not loop.last:
        <a href="#" class="subdocuments-delete" onclick="return (function(btn) { var el=btn.nextSibling; while(el.nodeType !== 1) { el = el.nextSibling; } if (el) { el.remove(); btn.remove(); } return false; })(this)"></a>
        % endif
        ${c.display() | n}
        % if w.separator and not loop.last:
          ${w.separator |n}
        %endif
    % endfor
</div>
