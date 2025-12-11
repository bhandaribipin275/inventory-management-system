# inventory management software
A simple inventory management system built with Django.
Users can add stock item and generate bills. All data is stored in database and are rendered in real time

To run project, run the following commands in the project's directory to create the database. When running the software for the first time, it is necessary to run each command for each app in the project
```
python manage.py makemigrations homepage
python manage.py migrate homepage
python manage.py makemigrations inventory
python manage.py migrate inventory
python manage.py makemigrations transactions
python manage.py migrate transactions
```
After the first time, the following can be run to migrate model changes in any app
```
python manage.py makemigrations
python manage.py migrate
```
Use the following command to run the server
```
python manage.py runserver
```
Use the following command to create an admin user 
```
python manage.py createsuperuser
```

## Stock History Feature (Stock In / Stock Out)

Overview
- The Stock History feature adds a complete audit trail for inventory movements. Every purchase, sale, manual stock change, and reversed transaction is logged as a timestamped record with quantity, direction (IN / OUT), and an optional note.

Key benefits
- Unified inventory model: `Stock` is the single source of truth for item quantities across inventory, purchases and sales.
- Auditability: `StockHistory` keeps chronological IN/OUT records for compliance and reconciliation.
- UI + API: Inventory dashboard and transactions pages now surface stock history for quick review.

What changed
- Added `StockHistory` model (linked to `Stock`) to record stock in/out events.
- Integrated logging into transactions flows: purchases (IN), sales (OUT), and bill deletions (reversal entries).
- Updated inventory list and history templates to show the latest activity.
- Added tests covering stock history creation, ordering, and view integration.

Database / Migrations
- New migration created: `inventory/migrations/0002_stockhistory.py` — run migrations before using the feature.

Verification & usage
1. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```
2. Start server:
```bash
python manage.py runserver 0.0.0.0:8001
```
3. Visit the Inventory page to view items and the recent stock history preview.
4. Use the Purchases and Sales flows (Transactions) — creating a purchase will log a Stock IN record; creating a sale will log a Stock OUT record.
5. You can also manually record stock in/out from the Inventory list via the "Record stock in/out" action.

Testing
- Unit and integration tests are included. Run them with:
```bash
python manage.py test
```

Developer notes
- The feature preserves backward compatibility with the existing `Stock` model used by transactions.
- When reversing/deleting bills the code adjusts `Stock.quantity` and writes opposing `StockHistory` records for clear auditability.

Troubleshooting
- If a page shows no history, ensure migrations were applied and you have created at least one `Stock` and a related transaction (purchase or sale) which will generate history entries.
- The dev server defaults to port `8001` in this environment if `8000` is in use.

Next steps / improvements
- Add filters and pagination to the history view (by item, date range, type).
- Add CSV export for stock history and visual dashboards for trends.

Contact
- For questions about implementation or to review edge cases, contact the repository maintainer.
