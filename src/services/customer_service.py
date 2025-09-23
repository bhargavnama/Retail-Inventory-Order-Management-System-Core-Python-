from src.dao.customer_dao import Customer
from typing import Optional, Dict

class CustomerError(Exception):
    pass

class Customer_service:
    
    def __init__(self):
        self.customer: Customer = Customer()
        
    def add_customer(self, name: str, email: str, phone: str, city: str) -> Optional[Dict]:
        """
        Validate and insert a new customer.
        Raises CustomerError on validation failure.
        """
        
        existing = self.customer.get_customer_by_email(email)
        
        if existing:
            raise CustomerError(f"Already a customer exists with the email: {email}")
        return self.customer.create_customer(name, email, phone, city)
    
    def update_details(self, cust_id: int, fields: Dict) -> Optional[Dict]:
        return self.customer.update_customer(cust_id, fields)
    
    def delete(self, cust_Id: int) -> Optional[Dict]:
        pass