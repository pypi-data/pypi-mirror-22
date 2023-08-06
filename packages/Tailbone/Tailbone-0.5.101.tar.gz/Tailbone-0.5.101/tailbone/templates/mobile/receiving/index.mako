## -*- coding: utf-8; -*-
<%inherit file="/mobile/master/index.mako" />

<%def name="title()">Receiving</%def>

% if request.has_perm('receiving.create'):
    ${h.link_to("New Receiving Batch", url('mobile.receiving.create'), class_='ui-btn ui-corner-all')}
% endif

<fieldset data-role="controlgroup" data-type="horizontal">
  ${h.radio('receiving-filter', value='pending', label="Pending", checked=True)}
  ${h.radio('receiving-filter', value='complete', label="Complete", disabled='disabled')}
  ${h.radio('receiving-filter', value='executed', label="Executed", disabled='disabled')}
  ${h.radio('receiving-filter', value='all', label="All", disabled='disabled')}
</fieldset>
<br /><br />

${parent.body()}
