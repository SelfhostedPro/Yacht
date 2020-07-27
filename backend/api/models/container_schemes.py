from .. import ma
from .containers import (
    Template,
    TemplateItem
)
from marshmallow.validate import (
    Length
)
from webargs import fields, validate

class TemplateItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TemplateItem

    template_id=ma.Int()

class TemplateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Template

    items = ma.Nested(
        TemplateItemSchema, many=True,
            exclude=(
                'template_id',
                'restart_policy',
                'sysctls',
                'cap_add'
            ))



class PortSchema(ma.Schema):
    cport = ma.Int(
        validate=validate.Range(min=0, max=65535)
    )
    hport = ma.Int(
        required=True,
        validate=validate.Range(min=0, max=65535)
    )
    proto = ma.Str(
        required=True,
        validate=validate.OneOf(['tcp','udp'])
    )

class VolumesSchema(ma.Schema):
    container = ma.Str(
        required=True
    )
    bind = ma.Str(
        required=True
    )

class EnvSchema(ma.Schema):
    label = ma.Str(
        required=True
    )
    default = ma.Str(
        required=True
    )
    # not required
    # exclude later, but it's nested in raw json data
    name = ma.Str()
    description = ma.Str()

class SysctlsSchema(ma.Schema):
    name = ma.Str(
        required=True
    )
    value = ma.Str(
        required=True
    )

class DeploySchema(ma.Schema):
    title = ma.Str(required=True)
    name = ma.Str(required=True)
    image = ma.Str(required=True)
    restart_policy = ma.Str(
        required=True,
        validate=validate.OneOf(['always','on-failure', 'unless-stopped'])
    )
    notes = ma.Str()
    ports = ma.List(ma.Nested(PortSchema))
    volumes = ma.List(ma.Nested(VolumesSchema))
    env = ma.List(ma.Nested(EnvSchema))
    sysctls = ma.List(ma.Nested(SysctlsSchema))
    cap_add = ma.List(ma.Str())
