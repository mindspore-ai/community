from flask_restplus import fields

from main.util.namespace import user_dataset_review_ns


class UserObject:
    AIBOM_user = user_dataset_review_ns.model("AIBOM_user", {
        'user_id': fields.Integer(description='user id', required=True),
    })
