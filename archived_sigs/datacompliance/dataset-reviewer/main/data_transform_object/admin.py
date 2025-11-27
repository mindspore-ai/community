from flask_restplus import fields

from main.util.namespace import user_dataset_review_ns


class AdminObject:
    Admin_user_req = user_dataset_review_ns.model("Admin_user_req", {
        'user_id': fields.Integer(description='user id', required=True),
        'account': fields.String(description='user account', required=True)
    })
