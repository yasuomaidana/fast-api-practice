from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class ProductType(Enum):
    MEAT = "carnes"
    DAIRY = "lácteos"
    FRUIT = "frutas"
    VEGETABLE = "verduras"
    FISH = "pescados"
    BAKERY = "panadería"
    ALCOHOL = "alcohol"
    BEVERAGE = "bebidas"
    GROCERY = "abarrotes"
    CLEANING = "limpieza"
    PERSONAL_CARE = "cuidado personal"
    MEDICINE = "medicamentos"
    CLOTHING = "ropa"
    ELECTRONICS = "electrónicos"
    TOYS = "juguetes"
    BOOKS = "libros"
    STATIONERY = "papelería"
    HARDWARE = "ferretería"
    TOOLS = "herramientas"
    AUTOMOTIVE = "automotriz"
    PET = "mascotas"
    CEREALS = "cereales"
    SNACKS = "botanas"
    SWEETS = "dulces"
    DESSERTS = "postres"
    HEALTH = "salud"
    FITNESS = "fitness"
    SPORTS = "deportes"
    TRANSPORT = "transporte"
    TRAVEL = "viajes"
    ENTERTAINMENT = "entretenimiento"
    EDUCATION = "educación"
    HOBBIES = "pasatiempos"
    ART = "arte"
    CRAFTS = "manualidades"
    GARDENING = "jardinería"
    FURNITURE = "muebles"
    DECORATION = "decoración"
    STUDENT_LOAN = "crédito estudiantil"
    MORTGAGE = "hipoteca"
    CAR_LOAN = "crédito automotriz"
    PERSONAL_LOAN = "crédito personal"
    BUSINESS_LOAN = "crédito empresarial"
    INSURANCE = "seguro"
    INVESTMENT = "inversión"
    SAVINGS = "ahorro"
    ELECTRICITY = "electricidad"
    WATER = "agua"
    GAS = "gas"
    INTERNET = "internet"
    PHONE = "teléfono"
    TV = "televisión"
    STREAMING = "streaming"
    GAMING = "videojuegos"
    MUSIC = "música"
    MOVIES = "películas"
    SERIES = "series"
    FOOD = "comida"
    RENT = "renta"
    SOFTWARE = "software"
    SUBSCRIPTION = "suscripción"


class ProductName(SQLModel, table=True):
    __tablename__ = "product_name"
    id: Optional[int] = Field(primary_key=True)
    name: str


class Product(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    productNameId: int = Field(foreign_key="product_name.id")
    productType: ProductType
    price: float
    

class PurchasedItem(SQLModel, table=True):
    __tablename__ = "purchased_item"
    id: Optional[int] = Field(primary_key=True)
    productId: int = Field(foreign_key="product.id")
    quantity: int
    invoiceId: Optional[int] = Field(default=None, foreign_key="invoice.id")
    
    product: Product = Relationship(back_populates="purchased_items")