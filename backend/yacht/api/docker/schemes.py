
from ... import ma

class TemplateSchema(ma.SQLAlchemySchema):
    id = ma.Int(dump_only=True)
    name = ma.Str()
    url = ma.Url()
