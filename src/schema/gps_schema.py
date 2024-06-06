from marshmallow import Schema, fields
from domain.gps import Gps

class GpsSchema(Schema):
    longitude = fields.Float(required=True)
    latitude = fields.Float(required=True)