from flask import request
from flask import json

from flask import send_from_directory, make_response

from flask_restplus import Resource
from flask_restplus import marshal

from main.data_transform_object.dataset import DatasetObject
from main.data_transform_object.user import UserObject
from main.data_transform_object.admin import AdminObject

from main.util.namespace import user_dataset_review_ns, auth_dataset_review_ns
from main.service import dataset_review


@user_dataset_review_ns.route("/review_upload")
class ReviewUpload(Resource):
    @user_dataset_review_ns.expect(DatasetObject.dataset_review_list_req)
    @user_dataset_review_ns.response(200, 'success', model=DatasetObject.dataset_is_reviewed_list_resp)
    @user_dataset_review_ns.response(403, 'fail', model=DatasetObject.dataset_review_msg_resp)
    def post(self):
        """
            Upon uploading a dataset for review, the system will immediately provide conclusions for the portions of the
            dataset that have already undergone review. Any sections that have not yet been audited will be placed
            in a "pending_AIBOM" category, allowing the calling party to supplement
            AIBOM (Artificial Intelligence Bill of Materials) information as necessary.
        """
        dataset_review_list_req = json.loads(
            request.data)  # Parse request into a dictionary

        # Execute the specific method, and get the returned dictionary
        user_id = dataset_review_list_req['user_id']
        dataset_review_list = dataset_review_list_req['dataset_review_list']
        response_dict = dataset_review.review_upload(
            user_id, dataset_review_list)

        # success or fail
        status_code = 200 if response_dict['message'] == 'success' else 403

        model_ret = DatasetObject.dataset_is_reviewed_list_resp if status_code == 200 else DatasetObject.dataset_review_msg_resp

        return marshal(response_dict, model_ret), status_code


@user_dataset_review_ns.route("/review_upload_by_file")
class ReviewUploadByFile(Resource):
    @user_dataset_review_ns.expect(DatasetObject.dataset_review_list_req)
    @user_dataset_review_ns.response(200, 'success', model=DatasetObject.dataset_is_reviewed_list_resp)
    @user_dataset_review_ns.response(403, 'fail', model=DatasetObject.dataset_review_msg_resp)
    def post(self):
        """
            The dataset review process involves batch uploading through files. It will promptly provide conclusions
            for the portions of the dataset that have undergone review. Any sections that have not yet been assessed
            will be categorized as "pending_AIBOM," allowing the calling party to add
            AIBOM (Artificial Intelligence Bill of Materials) information when necessary.
        """
        user_id = request.form.get("user_id")
        dataset_review_list_req = request.files.get('dataset_review_list')

        dataset_review_list = dataset_review.file_convert_dataset(
            user_id, dataset_review_list_req)

        if dataset_review_list['message'] == 'success':
            dataset_review_list = dataset_review_list['notification']
            # Execute the specific method, and get the returned dictionary
            response_dict = dataset_review.review_upload(
                user_id, dataset_review_list)
        else:
            response_dict = dataset_review_list

        # success or fail
        status_code = 200 if response_dict['message'] == 'success' else 403

        model_ret = DatasetObject.dataset_is_reviewed_list_resp if status_code == 200 else DatasetObject.dataset_review_msg_resp

        return marshal(response_dict, model_ret), status_code


@user_dataset_review_ns.route("/pending_AIBOM")
class PendingAIBOM(Resource):
    @user_dataset_review_ns.expect(UserObject.AIBOM_user)
    @user_dataset_review_ns.response(200, 'success', model=DatasetObject.pending_aibom_list_resp)
    @user_dataset_review_ns.response(403, 'fail', model=DatasetObject.dataset_review_msg_resp)
    def get(self):
        """
            Retrieve a list of datasets requiring AIBOM information supplementation using the provided user_id.
        """
        user_id = int(request.args.get('user_id', ''))

        # Execute the specific method, and get the returned dictionary
        response_dict = dataset_review.get_pending_aibom_by_user(user_id)

        # success or fail
        status_code = 200 if response_dict['message'] == 'success' else 403

        model_ret = DatasetObject.pending_aibom_list_resp if status_code == 200 else DatasetObject.dataset_review_msg_resp

        return marshal(response_dict, model_ret), status_code


