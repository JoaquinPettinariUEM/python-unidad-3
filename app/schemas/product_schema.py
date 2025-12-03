
class ProductBase:
  name: str
  brand: str

class Product(ProductBase):
    id: int

    model_config = { "from_attributes": True }
