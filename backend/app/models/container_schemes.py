
from .. import ma
from marshmallow.validate import (
    Length
)

class TemplateSchema(ma.SQLAlchemySchema):
    # perhapse use auto_field
    id = ma.Int(
        dump_only=True)
    created_at = ma.DateTime(
        dump_only=True)
    updated_at = ma.DateTime(
        dump_only=True)
    title = ma.Str(
        required=True,
        validate=Length(min=1, max=255))
    url = ma.Url(
        required=True)