@user_dataset_review_ns.route("/save_AIBOM")
class SaveAIBOM(Resource):
    @user_dataset_review_ns.expect(DatasetObject.pending_aibom_list_req)
    @user_dataset_review_ns.response(200, 'success', model=DatasetObject.dataset_review_msg_resp)
    @user_dataset_review_ns.response(403, 'fail', model=DatasetObject.dataset_review_msg_resp)
    def post(self):
        """
            Temporarily store the AIBOM information supplemented by the given user_id.
        """
        hashmap = json.loads(request.data)
        pending_aibom_list = hashmap.get('pending_aibom_list', '')

        # Execute the specific method, and get the returned dictionary
        response_dict = dataset_review.save_pending_aibom_list(
            pending_aibom_list)

        # success or fail
        status_code = 200 if response_dict['message'] == 'success' else 403

        model_ret = DatasetObject.dataset_review_msg_resp

        return marshal(response_dict, model_ret), status_code


@user_dataset_review_ns.route("/submit_AIBOM")
class SubmitAIBOM(Resource):
    @user_dataset_review_ns.expect(DatasetObject.pending_aibom_list_req)
    @user_dataset_review_ns.response(200, 'success', model=DatasetObject.dataset_review_msg_resp)
    @user_dataset_review_ns.response(403, 'fail', model=DatasetObject.pending_aibom_list_resp)
    def post(self):
        """
            Submit the AIBOM information supplemented by the provided user_id.
            If required information is incorrectly formatted or missing, a corresponding dataset list will be returned.
            The correct portions of datasets will be sent to the review side, and the "pending AIBOM" status will be removed.
            Format check: name, location, originator, license_location, type, size, intended_use, and user_id cannot be empty.
            The concluded_license and declared_license cannot be both empty simultaneously.
        """
        hashmap = json.loads(request.data)
        pending_aibom_list = hashmap.get('pending_aibom_list', '')

        # Execute the specific method, and get the returned dictionary
        dataset_review.save_pending_aibom_list(pending_aibom_list)  # 在提交前先临时保存
        response_dict = dataset_review.submit_pending_aibom_list(
            pending_aibom_list)

        # success or fail
        status_code = 200 if response_dict['message'] == 'success' else 403

        model_ret = DatasetObject.dataset_review_msg_resp if status_code == 200 else DatasetObject.pending_aibom_list_resp

        return marshal(response_dict, model_ret), status_code


@user_dataset_review_ns.route("/remove_AIBOM")
class RemoveAIBOM(Resource):
    @user_dataset_review_ns.expect(DatasetObject.dataset_state_rollback_req)
    @user_dataset_review_ns.response(200, 'success', model=DatasetObject.dataset_review_msg_resp)
    @user_dataset_review_ns.response(403, 'fail', model=DatasetObject.dataset_review_msg_resp)
    def post(self):
        """
            Allow users to choose to delete certain datasets while supplementing AIBOM information.
        """
        hashmap = json.loads(request.data)
        user_id = hashmap.get('user_id', "")
        pending_aibom_ids = set(hashmap.get('pending_aibom_review_ids', ''))

        # Execute the specific method, and get the returned dictionary
        response_dict = dataset_review.remove_pending_aibom_list(
            user_id, pending_aibom_ids)

        # success or fail
        status_code = 200 if response_dict['message'] == 'success' else 403

        model_ret = DatasetObject.dataset_review_msg_resp

        return marshal(response_dict, model_ret), status_code


@user_dataset_review_ns.route("/get_license")
class GetLicense(Resource):
    @user_dataset_review_ns.expect(DatasetObject.string_req)
    @user_dataset_review_ns.response(200, 'success', model=DatasetObject.license_list_resp)
    @user_dataset_review_ns.response(403, 'fail', model=DatasetObject.dataset_review_msg_resp)
    def get(self):
        """
            Retrieve a list of licenses that match the fuzzy query based on the provided text.
            If no text is provided, the default behavior is to retrieve the complete list of licenses.
        """
        text = request.args.get('text', '')

        # Execute the specific method, and get the returned dictionary
        response_dict = dataset_review.get_dataset_license_list(text)

        # success or fail
        status_code = 200 if response_dict['message'] == 'success' else 403

        model_ret = DatasetObject.license_list_resp if status_code == 200 else DatasetObject.dataset_review_msg_resp

        return marshal(response_dict, model_ret), status_code


