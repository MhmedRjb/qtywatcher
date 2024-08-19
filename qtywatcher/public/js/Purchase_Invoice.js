frappe.ui.form.on('Purchase Invoice', {
    onload_post_render: function(frm) {
        setupItemHandlers(frm, 'items');
    }
});

frappe.ui.form.on("Purchase Invoice Item", "item_code", function(frm, cdt, cdn) {
    onItemCodeChange(frm, cdt, cdn, 'items');
});
