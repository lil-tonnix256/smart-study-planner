students = {
    "VU001": {
        "name": "tonny",
        "total_fees": 800000,
        "amount_paid": 0,
        "outstanding_balance": 800000,
        "payments": []
    },

    "VU002": {
        "name": "keith",
        "total_fees": 800000,
        "amount_paid": 300000,
        "outstanding_balance": 500000,
        "payments": [
            {
                "payment_code": "PAY-0001",
                "amount": 300000
            }
        ]
    }
}


# Payment code counter
payment_counter = 2


def generate_payment_code():
    global payment_counter

    payment_code = f"PAY-{payment_counter:04d}"
    payment_counter += 1

    return payment_code


def record_payment(students):
    """Record a full or partial payment for a student."""

    print("\n--- Record Fee Payment ---")

    reg_no = input("Enter student registration number: ").strip()

    if reg_no not in students:
        print("Student not found.")
        return

    student = students[reg_no]

    total_fees = student["total_fees"]
    amount_paid = student["amount_paid"]
    outstanding = total_fees - amount_paid

    print(f"\nStudent Name: {student['name']}")
    print(f"Registration Number: {reg_no}")
    print(f"Total Fees: UGX {total_fees:,.0f}")
    print(f"Amount Already Paid: UGX {amount_paid:,.0f}")
    print(f"Outstanding Balance: UGX {outstanding:,.0f}")

    if outstanding <= 0:
        print("This student's fees are already fully paid.")
        return

    while True:
        try:
            payment = float(input("Enter payment amount: "))

            if payment <= 0:
                print("Payment must be greater than zero.")

            elif payment > outstanding:
                print(
                    f"Payment cannot exceed the outstanding balance "
                    f"of UGX {outstanding:,.0f}."
                )

            else:
                break

        except ValueError:
            print("Invalid amount. Please enter a number.")

    # Generate payment code
    payment_code = generate_payment_code()

    # Update amount paid
    student["amount_paid"] += payment

    # Calculate new outstanding balance
    student["outstanding_balance"] = (
        student["total_fees"] - student["amount_paid"]
    )

    # Store payment details
    student["payments"].append({
        "payment_code": payment_code,
        "amount": payment
    })

    print("\nPayment recorded successfully!")
    print(f"Payment Code: {payment_code}")
    print(f"Payment Made: UGX {payment:,.0f}")
    print(f"Total Amount Paid: UGX {student['amount_paid']:,.0f}")
    print(
        f"Outstanding Balance: "
        f"UGX {student['outstanding_balance']:,.0f}"
    )


# Run the payment function
record_payment(students)