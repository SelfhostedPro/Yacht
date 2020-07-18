from .. import ma
from ..models import (
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
            exclude=('template_id','restart_policy'))



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

class SysctlsSchema(ma.Schema):
    name = ma.Str()
    value = ma.Str()

class DeploySchema(ma.Schema):
    title = ma.Str(required=True)
    name = ma.Str(required=True)
    image = ma.Str(required=True)
    notes = ma.Str(required=True)
    restart_policy = ma.Str(
        required=True,
        validate=validate.OneOf(['always','on-failure', 'unless-stopped'])
    )
    ports = ma.List(ma.Nested(PortSchema))
    volumes = ma.List(ma.Nested(VolumesSchema))
    env = ma.List(ma.Nested(EnvSchema))
    sysctls = ma.List(ma.Nested(SysctlsSchema))
    cap_add = ma.List(ma.Str())





# class TemplateItemSchema(ma.SQLAlchemySchema):
#     id = ma.Int(
#         dump_only=True)
#
#     template_id=ma.Int(
#         required=True)
#     type = ma.Int()
#     title = ma.Str(
#         validate=Length(min=1, max=255))
#     platform = ma.Str(
#         validate=Length(min=1, max=255))
#     description = ma.Str()
#     name = ma.Str(
#         validate=Length(min=1, max=255))
#     logo = ma.Str(
#         validate=Length(min=1, max=255))
#     notes = ma.Str()
#     categories = ma.List(ma.Str())
#     # configuration data
#     restart_policy = ma.Str()   # perhaps dump_only=True
#     ports = ma.Raw()            # perhaps dump_only=True
#     volumes = ma.Raw()          # perhaps dump_only=True
#     env = ma.Raw()              # perhaps dump_only=True
#
#
# class TemplateSchema(ma.SQLAlchemySchema):
#     # perhapse use auto_field
#     id = ma.Int(
#         dump_only=True)
#     created_at = ma.DateTime(
#         dump_only=True)
#     updated_at = ma.DateTime(
#         dump_only=True)
#     title = ma.Str(
#         required=True,
#         validate=Length(min=1, max=255))
#     url = ma.Url(
#         required=True)
#     items = ma.Nested(
#         TemplateItemSchema, many=True,
#         exclude=('template_id','restart_policy','ports','volumes','env'))