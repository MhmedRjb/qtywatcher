frappe.ui.form.on('Stock Reconciliation', {
    onload_post_render: function(frm) {
        setupItemHandlers(frm, 'items');
    }
});

frappe.ui.form.on("Stock Reconciliation Item", "item_code", function(frm, cdt, cdn) {
    onItemCodeChange(frm, cdt, cdn, 'Stock Reconciliation Item');
});
