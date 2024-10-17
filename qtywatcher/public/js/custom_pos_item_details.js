function overrideItemDetails() {
    if (
      typeof erpnext !== "undefined" &&
      typeof erpnext.PointOfSale !== "undefined" &&
      typeof erpnext.PointOfSale.ItemDetails !== "undefined"
    ) {
      erpnext.PointOfSale.ItemDetails.prototype.get_form_fields = function (item) {
        const fields = [
          "qty",
          "uom",
          "rate",
          "conversion_factor",
          "discount_percentage",
          "warehouse",
          "actual_qty",
          "price_list_rate",
          "custom_nosquantity"
        ];
        if (item.has_serial_no) fields.push("serial_no");
        if (item.has_batch_no) fields.push("batch_no");
        return fields;
      };
    } else {
      setTimeout(overrideItemDetails, 100);
    }
  }
  
  overrideItemDetails();