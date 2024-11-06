from flask_restplus import fields

from main.util.namespace import user_dataset_review_ns


class DatasetObject:
    # General Message
    dataset_review_msg_resp = user_dataset_review_ns.model("1. dataset_review_msg_resp", {
        'message': fields.String(description='Success or Fail'),
        'notification': fields.String(description='Customized notification')
    })

    # The original info about the single dataset
    dataset_review_req = user_dataset_review_ns.model("2. dataset_review_req", {
        'name': fields.String(description='Dataset Name', required=True),
        'location': fields.String(description='Dataset official link', required=True),
        'originator': fields.String(description='Dataset Author', required=True)
    })

    # The AIBOM attributes of the single dataset
    pending_aibom = user_dataset_review_ns.model("3. pending_aibom", {
        'id': fields.Integer(description='Dataset ID in table pending_aibom ，this id is required when you use pending_aibom in the request.', required=True),
        # The AIBOM attributes
        'name': fields.String(description='Dataset Name', required=True),
        'location': fields.String(description='Dataset official link', required=True),
        'originator': fields.String(description='Dataset Author', required=True),
        'license_location': fields.String(description='Dataset link', required=True),
        'concluded_license': fields.String(description='License in SPDX license list'),
        'declared_license': fields.String(description='Customized license'),
        'type': fields.String(description='Dataset format，such as image、audio、video etc.', enum=['image', 'radio', 'video', 'binary', 'others'], required=True),
        'size': fields.String(description='Size of dataset', required=True),
        'intended_use': fields.String(description='The usage of dataset', required=True),
        'checksum': fields.String(description='Checksum'),
        'data_collection_process': fields.String(description='Process of data collection'),
        'known_biases': fields.Boolean(description='The dataset contains biases or not'),
        'sensitive_personal_information': fields.Boolean(description='The dataset contains personal info or not'),
        'offensive_content': fields.Boolean(description='The dataset contains offensive content or not'),
        # User info
        'user_id': fields.Integer(description='The id of AIBOM author', required=True),
        # Rejection remarks
        'rejection_notes': fields.String(description='Only used in pending_AIBOM or reject_review，when this AIBOM was rejected by reviewer.'),
    })

    # The review result of datasets
    review_result = user_dataset_review_ns.model("4. review_result", {
        'id': fields.Integer(description='Dataset ID in table pending_aibom ，this id is required when you use pending_aibom in the request.', required=True),
        # The AIBOM attributes
        'name': fields.String(description='Dataset Name', required=True),
        'location': fields.String(description='Dataset official link', required=True),
        'originator': fields.String(description='Dataset Author', required=True),
        'license_location': fields.String(description='Dataset link', required=True),
        'concluded_license': fields.String(description='License in SPDX license list'),
        'declared_license': fields.String(description='Customized license'),
        'type': fields.String(description='Dataset format，such as image、audio、video etc.', enum=['image', 'radio', 'video', 'binary', 'others'], required=True),
        'size': fields.String(description='Size of dataset', required=True),
        'intended_use': fields.String(description='The usage of dataset', required=True),
        'checksum': fields.String(description='Checksum'),
        'data_collection_process': fields.String(description='Process of data collection'),
        'known_biases': fields.Boolean(description='The dataset contains biases or not'),
        'sensitive_personal_information': fields.Boolean(description='The dataset contains personal info or not'),
        'offensive_content': fields.Boolean(description='The dataset contains offensive content or not'),
        # User info
        'user_id': fields.Integer(description='The id of AIBOM author', required=True),
        # Initial review comments
        'review_result_initial': fields.String(description='Initial review comments', required=True),
        'is_dataset_commercially_used_initial': fields.Boolean(description='The dataset can be used commercially or not', required=True),
        'is_dataset_commercially_distributed_initial': fields.Boolean(description='The dataset can be distributed commercially or not', required=True),
        'is_product_commercially_published_initial': fields.Boolean(description='The dataset can be integrated in commercial products or not', required=True),
        'right_initial': fields.String(description='Initial rights analysis'),
        'obligation_initial': fields.String(description='Initial obligations analysis'),
        'limitation_initial': fields.String(description='Initial limitations analysis'),
        'notes_initial': fields.String(description='Initial reviews'),
        # Final review comments
        'review_result_final': fields.String(description='Final reviews', required=True),
        'is_dataset_commercially_used_final': fields.Boolean(description='The dataset can be used commercially or not', required=True),
        'is_dataset_commercially_distributed_final': fields.Boolean(description='The dataset can be distributed commercially or not', required=True),
        'is_product_commercially_published_final': fields.Boolean(description='The dataset can be integrated in commercial products or not', required=True),
        'right_final': fields.String(description='Final rights analysis'),
        'obligation_final': fields.String(description='Final obligations analysis'),
        'limitation_final': fields.String(description='Final limitations analysis'),
        'notes_final': fields.String(description='Final reviews'),
    })

    # The review notes of batch datasets
    dataset_review_list_req = user_dataset_review_ns.model("5. dataset_review_list_req", {
        'user_id': fields.Integer(description='The id of AIBOM author', required=True),
        'dataset_review_list': fields.List(fields.Nested(dataset_review_req), description='The review notes of a single dataset', required=True)
    })

    # Batch datasets is reviwed or not
    dataset_is_reviewed_list_resp = user_dataset_review_ns.model("6. dataset_is_reviewed_list_resp", {
        'review_result_list': fields.List(fields.Nested(review_result), description='The review notes of batch datasets'),
        'pending_aibom_list': fields.List(fields.Nested(pending_aibom), description='The AIBOMs of batch datasets'),
        'message': fields.String(description='Success or fail'),
        'notification': fields.String(description='Customized notification')
    })

    # Store the AIBOMs of batch datasets
    pending_aibom_list_req = user_dataset_review_ns.model("7. pending_aibom_list_req", {
        'pending_aibom_list': fields.List(fields.Nested(pending_aibom), description='The AIBOMs of batch datasets', required=True)
    })

    # Return the AIBOMs of batch datasets
    pending_aibom_list_resp = user_dataset_review_ns.model("8. pending_aibom_list_resp", {
        'pending_aibom_list': fields.List(fields.Nested(pending_aibom), description='The AIBOMs of batch datasets'),
        'message': fields.String(description='Success or fail'),
        'notification': fields.String(description='Customized notification')
    })

    # Revise the status，if pending AIBOM，delete it，if pending review，revise the pending AIBOM
    dataset_state_rollback_req = user_dataset_review_ns.model("9. dataset_state_rollback_req", {
        'user_id': fields.Integer(description='The id of AIBOM author', required=True),
        'pending_aibom_review_ids': fields.List(fields.Integer, description='The dataset id in table pending_aibom or pending_review', required=True),
        'rejection_notes': fields.List(fields.String, description='The count of review notes，The count of rejection_notes <= The count of pending_aibom_review_ids')
    })

    # Store review notes of batch datasets
    pending_review_list_req = user_dataset_review_ns.model("10. pending_review_list_req", {
        'pending_review_list': fields.List(fields.Nested(review_result), description='The review notes of batch datasets', required=True)
    })

    # Return review notes of batch datasets
    pending_review_list_resp = user_dataset_review_ns.model("11. pending_review_list_resp", {
        'pending_review_list': fields.List(fields.Nested(review_result), description='The review notes of batch datasets'),
        'message': fields.String(description='Success or fail'),
        'notification': fields.String(description='Customized notification')
    })

    # Return final review notes of batch datasets
    review_result_list_resp = user_dataset_review_ns.model("12. review_result_list_resp", {
        'review_result_list': fields.List(fields.Nested(review_result), description='The review notes of batch datasets'),
        'message': fields.String(description='Success or fail'),
        'notification': fields.String(description='Customized notification')
    })

    # Single license info
    dataset_license = user_dataset_review_ns.model("13. dataset_license", {
        'full_name': fields.String(description='License', required=True),
        'identifier': fields.String(description='License identifier', required=True),
        'fsf_free_libre': fields.String(description='fsf_free/libre', required=False),
        'osi_approved': fields.String(description='osi approved', required=False)
    })

    # Batch licenses info
    dataset_license_list_req = user_dataset_review_ns.model("14. dataset_review_list_req", {
        'user_id': fields.Integer(description='The id of AIBOM author', required=True),
        'dataset_license_list': fields.List(fields.Nested(dataset_license), description='Batch upload info', required=True)
    })

    # The result of Batch licenses info
    dataset_license_list_resp = user_dataset_review_ns.model("15. dataset_license_list_resp", {
        'license_success_list': fields.List(fields.Nested(dataset_license), description='Uploaded license info'),
        'license_fail_list': fields.List(fields.Nested(dataset_license), description='Failed license info'),
        'message': fields.String(description='Success or fail'),
        'notification': fields.String(description='Customized notification')
    })

    # The result of Batch licenses info
    license_list_resp = user_dataset_review_ns.model("16. license_list_resp", {
        'spdx_license_list': fields.List(fields.Nested(dataset_license), description='License list'),
        'message': fields.String(description='Success or fail'),
        'notification': fields.String(description='Customized notification')
    })

    string_req = user_dataset_review_ns.model("17. String Req", {
        'text': fields.String(description='text'),
    })
