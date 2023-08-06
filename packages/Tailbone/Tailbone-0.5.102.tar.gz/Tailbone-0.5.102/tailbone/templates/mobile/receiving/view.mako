## -*- coding: utf-8; -*-
<%inherit file="/mobile/master/view.mako" />

<%def name="title()">${h.link_to("Receiving", url('mobile.receiving'))} &raquo; ${instance.id_str}</%def>

${form.render()|n}
<br />

${h.text('upc-search', class_='receiving-upc-search', placeholder="Enter UPC", autocomplete='off', **{'data-type': 'search', 'data-url': url('mobile.receiving.lookup', uuid=batch.uuid)})}
<br />

<fieldset data-role="controlgroup" data-type="horizontal">
  ## ${h.radio('receiving-row-filter', value='missing', label="Missing", disabled='disabled')}
  ${h.radio('receiving-row-filter', value='incomplete', label="Incomplete", disabled='disabled')}
  ${h.radio('receiving-row-filter', value='damaged', label="Damaged", disabled='disabled')}
  ${h.radio('receiving-row-filter', value='expired', label="Expired", disabled='disabled')}
  ${h.radio('receiving-row-filter', value='all', label="All", checked=True)}
</fieldset>
<br /><br />

<ul data-role="listview">
   % for obj in grid.iter_rows():
       <li>${grid.listitem.render_readonly()}</li>
   % endfor
</ul>
