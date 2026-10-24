#!/usr/bin/env python3
"""
Chamunda Automobile - Royal Enfield Genuine Spare Parts Filter & Search CLI.
Allows comprehensive searching across 4,400+ authentic Royal Enfield spare parts
by part number, model, category, price range, cost, stock status, bin, and HSN code.

Usage examples:
    python3 search_parts_cli.py --query "brake pads" --model "Hunter 350"
    python3 search_parts_cli.py --part-no "574050"
    python3 search_parts_cli.py --category "Periodic Service & Maintenance" --max-price 500
    python3 search_parts_cli.py --model "Himalayan 450" --sort price_asc
    python3 search_parts_cli.py --status low_stock
    python3 search_parts_cli.py --query "oil filter" --analytics
"""

import sys
import json
import argparse
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).parent))
from inventory_engine import ChamundaInventoryManager


def main():
    parser = argparse.ArgumentParser(
        description="Chamunda Automobile • Royal Enfield Genuine Spare Parts Multi-Filter Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-q", "--query", type=str, default="", help="General keyword or phrase search")
    parser.add_argument("-p", "--part-no", "--sku", type=str, default="", help="OEM Part Number or SKU")
    parser.add_argument("-m", "--model", type=str, default="", help="Motorcycle model (e.g. 'Hunter 350', 'Classic 350', 'Himalayan 450')")
    parser.add_argument("-c", "--category", type=str, default="", help="Part category (e.g. 'Braking', 'Engine', 'Periodic Service')")
    parser.add_argument("--min-price", type=float, default=None, help="Minimum MRP in INR")
    parser.add_argument("--max-price", type=float, default=None, help="Maximum MRP in INR")
    parser.add_argument("--min-cost", type=float, default=None, help="Minimum wholesale cost in INR")
    parser.add_argument("--max-cost", type=float, default=None, help="Maximum wholesale cost in INR")
    parser.add_argument("--status", type=str, choices=["all", "in_stock", "low_stock", "out_of_stock"], default="all", help="Stock status filter")
    parser.add_argument("--min-stock", type=int, default=None, help="Minimum stock count")
    parser.add_argument("--max-stock", type=int, default=None, help="Maximum stock count")
    parser.add_argument("--bin", type=str, default="", help="Warehouse bin location (e.g. 'Rack A')")
    parser.add_argument("--hsn", type=str, default="", help="GST HSN Code (e.g. '84212300')")
    parser.add_argument("--unit", type=str, default="", help="Unit of measure (e.g. 'Piece', 'Set')")
    parser.add_argument("--sort", type=str, default="name", choices=["name", "price_asc", "price_desc", "cost_asc", "cost_desc", "stock", "stock_asc", "part_number"], help="Sort order")
    parser.add_argument("-l", "--limit", type=int, default=20, help="Maximum results to display (default: 20)")
    parser.add_argument("--offset", type=int, default=0, help="Pagination offset")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--analytics", action="store_true", help="Show inventory valuation & category breakdown")

    args = parser.parse_args()
    mgr = ChamundaInventoryManager()

    results = mgr.filter_parts(
        query=args.query,
        part_number=args.part_no,
        model=args.model,
        category=args.category,
        min_price=args.min_price,
        max_price=args.max_price,
        min_cost=args.min_cost,
        max_cost=args.max_cost,
        stock_status=args.status,
        min_stock=args.min_stock,
        max_stock=args.max_stock,
        bin_location=args.bin,
        hsn_code=args.hsn,
        unit=args.unit,
        sort_by=args.sort,
        limit=args.limit,
        offset=args.offset,
    )

    if args.json:
        out = {
            "filters": vars(args),
            "count": len(results),
            "items": results
        }
        if args.analytics:
            out["analytics"] = mgr.get_filter_analytics(results)
        print(json.dumps(out, indent=2))
        return

    print("=" * 110)
    print("👑 CHAMUNDA AUTOMOBILE • ROYAL ENFIELD GENUINE PARTS MULTI-FILTER SEARCH")
    print("=" * 110)

    # Filter criteria banner
    active_filters = []
    if args.query: active_filters.append(f"Keyword: '{args.query}'")
    if args.part_no: active_filters.append(f"Part No: '{args.part_no}'")
    if args.model: active_filters.append(f"Model: '{args.model}'")
    if args.category: active_filters.append(f"Category: '{args.category}'")
    if args.min_price is not None or args.max_price is not None:
        active_filters.append(f"Price: ₹{args.min_price or 0} - ₹{args.max_price or 'Max'}")
    if args.status != "all": active_filters.append(f"Status: '{args.status}'")
    if args.bin: active_filters.append(f"Bin: '{args.bin}'")
    if args.sort != "name": active_filters.append(f"Sort: '{args.sort}'")

    if active_filters:
        print("🎯 Active Filters: " + " | ".join(active_filters))
    else:
        print("🎯 Active Filters: Showing All Catalog Parts")

    print(f"📊 Results Found: {len(results)} item(s) (Displaying up to {args.limit})")
    print("-" * 110)

    if not results:
        print("❌ No Royal Enfield genuine parts found matching the specified criteria.")
        print("=" * 110)
        return

    # Table header
    header = f"{'OEM Part No':<16} | {'Part Name':<38} | {'Category':<22} | {'MRP (₹)':<8} | {'Cost (₹)':<8} | {'Stock':<6} | {'Bin':<9}"
    print(header)
    print("-" * 110)

    for p in results:
        pn = p.get('part_number', p.get('oem_number', 'N/A'))[:16]
        name = p.get('name', 'Unknown')[:38]
        cat = p.get('category', 'Spares')[:22]
        mrp = f"₹{p.get('mrp', 0):,}"
        cost = f"₹{p.get('cost_price', 0):,}"
        stock = str(p.get('stock', 0))
        bin_loc = p.get('bin_location', 'A-01')[:9]
        print(f"{pn:<16} | {name:<38} | {cat:<22} | {mrp:<8} | {cost:<8} | {stock:<6} | {bin_loc:<9}")

    print("=" * 110)

    if args.analytics:
        analytics = mgr.get_filter_analytics(results)
        print("📈 INVENTORY ANALYTICS FOR MATCHING RESULTS:")
        print(f"  • Total Units in Stock: {analytics['total_units']:,}")
        print(f"  • Total Retail Value (MRP): ₹{analytics['mrp_valuation_inr']:,}")
        print(f"  • Total Wholesale Cost Value: ₹{analytics['cost_valuation_inr']:,}")
        print(f"  • Expected Gross Margin: ₹{analytics['gross_margin_inr']:,}")
        print("  • Category Distribution:")
        for cat_name, cnt in sorted(analytics['categories'].items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"    - {cat_name}: {cnt} parts")
        print("=" * 110)


if __name__ == "__main__":
    main()
