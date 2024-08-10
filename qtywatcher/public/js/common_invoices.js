var customDualQuantities = {};

// Shared function to set up item focus handler and refresh items
function setupItemHandlers(frm, childTable) {
    if (!frm.has_item_focus_handler) {
        frm.has_item_focus_handler = true;
        frm.fields_dict[childTable].grid.wrapper.on("focus", "div.frappe-control.form-group", function(e) {
            toggle_nosquantity_editability(frm, childTable);
        });
    }
    frm.trigger('refresh_items');
}

// Shared function to handle item code changes
function onItemCodeChange(frm, cdt, cdn, childTable) {
    var d = locals[cdt][cdn];
    console.log("Item: " + d.item_code);
    frappe.db.get_value("Item", {"name": d.item_code}, "custom_dual_quantity", function(value) {
        console.log("Item: " + d.item_code + ", dual quantity: " + value.custom_dual_quantity);
        customDualQuantities[d.name] = value.custom_dual_quantity;
        toggle_nosquantity_editability(frm, childTable);
    });
}

// Shared function to toggle editability based on custom dual quantities
function toggle_nosquantity_editability(frm, childTable) {
    $.each(frm.doc[childTable] || [], function(i, d) {
        let grid_row = frm.fields_dict[childTable].grid.grid_rows_by_docname[d.name];
        if (customDualQuantities[d.name] === 0) {
            frappe.model.set_value(d.doctype, d.name, 'custom_nosquantity', d.qty);
            grid_row.toggle_editable('custom_nosquantity', false);
        } else {
            grid_row.toggle_editable('custom_nosquantity', true);
        }
    });
}
