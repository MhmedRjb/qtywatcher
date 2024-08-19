frappe.ui.form.on('Stock Entry', {
    onload_post_render: function(frm) {
        setupItemHandlers(frm, 'items');
    },
});

frappe.ui.form.on("Stock Entry Detail", "item_code", function(frm, cdt, cdn) {
    onItemCodeChange(frm, cdt, cdn, 'Stock Entry Detail');
});
