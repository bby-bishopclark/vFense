from vFense.core._constants import SortValues
from vFense.core.operations._db_model import AgentOperationKey
from vFense.core.operations._constants import AgentOperations
from vFense.core.operations.search._db_agent_search import FetchAgentOperations
from vFense.search.base import RetrieveBase


class AgentOperationRetriever(RetrieveBase):
    """Retrieve operations, by various filters."""
    def __init__(
            self, sort=SortValues.DESC,
            sort_key=AgentOperationKey.CreatedTime, **kwargs
        ):
        """
        Kwargs:
            sort (str): Sort either by asc or desc.
                default = desc
            sort_key (str): Sort by a valid field.
                examples... operation, status, created_time, updated_time,
                completed_time, and created_by.
                default = created_time

        Basic Usage:
            >>> from vFense.core.operations.search.agent_search import AgentOperationRetriever
            >>> view_name = 'default'
            >>> operation = AgentOperationRetriever(view_name)
        """
        super(AgentOperationRetriever, self).__init__(**kwargs)
        self.sort_key = sort_key
        self.sort = sort
        sort_by_list = (
            [
                AgentOperationKey.Operation,
                AgentOperationKey.OperationStatus,
                AgentOperationKey.CreatedTime,
                AgentOperationKey.UpdatedTime,
                AgentOperationKey.CompletedTime,
                AgentOperationKey.CreatedBy,
                AgentOperationKey.ViewName,
            ]
        )
        if self.sort_key not in sort_by_list:
            self.sort_key = AgentOperationKey.CreatedTime

        self.agent_operations = (
            FetchAgentOperations(
                view_name=self.view_name, count=self.count,
                offset=self.offset, sort=self.sort, sort_key=self.sort_key
            )
        )

    def all(self, conn=None):
        """Get all operations
        Basic Usage:
            >>> from vFense.core.operations.search.agent_search import AgentOperationRetriever
            >>> view_name = 'default'
            >>> operation = AgentOperationRetriever(view_name)
            >>> operation.all()

        Returns:
            Dictionary
            {
                "count": 1,
                "uri": /api/v1/operations,
                "rv_status_code": 1001,
                "http_method": GET,
                "http_status": 200,
                "message": "dataset retrieved",
                "data": [
                    {
                        "agents_expired_count": 0,
                        "agents_total_count": 1,
                        "tag_id": null,
                        "agents_completed_with_errors_count": 0,
                        "created_by": "admin",
                        "agents_pending_pickup_count": 0,
                        "completed_time": 1398092303,
                        "operation_status": 6006,
                        "agents_completed_count": 1,
                        "operation_id": "6c0209d5-b350-48b7-808a-158ddacb6940",
                        "created_time": 1398092302,
                        "agents_pending_results_count": 0,
                        "operation": "install_os_apps",
                        "updated_time": 1398092303,
                        "agents_failed_count": 0,
                        "view_name": "default"
                    }
                ]
            }
        """
        count, data = self.agent_operations.all()
        return self._base(count, data)

    def by_agentid(self, agent_id, conn=None):
        """ Get all operations by agent id
        Args:
            agent_id (str) 36 character uuid

        Basic Usage:
            >>> from vFense.core.operations.search.agent_search import AgentOperationRetriever
            >>> view_name = 'default'
            >>> operation = AgentOperationRetriever(view_name)
            >>> agent_id = '33ba8521-b2e5-47dc-9bdc-0f1e3384049d'
            >>> operation.by_agentid(agent_id)

        Returns:
            Dictionary
            {
                "count": 1,
                "uri": /api/v1/operations,
                "rv_status_code": 1001,
                "http_method": GET,
                "http_status": 200,
                "message": "dataset retrieved",
                "data": [
                    {
                        "agents_expired_count": 0,
                        "created_time": 1398126651,
                        "agents_pending_results_count": 0,
                        "operation": "install_os_apps",
                        "net_throttle": 0,
                        "view_name": "default",
                        "cpu_throttle": "normal",
                        "agents_total_count": 1,
                        "agents_completed_with_errors_count": 0,
                        "action_performed_on": "agent",
                        "agent_ids": [
                            "33ba8521-b2e5-47dc-9bdc-0f1e3384049d"
                        ],
                        "created_by": "admin",
                        "tag_id": null,
                        "completed_time": 0,
                        "agents_completed_count": 0,
                        "agents_pending_pickup_count": 1,
                        "restart": "none",
                        "plugin": "rv",
                        "updated_time": 1398126651,
                        "operation_status": 6009,
                        "operation_id": "267486ef-850f-47e7-a0c4-0da5d5a38efb",
                        "agents_failed_count": 0
                    }
                ]
            }
        """
        count, data = self.agent_operations.by_agentid(agent_id)
        return self._base(count, data)

    def by_tagid(self, tag_id, conn=None):
        """Get all operations by tag id
        Args:
            tag_id (str) 36 character uuid

        Basic Usage:
            >>> from vFense.core.operations.search.agent_search import AgentOperationRetriever
            >>> view_name = 'default'
            >>> operation = AgentOperationRetriever(view_name)
            >>> tag_id = '78076908-e93f-4116-8d49-ad42b4ad0297'
            >>> operation.by_tagid(tag_id)
        Returns:
            Dictionary
            {
                "count": 1,
                "uri": null,
                "rv_status_code": 1001,
                "http_method": null,
                "http_status": 200,
                "message": "dataset retrieved",
                "data": [
                    {
                        "agents_expired_count": 0,
                        "agents_total_count": 2,
                        "tag_id": "78076908-e93f-4116-8d49-ad42b4ad0297",
                        "agents_completed_with_errors_count": 0,
                        "created_by": "admin",
                        "agents_pending_pickup_count": 1,
                        "completed_time": 1398110835,
                        "operation_status": 6009,
                        "agents_completed_count": 1,
                        "operation_id": "d6956a46-165f-49b6-a3df-872a1453ab88",
                        "created_time": 1398110770,
                        "agents_pending_results_count": 0,
                        "operation": "install_os_apps",
                        "updated_time": 1398110835,
                        "agents_failed_count": 0,
                        "view_name": "default"
                    }
                ]
            }
        """
        count, data = self.agent_operations.by_tagid(tag_id)
        return self._base(count, data)

    def by_operation(self, action):
        """Get all operations by operation
        Args:
            action (str) The action the operation will perform.
                examples... reboot, shutdown, install_os_apps

        Basic Usage:
            >>> from vFense.core.operations.search.agent_search import AgentOperationRetriever
            >>> view_name = 'default'
            >>> operation = AgentOperationRetriever(view_name)
            >>> action = 'install_os_apps'
            >>> operation.get_all_by_operation(action)
        Returns:
            Dictionary
            {
                "count": 1,
                "uri": null,
                "rv_status_code": 1001,
                "http_method": null,
                "http_status": 200,
                "message": "dataset retrieved",
                "data": [
                    {
                        "agents_expired_count": 0,
                        "created_time": 1398126651,
                        "agents_pending_results_count": 0,
                        "operation": "install_os_apps",
                        "net_throttle": 0,
                        "view_name": "default",
                        "cpu_throttle": "normal",
                        "agents_total_count": 1,
                        "agents_completed_with_errors_count": 0,
                        "action_performed_on": "agent",
                        "agent_ids": [
                            "33ba8521-b2e5-47dc-9bdc-0f1e3384049d"
                        ],
                        "created_by": "admin",
                        "tag_id": null,
                        "completed_time": 0,
                        "agents_completed_count": 0,
                        "agents_pending_pickup_count": 1,
                        "restart": "none",
                        "plugin": "rv",
                        "updated_time": 1398126651,
                        "operation_status": 6009,
                        "operation_id": "267486ef-850f-47e7-a0c4-0da5d5a38efb",
                        "agents_failed_count": 0
                    }
                ]
            }
        """
        if action in AgentOperations.get_valid_operations():
            count, data = (
                self.agent_operations.by_operation(action)
            )
            return self._base(count, data)

        else:
            return self._set_results_invalid_filter_key(action)

    def install_operation_by_id(self, operation_id, conn=None):
        """Get install operation by operation id
        Args:
            operation_id (str) 36 character UUID.

        Basic Usage:
            >>> from vFense.core.operations.search.agent_search import AgentOperationRetriever
            >>> view_name = 'default'
            >>> operation = AgentOperationRetriever(view_name)
            >>> operation_id = 'd6956a46-165f-49b6-a3df-872a1453ab88'
            >>> operation.install_operation_by_id(operation_id)

        Returns:
            Dictionary
            {
                "count": 1,
                "uri": "/api/v1/operation/48854d9d-a705-45d2-bab6-a448bc75f7d2",
                "rv_status_code": 1001,
                "http_method": "GET",
                "http_status": 200,
                "message": "dataset retrieved",
                "data": {
                    "agents_expired_count": 0,
                    "agents": [
                        {
                            "status": 6502,
                            "picked_up_time": 1398118321,
                            "errors": null,
                            "display_name": null,
                            "apps_failed_count": 0,
                            "apps_completed_count": 1,
                            "completed_time": 1398118775,
                            "applications": [
                                {
                                    "errors": null,
                                    "app_name": "libssl1.0.0",
                                    "results": 6002,
                                    "app_id": "c5fc13cb20b231eb03b225cc0cb1371240450afaf151ed63ef12df77766ca1cf",
                                    "apps_removed": [
                                        {
                                            "version": "1.0.1-4ubuntu5.10",
                                            "name": "libssl1.0.0"
                                        }
                                    ],
                                    "app_version": "1.0.1-4ubuntu5.12",
                                    "results_received_time": 1398118775
                                }
                            ],
                            "apps_pending_count": 0,
                            "agent_id": "33ba8521-b2e5-47dc-9bdc-0f1e3384049d",
                            "computer_name": "ubuntu",
                            "apps_total_count": 1,
                            "operation_id": "48854d9d-a705-45d2-bab6-a448bc75f7d2",
                            "expired_time": 0
                        }
                    ],
                    "created_time": 1398118321,
                    "agents_pending_results_count": 0,
                    "operation": "install_os_apps",
                    "net_throttle": 0,
                    "view_name": "default",
                    "cpu_throttle": "normal",
                    "agents_total_count": 1,
                    "agents_completed_with_errors_count": 0,
                    "action_performed_on": "agent",
                    "agent_ids": [
                        "33ba8521-b2e5-47dc-9bdc-0f1e3384049d"
                    ],
                    "created_by": "admin",
                    "tag_id": null,
                    "completed_time": 1398118775,
                    "agents_completed_count": 1,
                    "agents_pending_pickup_count": 0,
                    "restart": "none",
                    "plugin": "rv",
                    "updated_time": 1398118775,
                    "operation_status": 6006,
                    "operation_id": "48854d9d-a705-45d2-bab6-a448bc75f7d2",
                    "agents_failed_count": 0
                }
            }
        """
        count, data = (
            self.agent_operations.install_operation_by_id(operation_id)
        )
        return self._base(count, data)

    def by_id(self, operation_id, conn=None):
        """Get operation by operation id
        Args:
            operation_id (str) 36 character UUID.

        Basic Usage:
            >>> from vFense.core.operations.search.agent_search import AgentOperationRetriever
            >>> view_name = 'default'
            >>> operation = AgentOperationRetriever(view_name)
            >>> operation_id = 'd6956a46-165f-49b6-a3df-872a1453ab88'
            >>> operation.by_id(operation_id)

        Returns:
            Dictionary
            {
                "count": 1,
                "uri": "/api/v1/operation/58d37cf8-c1a9-460d-a7c6-0c8f896970b4",
                "rv_status_code": 1001,
                "http_method": "GET",
                "http_status": 200,
                "message": "dataset retrieved",
                "data": {
                    "agents_expired_count": 0,
                    "agents": [
                        {
                            "status": 6501,
                            "picked_up_time": 0,
                            "errors": null,
                            "display_name": null,
                            "expired_time": 0,
                            "completed_time": 0,
                            "agent_id": "33ba8521-b2e5-47dc-9bdc-0f1e3384049d",
                            "computer_name": "ubuntu",
                        }
                    ],
                    "created_time": 1398110770,
                    "agents_pending_results_count": 0,
                    "operation": "updatesapplications",
                    "net_throttle": null,
                    "view_name": "default",
                    "cpu_throttle": null,
                    "agents_total_count": 1,
                    "agents_completed_with_errors_count": 0,
                    "action_performed_on": "agent",
                    "created_by": "admin",
                    "tag_id": null,
                    "completed_time": 0,
                    "agents_completed_count": 0,
                    "agents_pending_pickup_count": 1,
                    "restart": null,
                    "plugin": "rv",
                    "updated_time": 1398110770,
                    "operation_status": 6009,
                    "operation_id": "58d37cf8-c1a9-460d-a7c6-0c8f896970b4",
                    "agents_failed_count": 0
                }
            }
        """
        count, data = (
            self.agent_operations.by_id(operation_id)
        )
        return self._base(count, data)

    def get_install_operation_for_email_alert(self, operation_id):
        count, data = (
            self.agent_operations.fetch_install_operation_for_email_alert(
                operation_id
            )
        )

        return data

    def get_operation_for_email_alert(self, operation_id):
        count, data = (
            self.agent_operations.fetch_operation_for_email_alert(
                operation_id
            )
        )

        return data