
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


class TemplateContentSchema(ma.SQLAlchemySchema):
    id = ma.Int(dump_only=True)
    title = ma.Str()
    name = ma.Str()
    notes = ma.Str()
    description = ma.Str()
    logo = ma.Str()
    image = ma.Str()
    categories = ma.Str()
    platform = ma.Str()
    restart_policy = ma.Str()
    sysctls = ma.Str()
    ports = ma.Str()
    volumes = ma.Str()
    env = ma.Str()
    template_id = ma.Str()