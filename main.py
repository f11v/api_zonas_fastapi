from fastapi import FastAPI, HTTPException
from schemas import Zona
from data import zonas
from fastapi import Query
from zeep import Client

app = FastAPI(title="API Zonas Agrícolas", version="1.0")

@app.post("/zonas", response_model=Zona)
def crear_zona(zona: Zona):
    for z in zonas:
        if z.id == zona.id:
            raise HTTPException(status_code=400, detail="ID ya existe")
    zonas.append(zona)
    return zona

@app.get("/zonas", response_model=list[Zona])
def listar_zonas():
    return zonas

@app.get("/zonas/{id}", response_model=Zona)
def obtener_zona(id: int):
    for zona in zonas:
        if zona.id == id:
            return zona
    raise HTTPException(status_code=404, detail="Zona no encontrada")

@app.delete("/zonas/{id}")
def eliminar_zona(id: int):
    for i, zona in enumerate(zonas):
        if zona.id == id:
            zonas.pop(i)
            return {"mensaje": "Zona eliminada"}
    raise HTTPException(status_code=404, detail="Zona no encontrada")


WSDL_URL = "https://www.w3schools.com/xml/tempconvert.asmx?WSDL"
soap_client = Client(wsdl=WSDL_URL)

@app.get("/temperatura/convertir")
def convertir_celsius_a_fahrenheit(valor: float = Query(..., description="Valor en grados Celsius")):
    try:
        resultado = soap_client.service.CelsiusToFahrenheit(str(valor))
        return {
            "celsius": valor,
            "fahrenheit": float(resultado)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al convertir temperatura: {str(e)}")