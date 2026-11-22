"""                          "PBL Lab Project"
Problem 15: Restaurant Order Manager
B.Tech CSE (AI & ML with IBM) IILM Univeristy 
Aurthor : Ayyan Khan, Aryan Sharma, Mehul Rathor
Description: A console-based restaurant billing system that displays a categorized menu,
takes orders with quantities, validates inputs against errors, calculates
bifurcated GST (5%) and optional tips, saves bills to a file, and includes
a built-in test runner for the 5 required lab test scenarios.
"""

import datetime
import sys

#CONFIGURATION & MENU DATA
TAX_RATE = 0.05  # 5% Total GST 2.5% CGST + 2.5% SGST
LOG_FILE = "orders_log.txt"

MENU = {
    101: {"name": "Spring Rolls",         "cat": "Starters", "price": 120.0},
    102: {"name": "Paneer Tikka",         "cat": "Starters", "price": 200.0},
    201: {"name": "Dal Makhani",          "cat": "Mains",    "price": 240.0},
    202: {"name": "Paneer Butter Masala", "cat": "Mains",    "price": 270.0},
    203: {"name": "Butter Naan",          "cat": "Breads",   "price": 45.0},
    301: {"name": "Gulab Jamun (2 pcs)",  "cat": "Desserts", "price": 80.0},
    401: {"name": "Cold Coffee",          "cat": "Drinks",   "price": 90.0},
}


# INPUT VALIDATION HELPERS 
def get_int(prompt: str, min_v: int = 0, max_v: int | None = None) -> int:
    """Safely prompts for an integer with bounds checking and error recovery."""
    while True:
        try:
            val = int(input(prompt).strip())
            if val < min_v or (max_v is not None and val > max_v):
                print(f"  [!] Please enter a value between {min_v} and {max_v if max_v else 'above'}.")
                continue
            return val
        except ValueError:
            print("  [!] Invalid input. Please enter a valid whole number.")


def get_float(prompt: str, min_v: float = 0.0) -> float:
    """Safely prompts for a non-negative decimal number."""
    while True:
        try:
            val = float(input(prompt).strip())
            if val < min_v:
                print(f"  [!] Amount cannot be negative. Minimum is {min_v:.2f}.")
                continue
            return val
        except ValueError:
            print("  [!] Invalid amount. Please enter a valid number.")


#RESTAURANT OPERATIONS
def display_menu():
    """Prints the restaurant menu structured by food category."""
    print("\n" + "=" * 55)
    print("              THE BISTRO - DINING MENU")
    print("=" * 55)
    last_cat = None
    for code, item in MENU.items():
        if item["cat"] != last_cat:
            last_cat = item["cat"]
            print(f"\n[{last_cat}]")
            print(f"{'Code':<6} {'Item Name':<28} {'Price (Rs)':>14}")
            print("-" * 55)
        print(f"{code:<6} {item['name']:<28} {item['price']:>14.2f}")
    print("=" * 55)


def take_order() -> tuple[dict[int, int], str]:
    """Takes item codes and quantities into a cart. Returns (cart, table_name)."""
    table = input("\nEnter Table No. / Takeaway (e.g., Table 4 or T): ").strip() or "Table 1"
    cart = {}  
    print(f"Placing order for [{table}]. Enter item codes (or 0 to finish):")

    while True:
        code = get_int("  Enter Item Code (0 to finish): ", min_v=0)
        if code == 0:
            if not cart:
                if input("  Cart is empty. Exit ordering? (y/n): ").lower().startswith('y'):
                    return {}, table
                continue
            break
        if code not in MENU:
            print(f"  [!] Item code '{code}' not on menu. Check the menu codes.")
            continue
        
        qty = get_int(f"  Enter quantity for {MENU[code]['name']}: ", min_v=1)
        cart[code] = cart.get(code, 0) + qty
        print(f"  [+] Added: {cart[code]} x {MENU[code]['name']}")

    return cart, table


def calculate_bill(cart: dict[int, int], tip: float) -> dict:
    """Calculates subtotal, 5% GST (CGST + SGST), tip, and grand total."""
    subtotal = sum(MENU[code]["price"] * qty for code, qty in cart.items())
    cgst = round(subtotal * (TAX_RATE / 2), 2)
    sgst = round(subtotal * (TAX_RATE / 2), 2)
    total_tax = round(cgst + sgst, 2)
    grand_total = round(subtotal + total_tax + tip, 2)
    return {"subtotal": subtotal, "cgst": cgst, "sgst": sgst, "tax": total_tax, "tip": tip, "total": grand_total}


