"""
Define the resources for the review
"""
from flask import jsonify, abort
from flasgger import swag_from
from flask_restful import Resource
from flask_restful.reqparse import Argument
import json
from repositories import ReviewRepository
from utils import parse_params
from utils.errors import DataNotFound


class ReviewResource(Resource):
    """ methods relative to the review """

    @staticmethod
    @swag_from("../swagger/review/get_one.yml")
    def get_one(review_id):
        """ Return a review """

        try:
            review = ReviewRepository.get(review_id=review_id)
            return jsonify({"data": review.json})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception:
            abort(500)

    @staticmethod
    @swag_from("../swagger/review/get_all.yml")
    def get_all():
        """ Return all review key information based on the query parameter """
        reviews = ReviewRepository.getAll()
        return jsonify({"data": reviews})

    @staticmethod
    @parse_params(
        Argument("comment", location="json",
                 help="The comment for a review."),
        Argument("images", location="json",
                 help="The image for a review."),
        Argument("sellers_id", location="json",
                 help="The sellers_id for a review"),
        Argument("products_id", location="json",
                 help="The products_id for a review"),
    )
    def post(comment, images, sellers_id, products_id):
        """ Create a review """
        review = ReviewRepository.create(
            comment=comment, images=images,
            sellers_id=sellers_id,
            products_id=products_id
        )
        return jsonify({"data": review.json})

    @staticmethod
    @parse_params(
        Argument("comment", location="json",
                 help="The comment for a review."),
        Argument("images", location="json",
                 help="The image for a review.")
    )
    def update(review_id, comment, images):
        """ Update a review"""
        repo = ReviewRepository()
        review = repo.update(
            review_id=review_id, comment=comment, images=images
        )

        return jsonify({"data": {"message": "review updated"}})

    def delete(review_id):
        """ delete a review via the provided id """
        ReviewRepository.delete(review_id=review_id)
        return jsonify({"message": "review successfully deleted"})
