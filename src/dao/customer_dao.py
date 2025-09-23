from src.config import get_supabase
from typing import Optional, Dict

class Customer:
    def __init__(self):
        self._sb = get_supabase()
        
    def create_customer(self, name: str, email: str, phone: str, city: str) -> Optional[Dict]:
        """
            Inserts the details of the customer and returns the inserted customer details by unique email
        """
        payload = { "name": name, "email": email, "phone": phone}
        
        if city is not None:
            payload["city"] = city
            
        self._sb.table("customers").insert(payload).execute()
        
        resp = self._sb.table("customers").select("*").eq("email", email).limit(1).execute()
        
        return resp.data[0] if resp.data else None
    
    def get_customer_by_id(self, cust_id: int) -> Optional[Dict]:
        """
            Returns customer details which mathces the id
        """
        resp = self._sb.table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
        return resp.data[0] if resp.data else None
    
    def get_customer_by_email(self, email: str) -> Optional[Dict]:
        """
            Returns customer details which mathches the email
        """
        resp = self._sb.table("customers").select("*").eq("email", email).execute()
        return resp.data[0] if resp.data else None
        
    def update_customer(self,cust_id: int, fields: Dict):
        """
            Updates the customer details and returns the updated details
        """
        self._sb.table("customers").update(fields).eq("cust_id", cust_id).execute()
        resp = self._sb.table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
        return resp.data[0] if resp.data else None
    
    def delete_customer(self, cust_id: int) -> Optional[Dict]:
        """
            Deletes the customer and then returns the deleted customer
        """
        before_resp = self._sb.table("customers").select("*").eq("cust_id", cust_id).execute()
        self._sb.table("customers").delete().eq("cust_id", cust_id).execute()
        return before_resp.data[0] if before_resp else None
    
    def list_customers(self,limit = 100, city: str | None = None):
        q = self._sb.table("customers").select("*").order("cust_id", desc=False).limit(limit)
        
        if city is not None:
            q.eq("city", city)
        
        resp = q.execute()

        return resp.data[0] if resp.data else None
        