@auth_dataset_review_ns.route("/is_admin")
class IsAdmin(Resource):
    @auth_dataset_review_ns.expect(AdminObject.Admin_user_req)
    @auth_dataset_review_ns.response(200, 'success', model=DatasetObject.dataset_review_msg_resp)
    @auth_dataset_review_ns.response(403, 'fail', model=DatasetObject.dataset_review_msg_resp)
    def post(self):
        """
            Check if the user is an admin. Return "success" if successful and "fail" if unsuccessful.
        """
        hashmap = json.loads(request.data)

        user_id = hashmap.get('user_id', '')
        account = hashmap.get('account', '')

        # Execute the specific method, and get the returned dictionary
        response_dict = dataset_review.is_admin(user_id, account)

        # success or fail
        status_code = 200 if response_dict['message'] == 'success' else 403

        model_ret = DatasetObject.dataset_review_msg_resp

        return marshal(response_dict, model_ret), status_code


@auth_dataset_review_ns.route("/pending_review")
class PendingReview(Resource):
    @auth_dataset_review_ns.expect(UserObject.AIBOM_user)
    @auth_dataset_review_ns.response(200, 'success', model=DatasetObject.pending_review_list_resp)
    @auth_dataset_review_ns.response(403, 'fail', model=DatasetObject.dataset_review_msg_resp)
    def get(self):
        """
            Retrieve datasets pending approval for the specified user_id. If no user_id is provided, retrieve all datasets pending approval.
        """
        user_id = int(request.args.get('user_id', -1))

        # Execute the specific method, and get the returned dictionary
        response_dict = dataset_review.get_pending_review_list(user_id)

        # success or fail
        status_code = 200 if response_dict['message'] == 'success' else 403

        model_ret = DatasetObject.pending_review_list_resp if status_code == 200 else DatasetObject.dataset_review_msg_resp

        return marshal(response_dict, model_ret), status_code


@auth_dataset_review_ns.route("/save_review")
class SaveReview(Resource):
    @auth_dataset_review_ns.expect(DatasetObject.pending_review_list_req)
    @auth_dataset_review_ns.response(200, 'success', model=DatasetObject.dataset_review_msg_resp)
    @auth_dataset_review_ns.response(403, 'fail', model=DatasetObject.dataset_review_msg_resp)
    def post(self):
        """
            Temporarily store the information filled out by the reviewer.
        """
        hashmap = json.loads(request.data)
        pending_review_list = hashmap.get('pending_review_list', '')

        # Execute the specific method, and get the returned dictionary
        response_dict = dataset_review.save_pending_review_list(
            pending_review_list)

        # success or fail
        status_code = 200 if response_dict['message'] == 'success' else 403

        model_ret = DatasetObject.dataset_review_msg_resp

        return marshal(response_dict, model_ret), status_code


@auth_dataset_review_ns.route("/reject_review")
class RejectReview(Resource):
    @auth_dataset_review_ns.expect(DatasetObject.dataset_state_rollback_req)
    @auth_dataset_review_ns.response(200, 'success', model=DatasetObject.pending_aibom_list_resp)
    @auth_dataset_review_ns.response(403, 'fail', model=DatasetObject.dataset_review_msg_resp)
    def post(self):
        """
            If the reviewer determines that the AIBOM supplementary information is incomplete and decides to reject the review,
            the status will be reverted from "pending review" back to "pending AIBOM."
            The reviewer can also provide the user with feedback on the specific AIBOM issues related to the dataset.
        """
        hashmap = json.loads(request.data)
        user_id = hashmap.get('user_id', "")
        pending_review_ids = hashmap.get('pending_aibom_review_ids', '')
        rejection_notes = hashmap.get('rejection_notes', "")

        # Execute the specific method, and get the returned dictionary
        response_dict = dataset_review.reject_review(
            user_id, pending_review_ids, rejection_notes)

        # success or fail
        status_code = 200 if response_dict['message'] == 'success' else 403

        model_ret = DatasetObject.pending_aibom_list_resp if status_code == 200 else DatasetObject.dataset_review_msg_resp

        return marshal(response_dict, model_ret), status_code


