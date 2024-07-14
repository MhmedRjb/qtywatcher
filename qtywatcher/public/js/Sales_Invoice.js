var customDualQuantities = {};
/*
script to keeps the custom_nosquantity field in sync with the qty field.
When an item doesn't have multiple quantities, custom_nosquantity matches qty 
to keep everything consistent
*/
// TODO: add a custom field to the child table to store the dual quantity to simplify the script

frappe.ui.form.on('Sales Invoice', {
    onload_post_render: function(frm) {
        if (!frm.has_item_focus_handler) {
            frm.has_item_focus_handler = true;
            frm.fields_dict.items.grid.wrapper.on("focus", "div.frappe-control.form-group", function(e) {
                toggle_nosquantity_editability(frm);
            });
        }
    frm.trigger('refresh_items');
    },
    refresh: function(frm) {
        frm.trigger('refresh_items');
    },
    refresh_items: function(frm) {
        toggle_nosquantity_editability(frm);
    },
    items_add: function(frm) {
        toggle_nosquantity_editability(frm);
    },
    items_remove: function(frm) {
        toggle_nosquantity_editability(frm);
    }
});

frappe.ui.form.on("Sales Invoice Item", "item_code", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    console.log("Item: " + d.item_code);
    frappe.db.get_value("Item", {"name": d.item_code}, "custom_dual_quantity", function(value) {
        console.log("Item: " + d.item_code + ", dual quantity: " + value.custom_dual_quantity);
        customDualQuantities[d.name] = value.custom_dual_quantity;
        toggle_nosquantity_editability(frm);
    });
});

function toggle_nosquantity_editability(frm) {
    $.each(frm.doc.items, function(i, d) {
        let grid_row = frm.fields_dict['items'].grid.grid_rows_by_docname[d.name];
        if (customDualQuantities[d.name] === 0) {
            frappe.model.set_value(d.doctype, d.name, 'custom_nosquantity', d.qty);
            grid_row.toggle_editable('custom_nosquantity', false);
        } else {
            d.custom_nosquantity = customDualQuantities[d.name];
            grid_row.toggle_editable('custom_nosquantity', true);
        }
    });
}
