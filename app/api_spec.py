"""OpenAPI v3 Specification"""
# apispec via OpenAPI
import json
import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow_enum import EnumField

# Create an APISpec


def enum_to_properties(self, field, **kwargs):
    """
    Add an OpenAPI extension for marshmallow_enum.EnumField instances
    """
    if isinstance(field, EnumField):
        return {"type": "string", "enum": [enum_data.value for enum_data in field.enum]}
    return {}


marshmallow_plugin = MarshmallowPlugin()

# get swagger.json file path
swagger_json_path = os.path.dirname(__file__) + "/static/swagger.json"

# load swagger.json file
with open(swagger_json_path) as apispec_info:
    spec_info = json.load(apispec_info).get("info")

spec = APISpec(
    title=spec_info.get("title"),
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), marshmallow_plugin],
    info=spec_info,
)

marshmallow_plugin.converter.add_attribute_function(enum_to_properties)

# Security
api_key_scheme = {"type": "apiKey", "in": "header", "name": "X-API-Key"}
bearer_scheme = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
spec.components.security_scheme("ApiKeyAuth", api_key_scheme)
spec.components.security_scheme("bearerAuth", bearer_scheme)

# register schemas with spec
# example
# spec.components.schema("", schema=)

# add swagger tags that are used for endpoint annotation
tags = [
    {"name": "Resource", "description": "Api Endpoints To Operate on Resources"},
]

for tag in tags:
    print(f"Adding tag: {tag['name']}")
    spec.tag(tag)
