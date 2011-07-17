from elixir import *

metadata.bind = 'sqlite:///data.sqlite'

class Deal(Entity):
    url = Field(String(512))
    title = Field(Unicode(256))
    price = Field(Float(2))
    orig_price = Field(Float(2))
    image = Field(String(512))
    start_time = Field(DateTime)
    end_time = Field(DateTime)
    bought = Field(Integer)
    shops = OneToMany('Shop')
    type = Field(Integer)
    city = Field(String(50))
    site = Field(String(16))

class Shop(Entity):
    name = Field(Unicode(50))
    address = Field(Unicode(100))
    tel = Field(Unicode(30))
    latitude = Field(Float)
    longitude = Field(Float)
    deal = ManyToOne('Deal')

