## -*- coding: utf-8; -*-
<%inherit file="/mobile/base.mako" />

<%def name="title()">Receiving</%def>

${h.link_to("New Receiving Batch", url('purchases.batch.mobile_create'), class_='ui-btn')}

${h.link_to("View Receiving Batches", url('mobile.purchases.batch'), class_='ui-btn')}