def generate_receipt(cart: dict[int, int], bill: dict, table: str) -> str:
    """Formats a clean receipt string for terminal display and file storage."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "=" * 55,
        "                 THE BISTRO RESTAURANT",
        "             TAX INVOICE & DINING RECEIPT",
        "=" * 55,
        f" Date/Time: {now} | Service: {table}",
        "-" * 55,
        f" {'Item Name':<24} {'Qty':<5} {'Price':>8} {'Total':>12}",
        "-" * 55,
    ]
    for code, qty in cart.items():
        name = MENU[code]["name"]
        price = MENU[code]["price"]
        lines.append(f" {name:<24} {qty:<5} {price:>8.2f} {price * qty:>12.2f}")

    lines.extend([
        "-" * 55,
        f" {'Subtotal:':<38} Rs. {bill['subtotal']:>10.2f}",
        f" {'CGST (2.5%):':<38} Rs. {bill['cgst']:>10.2f}",
        f" {'SGST (2.5%):':<38} Rs. {bill['sgst']:>10.2f}",
        f" {'Tip / Gratuity:':<38} Rs. {bill['tip']:>10.2f}",
        "=" * 55,
        f" {'GRAND TOTAL:':<38} Rs. {bill['total']:>10.2f}",
        "=" * 55,
        "       Thank you for dining with us! Visit again.",
        "=" * 55,
    ])
    return "\n".join(lines)


#FILE STORAGE
def save_bill_to_file(receipt: str):
    """Appends the formatted bill receipt to the persistent log file."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(receipt + "\n\n")
    print(f"  [✔] Receipt saved to '{LOG_FILE}'.")


def view_order_history():
    """Reads and displays saved receipts from the log file."""
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            print("\n" + f.read())
    except FileNotFoundError:
        print(f"\n  [!] No previous orders found in '{LOG_FILE}'.")



def run_lab_tests():
    """Runs 5 diverse test inputs including edge cases and prints the outputs."""
    print("\n" + "#" * 60)
    print("   EXECUTING 5 LAB EVALUATION TEST CASES")
    print("#" * 60)

    test_scenarios = [
        ("TC-01: Standard Multi-Item Order with Tip", {101: 2, 201: 1, 203: 3}, 30.0, "Table 5"),
        ("TC-02: Single Item Takeaway with Zero Tip",  {202: 1}, 0.0, "Takeaway"),
        ("TC-03: Multiple Drinks and Desserts",        {301: 2, 401: 2}, 20.0, "Table 2"),
        ("TC-04: High Quantity Order with Custom Tip", {102: 4, 203: 8}, 55.50, "Table 10"),
        ("TC-05: Minimal Order (Single Naan)",         {203: 1}, 5.0, "Table 7"),
    ]

    for title, cart, tip, table in test_scenarios:
        print(f"\n>>> Running: {title}")
        bill = calculate_bill(cart, tip)
        receipt = generate_receipt(cart, bill, table)
        print(receipt)
        save_bill_to_file(receipt)

    print("\n[✔] All 5 lab test scenarios executed and saved successfully!")


#6. MAIN MENU
def main():
    while True:
        print("\n" + "=" * 45)
        print("      RESTAURANT ORDER MANAGER")
        print("=" * 45)
        print("  1. Place New Order & Generate Bill")
        print("  2. View Menu")
        print("  3. View Saved Bills Log")
        print("  4. Run 5 Built-in Lab Test Cases")
        print("  5. Exit")
        print("=" * 45)

        choice = get_int("Select option (1-5): ", min_v=1, max_v=5)

        if choice == 1:
            display_menu()
            cart, table = take_order()
            if not cart:
                print("  Order cancelled.")
                continue
            tip = get_float("\nEnter tip amount in Rs. (0 for none): ", min_v=0.0)
            bill = calculate_bill(cart, tip)
            receipt = generate_receipt(cart, bill, table)
            print("\n" + receipt)
            save_bill_to_file(receipt)
        elif choice == 2:
            display_menu()
        elif choice == 3:
            view_order_history()
        elif choice == 4:
            run_lab_tests()
        elif choice == 5:
            print("\nExiting. Thank you!")
            break


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_lab_tests()
    else:
        main()
