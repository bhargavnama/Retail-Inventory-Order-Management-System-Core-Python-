from src.config import get_supabase
from typing import Optional, Dict
from src.services.product_service import Product_service

class Order:
    
    def __init__(self):
        self._sb = get_supabase()
        
    def create_order(self, cust_id: int, order_items: list[str], total_amount: float) -> Optional[Dict]:
        """
            Creates and returns an order
        """
        payload = { "cust_id": cust_id, "status": "PLACED", "total_amount": total_amount }
        resp = self._sb.table("orders").insert(payload).execute()
        
        if resp.data:
            for item in order_items:
                self._sb.table("order_items").insert({
                    "order_id": resp.data[0]["order_id"],
                    "prod_id": item["prod_id"],
                    "quantity": item["quantity"],
                    "price": item["price"]
                })
            return resp.data[0]
        else:
            return None
        
    def fetch(self, order_id: int) -> Optional[Dict]:
        """
            Fetch the details of the order and the order items and the customer details
        """
        resp = self._sb.table("order").select("*, customer(*), order_items(*, products(*))").eq("order_id", order_id).execute()
        return resp.data if resp.data[0] else None
    
    
    def list_orders(self, cust_id: int) -> Optional[Dict]:
        """
            Returns all the orders ordered by a customer
        """
        resp = self._sb.table("orders").select("*, customers(*)").eq("cust_id", cust_id).execute()
        
        return resp.data if resp.data[0] else None
    
    def cancel_order(self, order_id: int) -> Optional[Dict]:
        """
            Cancels an order
        """
        items = self._sb.table("order_items").select("*").eq("order_id", order_id).execute().data
        product_service = Product_service()
        
        for item in items:
            product_service.restock_product(item["prod_id"], -1 * item["quantity"])
            
        resp = self._sb.table("orders").update({"status": "CANCELLED"}).execute()
        
        return resp.data if resp.data[0] else None