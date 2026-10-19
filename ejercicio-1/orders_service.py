from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(title="Orders Service")

INVENTORY_URL = "http://localhost:5001/inventory"

@app.post("/orders")
async def create_order(product_id: str, quantity: int):
    # 1. Comunicación Síncrona: Consultar stock a InventoryService
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{INVENTORY_URL}/{product_id}", timeout=5.0)
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Producto no existe en inventario")
            
            inventory_data = response.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Inventory Service no disponible (Falla de red/caído)")

    # 2. Evaluar la respuesta obtenida
    if not inventory_data["available"] or inventory_data["stock"] < quantity:
        return {
            "status": "REJECTED",
            "message": "No hay suficiente stock para confirmar el pedido."
        }

    # 3. Confirmar pedido (lógica simulada)
    return {
        "status": "CONFIRMED",
        "product": inventory_data["name"],
        "quantity": quantity,
        "message": "Pedido procesado y confirmado exitosamente."
    }