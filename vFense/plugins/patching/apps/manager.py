import os
import logging
from time import time

from vFense import VFENSE_LOGGING_CONFIG, VFENSE_APP_TMP_PATH
from vFense.plugins.patching import Apps, Files
from vFense.plugins.patching._constants import AppStatuses
from vFense.plugins.patching._db_model import (
    AppCollections, DbCommonAppKeys
)
from vFense.core.agent._db import(
    fetch_agent_ids_in_views
)
from vFense.core.agent import Agent
from vFense.core.agent.manager import AgentManager
from vFense.core._db import insert_data_in_table
from vFense.core.status_codes import DbCodes
from vFense.core.results import ApiResultKeys
from vFense.core.view._db_model import ViewKeys
from vFense.core.view.manager import ViewManager
from vFense.plugins.patching.status_codes import (
    PackageCodes, PackageFailureCodes
)
from vFense.plugins.patching.file_data import add_file_data

from vFense.plugins.patching._db import (
    fetch_app_data, fetch_apps_data_by_os_code, insert_app_data,
    delete_apps_per_agent_older_than
)

from vFense.plugins.patching.downloader.downloader import (
    download_all_files_in_app
)


import redis
from rq import Queue

RQ_HOST = 'localhost'
RQ_PORT = 6379
RQ_DB = 0
RQ_PKG_POOL = redis.StrictRedis(host=RQ_HOST, port=RQ_PORT, db=RQ_DB)

logging.config.fileConfig(VFENSE_LOGGING_CONFIG)
logger = logging.getLogger('rvapi')