@auth_dataset_review_ns.route("/submit_review")
class SubmitReview(Resource):
    @auth_dataset_review_ns.expect(DatasetObject.pending_review_list_req)
    @auth_dataset_review_ns.response(200, 'success', model=DatasetObject.dataset_review_msg_resp)
    @auth_dataset_review_ns.response(403, 'fail', model=DatasetObject.pending_review_list_resp)
    def post(self):
        """
            Submit the reviewer's review information to transition the status from "pending_review" to "review_result."
        """
        hashmap = json.loads(request.data)
        pending_review_list = hashmap.get('pending_review_list', '')

        # Execute the specific method, and get the returned dictionary
        dataset_review.save_pending_review_list(
            pending_review_list)  # 在提交前先临时保存
        response_dict = dataset_review.submit_pending_review_list(
            pending_review_list)

        # success or fail
        status_code = 200 if response_dict['message'] == 'success' else 403

        model_ret = DatasetObject.dataset_review_msg_resp if status_code == 200 else DatasetObject.pending_review_list_resp

        return marshal(response_dict, model_ret), status_code


@auth_dataset_review_ns.route("/review_result")
class ReviewResult(Resource):
    @auth_dataset_review_ns.expect(UserObject.AIBOM_user)
    @auth_dataset_review_ns.response(200, 'success', model=DatasetObject.review_result_list_resp)
    @auth_dataset_review_ns.response(403, 'fail', model=DatasetObject.dataset_review_msg_resp)
    def get(self):
        """
            Retrieve all datasets that have been successfully reviewed for the specified user_id. If no user_id is provided,
            retrieve all datasets that have been approved.
        """
        user_id = int(request.args.get('user_id', -1))

        # Execute the specific method, and get the returned dictionary
        response_dict = dataset_review.get_review_result_list(user_id)

        # success or fail
        status_code = 200 if response_dict['message'] == 'success' else 403

        model_ret = DatasetObject.review_result_list_resp if status_code == 200 else DatasetObject.dataset_review_msg_resp

        return marshal(response_dict, model_ret), status_code


@auth_dataset_review_ns.route("/review_result_download")
class ReviewResultDownload(Resource):
    @auth_dataset_review_ns.expect(UserObject.AIBOM_user)
    @auth_dataset_review_ns.response(403, 'fail', model=DatasetObject.dataset_review_msg_resp)
    def post(self):
        """
            Download all datasets that have been successfully reviewed for the specified user_id in CSV format.
            If no user_id is provided, download all datasets that have been approved in CSV format by default.
        """
        user_id = json.loads(request.data).get('user_id', -1)
        user_id = -1 if user_id == "" or user_id is None else user_id

        # Execute the specific method, and get the returned dictionary
        response_dict = dataset_review.get_review_result_list(user_id)

        if response_dict['message'] == 'success':
            response_dict = dataset_review.review_result_download(
                user_id, response_dict['review_result_list'])

        # success or fail
        status_code = 200 if response_dict['message'] == 'success' else 403

        model_ret = DatasetObject.review_result_list_resp if status_code == 200 else DatasetObject.dataset_review_msg_resp

        if status_code == 404:
            return marshal(response_dict, model_ret), status_code
        else:
            res = make_response(send_from_directory(
                response_dict['download_path'], response_dict['file_name'], as_attachment=True))
            res.headers["Cache-Control"] = "no_store"
            res.headers["max-age"] = 1
            return res


@auth_dataset_review_ns.route("/review_result_search_for_name")
class ReviewResultSearchForName(Resource):
    # @auth_dataset_review_ns.expect(UserObject.AIBOM_user)
    @auth_dataset_review_ns.response(403, 'fail', model=DatasetObject.dataset_review_msg_resp)
    def post(self):
        """
            Searching review result by dataset similar name
        """
        # user_id = json.loads(request.data).get('user_id', -1)
        request_body_json = json.loads(request.data)
        dataset_name = request_body_json.get('dataset_name', [""])
        # user_id = -1 if user_id == "" or user_id is None else user_id

        response_dict = dataset_review.get_review_result_list_for_dataset_name(dataset_name)

        status_code = 200 if response_dict['message'] == 'success' else 403

        model_ret = DatasetObject.review_result_list_resp if status_code == 200 else DatasetObject.dataset_review_msg_resp

        return marshal(response_dict, model_ret), status_code
        #
        # if status_code == 404:
        #     return marshal(response_dict, model_ret), status_code
        # else:
        #     res = make_response(send_from_directory(
        #         response_dict['review_result_list'], response_dict['file_name'], as_attachment=True))
        #     res.headers["Cache-Control"] = "no_store"
        #     res.headers["max-age"] = 1
        #     return res


