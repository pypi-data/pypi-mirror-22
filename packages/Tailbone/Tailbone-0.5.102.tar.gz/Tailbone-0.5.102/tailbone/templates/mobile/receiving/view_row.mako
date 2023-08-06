## -*- coding: utf-8; -*-
<%inherit file="/mobile/master/view_row.mako" />

## TODO: this is broken for actual page (header) title
<%def name="title()">${h.link_to("Receiving", url('mobile.receiving'))} &raquo; ${h.link_to(instance.batch.id_str, url('mobile.receiving.view', uuid=instance.batch_uuid))} &raquo; ${row.upc.pretty()}</%def>

<% unit_uom = 'LB' if row.product.weighed else 'EA' %>

<div class="ui-grid-a">
  <div class="ui-block-a">
    <h3>${instance.brand_name}</h3>
    <h3>${instance.description} ${instance.size}</h3>
    <h3>${h.pretty_quantity(row.case_quantity)} ${unit_uom} per CS</h3>
  </div>
  <div class="ui-block-b">
    ${h.image(product_image_url, "product image")}
  </div>
</div>

<table>
  <tbody>
    <tr>
      <td>ordered</td>
      <td>${h.pretty_quantity(row.cases_ordered or 0)} / ${h.pretty_quantity(row.units_ordered or 0)}</td>
    </tr>
    <tr>
      <td>received</td>
      <td>${h.pretty_quantity(row.cases_received or 0)} / ${h.pretty_quantity(row.units_received or 0)}</td>
    </tr>
    <tr>
      <td>damaged</td>
      <td>${h.pretty_quantity(row.cases_damaged or 0)} / ${h.pretty_quantity(row.units_damaged or 0)}</td>
    </tr>
    <tr>
      <td>expired</td>
      <td>${h.pretty_quantity(row.cases_expired or 0)} / ${h.pretty_quantity(row.units_expired or 0)}</td>
    </tr>
  </tbody>
</table>

<table id="receiving-quantity-keypad-thingy" data-changed="false">
  <tbody>
    <tr>
      <td>${h.link_to("7", '#', class_='keypad-button ui-btn ui-btn-inline ui-corner-all')}</td>
      <td>${h.link_to("8", '#', class_='keypad-button ui-btn ui-btn-inline ui-corner-all')}</td>
      <td>${h.link_to("9", '#', class_='keypad-button ui-btn ui-btn-inline ui-corner-all')}</td>
    </tr>
    <tr>
      <td>${h.link_to("4", '#', class_='keypad-button ui-btn ui-btn-inline ui-corner-all')}</td>
      <td>${h.link_to("5", '#', class_='keypad-button ui-btn ui-btn-inline ui-corner-all')}</td>
      <td>${h.link_to("6", '#', class_='keypad-button ui-btn ui-btn-inline ui-corner-all')}</td>
    </tr>
    <tr>
      <td>${h.link_to("1", '#', class_='keypad-button ui-btn ui-btn-inline ui-corner-all')}</td>
      <td>${h.link_to("2", '#', class_='keypad-button ui-btn ui-btn-inline ui-corner-all')}</td>
      <td>${h.link_to("3", '#', class_='keypad-button ui-btn ui-btn-inline ui-corner-all')}</td>
    </tr>
    <tr>
      <td>${h.link_to("0", '#', class_='keypad-button ui-btn ui-btn-inline ui-corner-all')}</td>
      <td>${h.link_to(".", '#', class_='keypad-button ui-btn ui-btn-inline ui-corner-all')}</td>
      <td>${h.link_to("Del", '#', class_='keypad-button ui-btn ui-btn-inline ui-corner-all')}</td>
    </tr>
  </tbody>
</table>

${h.form(request.current_route_url(), class_='receiving-update')}
${h.csrf_token(request)}
${h.hidden('row', value=row.uuid)}
${h.hidden('cases')}
${h.hidden('units')}

<%
   uom = 'CS'
   if row.units_ordered and not row.cases_ordered:
       uom = 'EA'
%>
<fieldset data-role="controlgroup" data-type="horizontal">
  <button type="button" class="ui-btn-active receiving-quantity">1</button>
  <button type="button" disabled="disabled">&nbsp;</button>
  ${h.radio('receiving-uom', value='CS', checked=uom == 'CS', label="CS")}
  ${h.radio('receiving-uom', value=unit_uom, checked=uom == unit_uom, label=unit_uom)}
</fieldset>

<table>
  <tbody>
    <tr>
      <td>
        <fieldset data-role="controlgroup" data-type="horizontal">
          ${h.radio('mode', value='received', label="received", checked=True)}
          ${h.radio('mode', value='damaged', label="damaged")}
          ${h.radio('mode', value='expired', label="expired")}
        </fieldset>
      </td>
    </tr>
    <tr>
      <td>
        <fieldset data-role="controlgroup" data-type="horizontal" class="receiving-actions">
          <button type="button" data-action="add" class="ui-btn-inline ui-corner-all">Add</button>
          <button type="button" data-action="subtract" class="ui-btn-inline ui-corner-all">Subtract</button>
          <button type="button" data-action="clear" class="ui-btn-inline ui-corner-all ui-state-disabled">Clear</button>
        </fieldset>
      </td>
    </tr>
  </tbody>
</table>

${h.end_form()}
