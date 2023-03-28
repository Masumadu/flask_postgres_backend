import pinject
from flask import Blueprint, request

from app.controllers import ResourceController

from app.core.service_result import handle_result
from app.repositories import ResourceRepository

from app.schema import (
    ResourceSchema, CreateResourceSchema,
    UpdateResourceSchema, ResourceRequestArgumentSchema
)
from app.services import RedisService, AuthService
from app.utils import arg_validator, auth_required, validator

resource = Blueprint("resource", __name__)

obj_graph = pinject.new_object_graph(
    modules=None,
    classes=[
        ResourceController,
        ResourceRepository,
        ResourceSchema,
        RedisService,
        AuthService
    ],
)
resource_controller: ResourceController = obj_graph.provide(ResourceController)


@resource.route("/", methods=["POST"])
@validator(schema=CreateResourceSchema)
def create_resource():
    """
    ---
    post:
      description: create a resource
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateResourceSchema
      responses:
        '201':
          description: returns created resource
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: uuid
                    example: 3fa85f64-5717-4562-b3fc-2c963f66afa6
        '500':
          description: internal server error
          content:
            application/json:
              schema:
                type: object
                properties:
                  app_exception:
                    type: str
                    example: InternalServerError
                  errorMessage:
                    type: str
                    example: Resource Exists
      tags:
          - Resource
    """

    data = request.json
    result = resource_controller.create_resource(data)
    return handle_result(result, schema=ResourceSchema)


@resource.route("/", methods=["GET"])
@arg_validator(schema=ResourceRequestArgumentSchema, param="page|per_page")
def get_all_resources():
    """
    ---
    get:
      description: retrieve all resources
      parameters:
        - in: query
          name: page
          required: true
          schema:
            type: string
          description: the page to show
        - in: query
          name: per_page
          required: true
          schema:
            type: string
          description: the records to show on page
      responses:
        '200':
          description: returns list of resources
          content:
            application/json:
              schema:
                type: array
                items: ResourceSchema
      tags:
          - Resource
    """
    query_param = request.args
    result = resource_controller.get_all_resources(query_param)
    return handle_result(result, schema=ResourceSchema, many=True)


@resource.route("/<string:resource_id>", methods=["GET"])
@arg_validator(schema=ResourceRequestArgumentSchema, param="resource_id")
def get_resource(resource_id):
    """
    ---
    get:
      description: retrieve resource with id specified in path
      parameters:
        - in: path
          name: resource_id
          required: true
          schema:
            type: string
          description: The resource id
      responses:
        '200':
          description: returns resource
          content:
            application/json:
              schema: ResourceSchema
        '404':
          description: not found
          content:
            application/json:
              schema:
                type: object
                properties:
                  app_exception:
                    type: str
                    example: NotFoundException
                  errorMessage:
                    type: str
                    example: resource does not exist
      tags:
          - Resource
    """
    result = resource_controller.get_resource(resource_id)
    return handle_result(result, schema=ResourceSchema)


@resource.route("/<string:resource_id>", methods=["PATCH"])
@auth_required()
@arg_validator(schema=ResourceRequestArgumentSchema, param="resource_id")
@validator(schema=UpdateResourceSchema)
def update_resource(resource_id):
    """
    ---
    patch:
      description: update resource with id specified in path
      security:
        - bearerAuth: []
      parameters:
        - in: path
          name: resource_id
          required: true
          schema:
            type: string
          description: id of resource
      requestBody:
        required: true
        content:
          application/json:
            schema: UpdateResourceSchema
      responses:
        '200':
          description: returns a updated resource
          content:
            application/json:
              schema: ResourceSchema
        '401':
          description: Unauthorized
          content:
            application/json:
              schema:
                type: object
                properties:
                  app_exception:
                    type: str
                    example: Unauthorized
                  errorMessage:
                    type: str
                    example: missing authentication token
        '404':
          description: not found
          content:
            application/json:
              schema:
                type: object
                properties:
                  app_exception:
                    type: str
                    example: NotFoundException
                  errorMessage:
                    type: str
                    example: resource does not exist
        '500':
          description: returns an internal server error exception
          content:
            application/json:
              schema:
                type: object
                properties:
                  app_exception:
                    type: str
                    example: InternalServerError
                  error_message:
                    type: str
                    example: error updating resource
      tags:
          - Resource
    """

    data = request.json
    result = resource_controller.update_resource(resource_id, data)
    return handle_result(result, schema=ResourceSchema)


@resource.route("/<string:resource_id>", methods=["DELETE"])
@auth_required()
@arg_validator(schema=ResourceRequestArgumentSchema, param="resource_id")
def delete_resource(resource_id):
    """
    ---
    delete:
      description: delete resource with id specified in path
      security:
        - bearerAuth: []
      parameters:
        - in: path
          name: resource_id
          required: true
          schema:
            type: string
          description: The resource id
      responses:
        '200':
          description: returns nil
        '401':
          description: unauthorised
          content:
            application/json:
              schema:
                type: object
                properties:
                  app_exception:
                    type: str
                    example: Unauthorized
                  errorMessage:
                    type: str
                    example: missing authentication token
        '404':
          description: not found
          content:
            application/json:
              schema:
                type: object
                properties:
                  app_exception:
                    type: str
                    example: NotFoundException
                  errorMessage:
                    type: str
                    example: resource does not exist
      tags:
          - Resource
    """
    result = resource_controller.delete_resource(resource_id)
    return handle_result(result)


@resource.route("/get-token", methods=["GET"])
def get_access_token():
    """
    ---
    get:
      description: retrieve access token
      responses:
        '200':
          description: returns token
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: str
                    example: d75f29a55d76a6a8dc6c8ced09e20e3acd363e9a478769e6de904b86064
                  refresh_token:
                    type: str
                    example: d75f29a55d76a6a8dc6c8ced09e20e3acd363e9a478769e6de904b86064

      tags:
          - Resource
    """
    result = resource_controller.get_token()
    return handle_result(result)


@resource.route("/refresh-token", methods=["GET"])
@arg_validator(schema=ResourceRequestArgumentSchema, param="refresh_token")
def get_refresh_token():
    """
    ---
    get:
      description: refresh access token
      parameters:
        - in: query
          name: refresh_token
          required: true
          schema:
            type: string
          description: the refresh token
      responses:
        '200':
          description: returns token
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: str
                    example: d75f29a55d76a6a8dc6c8ced09e20e3acd363e9a478769e6de904b86064
                  refresh_token:
                    type: str
                    example: d75f29a55d76a6a8dc6c8ced09e20e3acd363e9a478769e6de904b86064

      tags:
          - Resource
    """
    query_params = request.args
    result = resource_controller.get_refresh_token(query_params)
    return handle_result(result)
