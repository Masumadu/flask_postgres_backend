from sqlalchemy import asc, desc
from sqlalchemy.exc import DBAPIError, IntegrityError

from app import db
from app.core.exceptions.app_exceptions import AppException
from app.core.repository.base.crud_repository_interface import CRUDRepositoryInterface


class SQLBaseRepository(CRUDRepositoryInterface):
    model: db.Model

    def __init__(self):
        """
        Base class to be inherited by all repositories. This class comes with
        base crud functionalities attached

        :param model: base model of the class to be used for queries
        """

        self.db = db

    def index(self) -> [db.Model]:
        """

        :return: {list} returns a list of objects of type model
        """
        try:
            data = self.model.query.all()
            return data

        except DBAPIError as e:
            raise AppException.OperationError(error_message=e.orig.args[0])

    def create(self, obj_in: dict) -> db.Model:
        """

        :param obj_in: the data you want to use to create the model
        :return: {object} - Returns an instance object of the model passed
        """
        assert obj_in, "Missing data to be saved"

        try:
            obj_data = dict(obj_in)
            db_obj = self.model(**obj_data)
            self.db.session.add(db_obj)
            self.db.session.commit()
            return db_obj
        except IntegrityError as e:
            raise AppException.OperationError(error_message=e.orig.args[0])
        except DBAPIError as e:
            raise AppException.OperationError(error_message=e.orig.args[0])

    def update_by_id(self, obj_id: str, obj_in: dict) -> db.Model:
        """
        :param obj_id: {int} id of object to update
        :param obj_in: {dict} update data. This data will be used to update
        any object that matches the id specified
        :return: model_object - Returns an instance object of the model passed
        """
        assert obj_id, "Missing id of object to update"
        assert obj_in, "Missing update data"
        assert isinstance(obj_in, dict), "Update data should be a dictionary"

        db_obj = self.find_by_id(obj_id)

        try:
            for field in obj_in:
                if hasattr(db_obj, field):
                    setattr(db_obj, field, obj_in[field])
            self.db.session.add(db_obj)
            self.db.session.commit()
            return db_obj
        except DBAPIError as e:
            raise AppException.OperationError(error_message=e.orig.args[0])

    def update(self, filter_param: dict, obj_in: dict) -> db.Model:
        """
        :param filter_param: {dict} object to filter with
        :param obj_in: {dict} update data. This data will be used to update
        any object that matches the id specified
        :return: model_object - Returns an instance object of the model passed
        """
        assert filter_param, "Missing filter param of object to update"
        assert obj_in, "Missing update data"
        assert isinstance(obj_in, dict), "Update data should be a dictionary"

        db_obj = self.find(filter_param)

        try:
            for field in obj_in:
                if hasattr(db_obj, field):
                    setattr(db_obj, field, obj_in[field])
            self.db.session.add(db_obj)
            self.db.session.commit()
            return db_obj
        except DBAPIError as e:
            raise AppException.OperationError(error_message=e.orig.args[0])

    def find_by_id(self, obj_id: str) -> db.Model:
        """
        returns an object matching the specified id if it exists in the database
        :param obj_id: id of object to query
        :return: model_object - Returns an instance object of the model passed
        """
        assert obj_id, "Missing id of object for querying"

        try:
            db_obj = self.model.query.get(obj_id)
            if db_obj is None:
                raise AppException.NotFoundException(error_message=None)
            return db_obj
        except DBAPIError as e:
            raise AppException.OperationError(error_message=e.orig.args[0])

    def find(self, filter_param: dict) -> db.Model:
        """
        This method returns the first object that matches the query parameters specified
        :param filter_param {dict}. Parameters to be filtered by
        """
        assert filter_param, "Missing filter parameters"
        assert isinstance(
            filter_param, dict
        ), "Filter parameters should be of type dictionary"

        try:
            db_obj = self.model.query.filter_by(**filter_param).first()
            if db_obj is None:
                raise AppException.NotFoundException(error_message=None)
            return db_obj
        except DBAPIError as e:
            raise AppException.OperationError(error_message=e.orig.args[0])

    def find_all(self, filter_param: dict) -> db.Model:
        """
        This method returns all objects that matches the query
        parameters specified
        """
        assert filter_param, "Missing filter parameters"
        assert isinstance(
            filter_param, dict
        ), "Filter parameters should be of type dictionary"

        try:
            db_obj = self.model.query.filter_by(**filter_param).all()
            return db_obj
        except DBAPIError as e:
            raise AppException.OperationError(error_message=e.orig.args[0])

    def delete_by_id(self, obj_id: str):
        """
        :param obj_id: id of the object to delete
        :return:
        """

        db_obj = self.find_by_id(obj_id)
        try:
            db.session.delete(db_obj)
            db.session.commit()
        except DBAPIError as e:
            raise AppException.OperationError(error_message=e.orig.args[0])

    def delete(self, filter_param: dict):
        """
        :param filter_param: object to filter with
        :return:
        """

        db_obj = self.find(filter_param)
        try:
            db.session.delete(db_obj)
            db.session.commit()
        except DBAPIError as e:
            raise AppException.OperationError(error_message=e.orig.args[0])

    def paginate(self, page: int, per_page: int) -> [db.Model]:
        """

        This method returns a list of paginated objects
        :param page: the page number
        :param per_page: the number of items to return for each page
        :return: {list} returns a list of objects of type model
        """
        try:
            data = self.model.query.paginate(
                page=page, per_page=per_page, error_out=False
            ).items
            return data
        except DBAPIError as e:
            raise AppException.OperationError(error_message=e.orig.args[0])

    def filter_paginate(
        self, filter_param: dict, page: int, per_page: int
    ) -> [db.Model]:
        """

        This method returns a list of paginated objects
        :param filter_param: object to filter with
        :param page: the page number
        :param per_page: the number of items to return for each page
        :return: {list} returns a list of objects of type model
        """

        try:
            data = (
                self.model.query.filter_by(**filter_param)
                .paginate(page=page, per_page=per_page, error_out=False)
                .items
            )
            return data
        except DBAPIError as e:
            raise AppException.OperationError(error_message=e.orig.args[0])

    def filter_sort_paginate(
        self, filter_param: dict, sort_in: str, sort_by: str, page: int, per_page: int
    ) -> [db.Model]:
        """

        This method returns a list of paginated objects
        :param filter_param: the object to filter with
        :param sort_by: record column to sort the objects with
        :param sort_in: the order to sort the objects in
        :param page: the page number
        :param per_page: the number of items to return for each page
        :return: {list} returns a list of objects of type model
        """
        try:
            if sort_in.lower() == "asc":
                result = (
                    self.model.query.filter_by(**filter_param)
                    .order_by(asc(getattr(self.model, sort_by)))
                    .paginate(page=page, per_page=per_page, error_out=False)
                    .items
                )
            elif sort_in.lower() == "desc":
                result = (
                    self.model.query.filter_by(**filter_param)
                    .order_by(desc(getattr(self.model, sort_by)))
                    .paginate(page=page, per_page=per_page, error_out=False)
                    .items
                )
            else:
                raise AppException.OperationError(error_message="invalid sort order")
            return result
        except DBAPIError as e:
            raise AppException.OperationError(error_message=e.orig.args[0])
