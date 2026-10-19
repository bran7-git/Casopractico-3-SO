from fastapi import FastAPI, HTTPException

app = FastAPI(title="Inventory Service")

# Base de datos simulada en memoria
fake_inventory = {
    "prod_123": {"name": "Notebook Gamer", "stock": 5},
    "prod_456": {"name": "Mouse Inalámbrico", "stock": 0}
}

@app.get("/inventory/{product_id}")
def check_stock(product_id: str):
    if product_id not in fake_inventory:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    product = fake_inventory[product_id]
    return {
        "product_id": product_id,
        "name": product["name"],
        "available": product["stock"] > 0,
        "stock": product["stock"]
    }