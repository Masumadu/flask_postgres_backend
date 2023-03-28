from marshmallow import Schema, fields


class ResourceSchema(Schema):
    id = fields.UUID(allow_none=True)
    title = fields.String()
    content = fields.String(allow_none=True)
    created = fields.DateTime()
    modified = fields.DateTime()

    class Meta:
        ordered = True


class CreateResourceSchema(ResourceSchema):
    title = fields.String(required=True)
    content = fields.String(required=True)

    class Meta:
        fields = ["title", "content"]


class UpdateResourceSchema(Schema):
    title = fields.String()
    content = fields.String()

    class Meta:
        fields = ["title", "content"]


class ResourceRequestArgumentSchema(Schema):
    resource_id = fields.UUID()
    page = fields.Integer()
    per_page = fields.Integer()
    refresh_token = fields.String()
