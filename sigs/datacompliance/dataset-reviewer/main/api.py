from flask import Blueprint
from flask_restplus import Api

from main.controller.dataset_review import user_dataset_review_ns, auth_dataset_review_ns


blueprint = Blueprint("api", __name__)
api = Api(
    blueprint,
    version=0.1,
    title="APIs for OpenDataology service toolset",
    description="Welcome to the OpenDataology service backend API document!"
)

api.add_namespace(user_dataset_review_ns, '/user/dataset_review')
api.add_namespace(auth_dataset_review_ns, '/auth/dataset_review')
