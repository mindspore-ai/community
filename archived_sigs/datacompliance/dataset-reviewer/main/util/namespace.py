from flask_restplus import Namespace

user_dataset_review_ns = Namespace("User End - Dataset Review API",
                                   description="All functions for dataset review.")

auth_dataset_review_ns = Namespace("Review End - Dataset Review API",
                                   description="All functions for dataset review.")
