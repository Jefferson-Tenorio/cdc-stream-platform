from fabric.customer_pii_fabric import create_customer_pii

if __name__ == "__main__":
    customer = create_customer_pii()  # chama sua função
    print("\nCustomerPII Object:")
    print(customer.email_blind_index.hex())