class AppsManager(object):
    def __init__(self):
        self.apps_collection = AppCollections.CustomApps
        self.apps_per_agent_collection = AppCollections.AppsPerAgent

    def url_path(self, app_id, app_name, view):
        view = ViewManager(view)
        tmp_url = (
            os.path.join(
                view.get_attribute(ViewKeys.PackageUrl),
                app_id, app_name
            )
        )
        return tmp_url

    def url_tmp_path(self, app_id, app_name, view):
        view = ViewManager(view)
        tmp_url = (
            os.path.join(
                view.get_attribute(ViewKeys.PackageUrl),
                'tmp', app_id, app_name
            )
        )
        return tmp_url

    def local_file_path(self, uuid, app_name):
        return os.path.join(VFENSE_APP_TMP_PATH, uuid, app_name)


    def get_apps(self, app_id=None, os_code=None, views=None):
        if os_code and views and not app_id:
            apps_info = (
                fetch_apps_data_by_os_code(
                    os_code, views,
                    collection=self.apps_collection
                )
            )

        elif app_id and not os_code and not views:
            apps_info = (
                fetch_app_data(app_id, collection=self.apps_collection)
            )

        return apps_info

    def get_agent_ids(self, os_code, views):
        agent_ids = (
            fetch_agent_ids_in_views(
                views=views, os_code=os_code
            )
        )

        return agent_ids


    def store_app_in_db(self, app, file_data, views=None):
        """Store the application into the vFense database.
        Args:
            apps (Apps): The App instance that contains all the application
                data.

        Kwargs:
            file_data (list): List of Files instances that contains all the
                file related data.
            views (list): List of views, you want this application to be made
                available.

        Basic Usage:
            >>> from vFense.plugins.patching.uploader.uploader import UploadManager
            >>> from vFense.plugins.patching import Apps, Files


        Returns:
        """
        results = {}
        if isinstance(app, Apps) and isinstance(file_data, list):
            app_invalid_fields = app.get_invalid_fields()
            if not app_invalid_fields:
                app.fill_in_defaults()
                object_status, _, _, _ = (
                    insert_app_data(
                        app.to_dict_db_apps(), self.apps_collection
                    )
                )
                self.store_file_data_in_db(file_data)
                if app.status == AppStatuses.AVAILABLE:
                    self.download_app_files(app, file_data)

                if (object_status == DbCodes.Inserted or
                        object_status == DbCodes.Replaced or
                        object_status == DbCodes.Unchanged):
                    msg = 'App %s stored succesfully' % (app.name)
                    results[ApiResultKeys.GENERIC_STATUS_CODE] = (
                        PackageCodes.ObjectCreated
                    )
                    results[ApiResultKeys.VFENSE_STATUS_CODE] = (
                        PackageCodes.FileUploadedSuccessfully
                    )
                    results[ApiResultKeys.MESSAGE] = msg
                    results[ApiResultKeys.DATA] = [app.to_dict_apps()]

                else:
                    msg = 'Failed to add app %s' % (app.name)
                    results[ApiResultKeys.GENERIC_STATUS_CODE] = (
                        PackageFailureCodes.FailedToCreateObject
                    )
                    results[ApiResultKeys.VFENSE_STATUS_CODE] = (
                        PackageFailureCodes.FileUploadFailed
                    )
                    results[ApiResultKeys.MESSAGE] = msg
                    results[ApiResultKeys.DATA] = [app.to_dict_apps()]

            else:
                msg = (
                    'Failed to add {0}, contained invalid_fields {1}'
                    .format(app.name, ', '.join(app_invalid_fields))
                )
                results[ApiResultKeys.ERRORS] = app_invalid_fields
                results[ApiResultKeys.GENERIC_STATUS_CODE] = (
                    PackageFailureCodes.FailedToCreateObject
                )
                results[ApiResultKeys.VFENSE_STATUS_CODE] = (
                    PackageFailureCodes.FileUploadFailed
                )
                results[ApiResultKeys.MESSAGE] = msg
                results[ApiResultKeys.DATA] = [app.to_dict_apps()]

        else:
            msg = (
                'Not a valid Apps {0} or Files {1} instance'
                .format(type(app), type(file_data))
            )
            results[ApiResultKeys.GENERIC_STATUS_CODE] = (
                    PackageFailureCodes.FailedToCreateObject
            )
            results[ApiResultKeys.VFENSE_STATUS_CODE] = (
                    PackageFailureCodes.FileUploadFailed
            )
            results[ApiResultKeys.MESSAGE] = msg
            results[ApiResultKeys.DATA] = []

        return results

    def add_app_to_agent(self, app):
        if isinstance(app, Apps):
            invalid_keys = app.get_invalid_fields()
            if not invalid_keys:
                pass


    def add_apps_to_agent(self, agent_id, app_list, now=None,
                          delete_afterwards=True):

        updated = 0
        inserted = 0
        deleted = 0
        apps_to_insert = []
        if isinstance(app_list, list):
            for app in app_list:
                if not now:
                    now = time()

                app.last_modified_time = now
                if isinstance(app, Apps):
                    apps_to_insert.append(app.to_dict_db_apps_per_agent())

        if apps_to_insert:
            status_code, count, _, _ = (
                insert_data_in_table(apps_to_insert, self.apps_collection)
            )

            if isinstance(count, list):
                if len(count) > 1:
                    inserted = count[0]
                    updated = count[1]

            else:
                if status_code == DbCodes.Replaced:
                    updated = count
                elif status_code == DbCodes.Inserted:
                    inserted = count

            status_code, count, _, _ = (
                delete_apps_per_agent_older_than(
                    agent_id, now, self.apps_collection)
            )

            deleted = count

        return inserted, updated, deleted

    def store_file_data_in_db(self, file_data):
        """Store the uploaded application into the vFense database.
        Args:
            file_data (list): List of Files instances that contains all the
                file related data.
        """
        data_stored = False
        if isinstance(file_data, list):
            data_to_insert = []
            for data in file_data:
                if isinstance(data, Files):
                    if not data.get_invalid_fields():
                        data_to_insert.append(data)

            if data_to_insert:
                data_stored = add_file_data(file_data)

        return data_stored

    def download_app_files(self, app, file_data):

        rv_q = Queue('downloader', connection=RQ_PKG_POOL)
        rv_q.enqueue_call(
            func=download_all_files_in_app,
            args=(app, file_data, 0, self.apps_collection),
            timeout=86400
        )


def incoming_applications_from_agent(agent_id, apps, delete_afterwards=True):

    manager = AppsManager()
    apps_data = []
    now = time()
    agent = AgentManager(agent_id)
    if isinstance(apps, list):
        for app in apps:
            files_data = []
            files = app.pop(DbCommonAppKeys.FileData)
            app.views = agent.views
            app_data = Apps(**app)
            if isinstance(files, list):
                for file_data in files:
                    files_data.append(Files(**file_data))

            apps_data.append(Apps(app_data))
            manager.store_app_in_db(app_data, files_data)

        manager.add_apps_to_agent(agent_id, apps_data, now, delete_afterwards)