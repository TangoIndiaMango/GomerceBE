"""
Define the resources for the order detail
"""
from flask import jsonify, abort
from flasgger import swag_from
from flask_restful import Resource
from flask_restful.reqparse import Argument
from repositories import OrderDetailRepository
from utils import parse_params
from utils.errors import DataNotFound


class OrderDetailResource(Resource):
    """ methods relative to the order detail """

    @staticmethod
    @swag_from("../swagger/order_detail/get_one.yml")
    def get_one(detail_id):
        """ Return an order key information based on order_id """

        try:
            order_detail = OrderDetailRepository.get(detail_id=detail_id)
            return jsonify({"data": order_detail.json})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception:
            abort(500)

    @staticmethod
    @swag_from("../swagger/order_detail/get_all.yml")
    def get_all():
        """ Return all order detail key information based on the query parameter """
        order_details = OrderDetailRepository.getAll()
        return jsonify({"data": order_details})

    @staticmethod
    @parse_params(
        Argument("sku", location="json",
                 help="The sku of the order."),
        Argument("order_id", location="json",
                 help="The order_id of the order."),
        Argument("products_id", location="json",
                 help="The products_id of the order."),
        Argument("statuses_id", location="json",
                 help="The statuses of the order."),
    )
    def update(order_detail_id, sku, order_id, products_id, statuses_id):
        """ Update a order """
        order = OrderDetailRepository().update(
            order_detail_id=order_detail_id,
            sku=sku, order_id=order_id,
            products_id=products_id,
            statuses_id=statuses_id
        )
        return jsonify({"data": order.json})

    @staticmethod
    @parse_params(
        Argument("sku", location="json",
                 help="The sku of the order."),
        Argument("order_id", location="json",
                 help="The order_id of the order."),
        Argument("products_id", location="json",
                 help="The products_id of the order."),
        Argument("order_id", location="json",
                 help="The order of the order."),
        Argument("statuses_id", location="json",
                 help="The statuses of the order."),
    )
    def post(sku, order_id, products_id, statuses_id):
        """ Create an order detail """

        order = OrderDetailRepository.create(
            sku=sku, order_id=order_id,
            products_id=products_id,
            statuses_id=statuses_id,
        )
        return jsonify({"data": order.json})

    def delete(order_detail_id):
        """ delete a order via the provided id """
        OrderDetailRepository.delete(order_detail_id=order_detail_id)
        return jsonify({"message": "order successfully deleted"})
