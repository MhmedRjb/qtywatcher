# Secondary QTY Tracking for Inventory Management / Multi Uom IN erpnext
This system addresses the need to track quantities of items, especially in industries where products like cheese lose weight over time. The primary purpose is to maintain accurate inventory records and prevent discrepancies or potential theft.

# feature

1. a secondary quantity to accurately monitor stock levels, crucial for industries where products like cheese vary in weight over time.
2. (dual uom check) in item page to allow secondary quantity  for specific items
4. Comprehensive Reporting
   1. stocke ledger qty show all movements of the secondary quantity 
   2. stock balance qty (secondary quantity)

# how to install 

```
bench get-app  https://github.com/MhmedRjb/qtywatcher.git
```

```
bench --site <site_name> install-app  qtywatcher
```
# where is it working
### 1. stock:
   1. Stock Entry
   2. Stock Reconciliation
### 2. selling:
   1. Sales Invoice
   2. Sales Order
### 3. buying
   1. Purchase Order
   2. Purchase Invoice

  
## License
This project is licensed under the MIT License.