@auth_dataset_review_ns.route("/review_result_cur_row_download")
class ReviewResultDownloadForNames(Resource):
    @auth_dataset_review_ns.response(403, 'fail', model=DatasetObject.dataset_review_msg_resp)
    def post(self):
        """
            Downloading one row review result that is you selected
        """
        # user_id = json.loads(request.data).get('user_id', -1)
        result_id = json.loads(request.data).get('result_id')
        # user_id = -1 if user_id == "" or user_id is None else user_id

        # Execute the specific method, and get the returned dictionary

        response_dict = dataset_review.get_review_result_by_id(result_id)
        if response_dict['message'] == 'success':
            response_dict = dataset_review.review_result_download(
                user_id="", review_result_list=response_dict['review_result_list'])

        # success or fail
        status_code = 200 if response_dict['message'] == 'success' else 403

        model_ret = DatasetObject.review_result_list_resp if status_code == 200 else DatasetObject.dataset_review_msg_resp

        if status_code == 404:
            return marshal(response_dict, model_ret), status_code
        else:
            res = make_response(send_from_directory(
                response_dict['download_path'], response_dict['file_name'], as_attachment=True))
            res.headers["Cache-Control"] = "no_store"
            res.headers["max-age"] = 1
            return res


@auth_dataset_review_ns.route("/review_result_cur_search_download")
class ReviewResultDownloadForNames(Resource):
    @auth_dataset_review_ns.response(403, 'fail', model=DatasetObject.dataset_review_msg_resp)
    def post(self):
        """
            Downloading current search review result by dataset similar name
        """
        # user_id = json.loads(request.data).get('user_id', -1)
        request_body_json = json.loads(request.data)
        dataset_name = request_body_json.get('dataset_name', [""])
        # user_id = -1 if user_id == "" or user_id is None else user_id

        response_dict = dataset_review.get_review_result_list_for_dataset_name(dataset_name)

        status_code = 200 if response_dict['message'] == 'success' else 403

        if response_dict['message'] == 'success':
            response_dict = dataset_review.review_result_download(
                user_id="", review_result_list=response_dict['review_result_list'])

        # success or fail
        status_code = 200 if response_dict['message'] == 'success' else 403

        model_ret = DatasetObject.review_result_list_resp if status_code == 200 else DatasetObject.dataset_review_msg_resp

        if status_code == 404:
            return marshal(response_dict, model_ret), status_code
        else:
            res = make_response(send_from_directory(
                response_dict['download_path'], response_dict['file_name'], as_attachment=True))
            res.headers["Cache-Control"] = "no_store"
            res.headers["max-age"] = 1
            return res


@auth_dataset_review_ns.route("/license_upload_by_file")
class LicenseUploadByFile(Resource):
    @auth_dataset_review_ns.expect(DatasetObject.dataset_license_list_req)
    @auth_dataset_review_ns.response(200, 'success', model=DatasetObject.dataset_review_msg_resp)
    @auth_dataset_review_ns.response(403, 'fail', model=DatasetObject.dataset_license_list_resp)
    def post(self):
        """
             Upload licenses in bulk through files. Existing licenses will not be duplicated and will be placed in the "fail" list,
             while successful uploads will be placed in the "success" list. If all uploads are successful,
             only a success message will be returned.
        """
        user_id = request.form.get("user_id")
        dataset_license_list_req = request.files.get('dataset_license_list')

        dataset_license_list_req = dataset_review.file_convert_license(
            user_id, dataset_license_list_req)

        if dataset_license_list_req['message'] == 'success':
            dataset_license_list = dataset_license_list_req['notification']
            # Execute the specific method, and get the returned dictionary
            response_dict = dataset_review.license_upload(
                user_id, dataset_license_list)
        else:
            response_dict = dataset_license_list_req

        # success or fail
        status_code = 200 if response_dict['message'] == 'success' else 403

        model_ret = DatasetObject.dataset_review_msg_resp if status_code == 200 else DatasetObject.dataset_license_list_resp

        return marshal(response_dict, model_ret), status_code
