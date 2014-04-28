import logging
import logging.config
from vFense.utils.common import *
from vFense.plugins.patching.operations.patching_operations import \
    PatchingOperation
from vFense.operations._constants import AgentOperations, vFensePlugins, \
    vFenseObjects
from vFense.operations.store_agent_operation import StoreAgentOperation
from vFense.operations import *
from vFense.core.agent import *
from vFense.core.decorators import results_message
from vFense.core._constants import CPUThrottleValues, RebootValues
from vFense.plugins.patching.rv_db_calls import *
from vFense.plugins.patching import *
from vFense.core.tag.tagManager import *
from vFense.errorz._constants import ApiResultKeys
from vFense.errorz.status_codes import GenericCodes, AgentOperationCodes, \
    GenericFailureCodes, AgentOperationFailureCodes

logging.config.fileConfig('/opt/TopPatch/conf/logging.config')
logger = logging.getLogger('rvapi')


class StorePatchingOperation(StoreAgentOperation):
    """Create operations for the patching plugin"""
    def apps_refresh(self, agentids=None, tag_id=None):
        """Send the apps_refresh operation to the agent,
            Send all installed applications and updates needed
            to the server.
        Kwargs:
            agentids (str): List of agent ids.
                default = None
            tag_id (str): 36 character UUID of the agent.
                default = None

        Basic Usage:
            >>> from vFense.plugins.patching.operations.store_operations import StorePatchingOperation
            >>> agentids = ['e9a8871a-5ae8-40fb-9316-b0918947f736']
            >>> username = 'admin'
            >>> customer_name = 'default'
            >>> uri = '/api/v1/agent/e9a8871a-5ae8-40fb-9316-b0918947f736/apps/os'
            >>> method = 'PUT'
            >>> operation = StorePatchingOperation(username, customer_name, uri, method)
            >>> operation.apps_refresh(agentids=agentids)

        Returns:
        """
        results = (
            self.generic_operation(
                AgentOperations.REFRESH_APPS,
                vFensePlugins.RV_PLUGIN,
                agentids, tag_id
            )
        )

        return(results)

    def uninstall_agent(self, agent_id):
        operation_data = {
            AgentOperationKey.Operation: AgentOperations.UNINSTALL,
            AgentOperationKey.Plugin: vFensePlugins.RV_PLUGIN,
            OperationPerAgentKey.AgentId: agent_id,
        }
        self._store_in_agent_queue(operation_data)

    def install_os_apps(
        self, appids, cpu_throttle=CPUThrottleValues.NORMAL,
        net_throttle=0, restart=RebootValues.NONE,
        agentids=None, tag_id=None):
        """Send the install_os_apps operation to the agent,
            This will install a list of applications on n
            number of agents or tag id.
        Args:
            appids (list): List of the application ids,
                that you want to install.

        Kwargs:
            cpu_throttle (str): Throttle how much cpu to use while installing
                the applications.
                default = normal
            net_throttle (int): Throttle how much bandwidth is being used,
                while the agent is downloading the applications.
                default = 0 (unlimited)
            restart (str): Choose if you want to restart the system after
                the application is installed. Examples (none, needed, forced)
                default = 'none' (do not reboot)
            agentids (str): List of agent ids.
                default = None
            tag_id (str): 36 character UUID of the agent.
                default = None

        Basic Usage:
            >>> from vFense.plugins.patching.operations.store_operations import StorePatchingOperation
            >>> username = 'admin'
            >>> customer_name = 'default'
            >>> uri = '/api/v1/agent/e9a8871a-5ae8-40fb-9316-b0918947f736/apps/os'
            >>> method = 'PUT'
            >>> appids = ['000bd2abd0f5197612dad031eb5d04abc082aba1b904b801c7b2d7925ac248a3']
            >>> reboot = 'needed'
            >>> cpu = 'high'
            >>> net = 100
            >>> agentids = ['e9a8871a-5ae8-40fb-9316-b0918947f736']
            >>> operation = StorePatchingOperation(username, customer_name, uri, method)
            >>> operation.install_os_apps(
                    appids, cpu_throttle=cpu, net_throttle=net,
                    restart=reboot, agentids=agentids
                )

        Returns:
        """

        oper_type = AgentOperations.INSTALL_OS_APPS
        oper_plugin = vFensePlugins.RV_PLUGIN

        self.CurrentAppsCollection = AppCollections.UniqueApplications
        self.CurrentAppsKey = AppsKey
        self.CurrentAppsPerAgentCollection = AppCollections.AppsPerAgent
        self.CurrentAppsPerAgentKey = AppsPerAgentKey

        return(
            self.install_apps(
                oper_type, oper_plugin, appids,
                cpu_throttle, net_throttle,
                restart, agentids, tag_id
            )
        )

    def install_custom_apps(
        self, appids, cpu_throttle=CPUThrottleValues.NORMAL,
        net_throttle=0, restart=RebootValues.NONE,
        agentids=None, tag_id=None
        ):
        """Send the install_custom_apps operation to the agent,
            This will install a list of applications on n
            number of agents or tag id.
        Args:
            appids (list): List of the application ids,
                that you want to install.

        Kwargs:
            cpu_throttle (str): Throttle how much cpu to use while installing
                the applications.
                default = normal
            net_throttle (int): Throttle how much bandwidth is being used,
                while the agent is downloading the applications.
                default = 0 (unlimited)
            restart (str): Choose if you want to restart the system after
                the application is installed. Examples (none, needed, forced)
                default = 'none' (do not reboot)
            agentids (str): List of agent ids.
                default = None
            tag_id (str): 36 character UUID of the agent.
                default = None

        Basic Usage:
            >>> from vFense.plugins.patching.operations.store_operations import StorePatchingOperation
            >>> username = 'admin'
            >>> customer_name = 'default'
            >>> uri = '/api/v1/agent/e9a8871a-5ae8-40fb-9316-b0918947f736/apps/custom'
            >>> method = 'PUT'
            >>> appids = ['000bd2abd0f5197612dad031eb5d04abc082aba1b904b801c7b2d7925ac248a3']
            >>> reboot = 'needed'
            >>> cpu = 'high'
            >>> net = 100
            >>> agentids = ['e9a8871a-5ae8-40fb-9316-b0918947f736']
            >>> operation = StorePatchingOperation(username, customer_name, uri, method)
            >>> operation.install_custom_apps(
                    appids, cpu_throttle=cpu, net_throttle=net,
                    restart=reboot, agentids=agentids
                )
        """

        oper_type = AgentOperations.INSTALL_CUSTOM_APPS
        oper_plugin = vFensePlugins.RV_PLUGIN

        self.CurrentAppsCollection = AppCollections.CustomApps
        self.CurrentAppsKey = CustomAppsKey
        self.CurrentAppsPerAgentCollection = AppCollections.CustomAppsPerAgent
        self.CurrentAppsPerAgentKey = CustomAppsPerAgentKey

        return(
            self.install_apps(
                oper_type, oper_plugin, appids,
                cpu_throttle, net_throttle,
                restart, agentids, tag_id
            )
        )


    def install_supported_apps(
        self, appids, cpu_throttle=CPUThrottleValues.NORMAL,
        net_throttle=0, restart=RebootValues.NONE,
        agentids=None, tag_id=None
        ):
        """Send the install_supported_apps operation to the agent,
            This will install a list of supported applications on n
            number of agents or tag id.
        Args:
            appids (list): List of the application ids,
                that you want to install.

        Kwargs:
            cpu_throttle (str): Throttle how much cpu to use while installing
                the applications.
                default = normal
            net_throttle (int): Throttle how much bandwidth is being used,
                while the agent is downloading the applications.
                default = 0 (unlimited)
            restart (str): Choose if you want to restart the system after
                the application is installed. Examples (none, needed, forced)
                default = 'none' (do not reboot)
            agentids (str): List of agent ids.
                default = None
            tag_id (str): 36 character UUID of the agent.
                default = None

        Basic Usage:
            >>> from vFense.plugins.patching.operations.store_operations import StorePatchingOperation
            >>> username = 'admin'
            >>> customer_name = 'default'
            >>> uri = '/api/v1/agent/e9a8871a-5ae8-40fb-9316-b0918947f736/apps/supported'
            >>> method = 'PUT'
            >>> appids = ['000bd2abd0f5197612dad031eb5d04abc082aba1b904b801c7b2d7925ac248a3']
            >>> reboot = 'needed'
            >>> cpu = 'high'
            >>> net = 100
            >>> agentids = ['e9a8871a-5ae8-40fb-9316-b0918947f736']
            >>> operation = StorePatchingOperation(username, customer_name, uri, method)
            >>> operation.install_supported_apps(
                    appids, cpu_throttle=cpu, net_throttle=net,
                    restart=reboot, agentids=agentids
                )
        """

        oper_type = AgentOperations.INSTALL_SUPPORTED_APPS
        oper_plugin = vFensePlugins.RV_PLUGIN

        self.CurrentAppsCollection = AppCollections.SupportedApps
        self.CurrentAppsKey = SupportedAppsKey
        self.CurrentAppsPerAgentCollection = AppCollections.SupportedAppsPerAgent
        self.CurrentAppsPerAgentKey = SupportedAppsPerAgentKey

        return(
            self.install_apps(
                oper_type, oper_plugin, appids,
                cpu_throttle, net_throttle,
                restart, agentids, tag_id
            )
        )

    def install_agent_apps(
        self, appids, cpu_throttle=CPUThrottleValues.NORMAL,
        net_throttle=0, restart=RebootValues.NONE,
        agentids=None, tag_id=None
        ):
        """Send the install_agent_apps operation to the agent,
            This will install the agent update on n
            number of agents or tag id.
        Args:
            appids (list): List of the application ids,
                that you want to install.

        Kwargs:
            cpu_throttle (str): Throttle how much cpu to use while installing
                the applications.
                default = normal
            net_throttle (int): Throttle how much bandwidth is being used,
                while the agent is downloading the applications.
                default = 0 (unlimited)
            restart (str): Choose if you want to restart the system after
                the application is installed. Examples (none, needed, forced)
                default = 'none' (do not reboot)
            agentids (str): List of agent ids.
                default = None
            tag_id (str): 36 character UUID of the agent.
                default = None

        Basic Usage:
            >>> from vFense.plugins.patching.operations.store_operations import StorePatchingOperation
            >>> username = 'admin'
            >>> customer_name = 'default'
            >>> uri = '/api/v1/agent/e9a8871a-5ae8-40fb-9316-b0918947f736/apps/agent'
            >>> method = 'PUT'
            >>> appids = ['000bd2abd0f5197612dad031eb5d04abc082aba1b904b801c7b2d7925ac248a3']
            >>> reboot = 'needed'
            >>> cpu = 'high'
            >>> net = 100
            >>> agentids = ['e9a8871a-5ae8-40fb-9316-b0918947f736']
            >>> operation = StorePatchingOperation(username, customer_name, uri, method)
            >>> operation.install_agent_apps(
                    appids, cpu_throttle=cpu, net_throttle=net,
                    restart=reboot, agentids=agentids
                )
        """

        oper_type = AgentOperations.INSTALL_AGENT_APPS
        oper_plugin = vFensePlugins.RV_PLUGIN

        self.CurrentAppsCollection = AppCollections.AgentApps
        self.CurrentAppsKey = AgentAppsKey
        self.CurrentAppsPerAgentCollection = AppCollections.AgentAppsPerAgent
        self.CurrentAppsPerAgentKey = AgentAppsPerAgentKey

        return(
            self.install_apps(
                oper_type, oper_plugin, appids,
                cpu_throttle, net_throttle,
                restart, agentids, tag_id
            )
        )


    def uninstall_apps(
        self, appids, cpu_throttle=CPUThrottleValues.NORMAL,
        net_throttle=0, restart=RebootValues.NONE,
        agentids=None, tag_id=None
        ):
        """Send the uninstall_apps operation to the agent,
            This will uninstall the applications from n
            number of agents or tag id.
        Args:
            appids (list): List of the application ids,
                that you want to install.

        Kwargs:
            cpu_throttle (str): Throttle how much cpu to use while installing
                the applications.
                default = normal
            net_throttle (int): Throttle how much bandwidth is being used,
                while the agent is downloading the applications.
                default = 0 (unlimited)
            restart (str): Choose if you want to restart the system after
                the application is installed. Examples (none, needed, forced)
                default = 'none' (do not reboot)
            agentids (str): List of agent ids.
                default = None
            tag_id (str): 36 character UUID of the agent.
                default = None

        Basic Usage:
            >>> from vFense.plugins.patching.operations.store_operations import StorePatchingOperation
            >>> username = 'admin'
            >>> customer_name = 'default'
            >>> uri = '/api/v1/agent/e9a8871a-5ae8-40fb-9316-b0918947f736/apps/agent'
            >>> method = 'PUT'
            >>> appids = ['000bd2abd0f5197612dad031eb5d04abc082aba1b904b801c7b2d7925ac248a3']
            >>> reboot = 'needed'
            >>> cpu = 'high'
            >>> net = 100
            >>> agentids = ['e9a8871a-5ae8-40fb-9316-b0918947f736']
            >>> operation = StorePatchingOperation(username, customer_name, uri, method)
            >>> operation.uninstall_apps(
                    appids, cpu_throttle=cpu, net_throttle=net,
                    restart=reboot, agentids=agentids
                )
        """

        oper_type = AgentOperations.UNINSTALL
        oper_plugin = vFensePlugins.RV_PLUGIN

        self.CurrentAppsCollection = AppCollections.UniqueApplications
        self.CurrentAppsKey = AppsKey
        self.CurrentAppsPerAgentCollection = AppCollections.AppsPerAgent
        self.CurrentAppsPerAgentKey = AppsPerAgentKey

        return(
            self.install_apps(
                oper_type, oper_plugin, appids,
                cpu_throttle, net_throttle,
                restart, agentids, tag_id
            )
        )


    @results_message
    def install_apps(
        self, oper_type, oper_plugin,
        appids, cpu_throttle=CPUThrottleValues.NORMAL,
        net_throttle=0, restart=RebootValues.NONE,
        agentids=None, tag_id=None
        ):

        results = {
            ApiResultKeys.DATA: [],
            ApiResultKeys.USERNAME: self.username,
            ApiResultKeys.URI: self.uri,
            ApiResultKeys.HTTP_METHOD: self.method
        }
    
        performed_on = vFenseObjects.AGENT
        if tag_id:
            performed_on = vFenseObjects.TAG
            if not agentids:
                agentids = get_agent_ids_from_tag(tag_id)
            else:
                agentids += get_agent_ids_from_tag(tag_id)

        operation = (
            PatchingOperation(
                self.username, self.customer_name,
            )
        )

        operation_id = (
            operation.create_operation(
                oper_type, oper_plugin, agentids,
                tag_id, cpu_throttle,
                net_throttle, restart,
                performed_on=performed_on
            )
        )
        if operation_id:
            msg = 'operation created'
            status_code = GenericCodes.ObjectCreated
            vfense_status_code = AgentOperationCodes.Created
            results[ApiResultKeys.GENERATED_IDS] = [operation_id]
            results[ApiResultKeys.GENERIC_STATUS_CODE] = status_code
            results[ApiResultKeys.VFENSE_STATUS_CODE] = vfense_status_code
            results[ApiResultKeys.MESSAGE] = msg
            for agent_id in agentids:
                valid_appids = (
                    self._return_valid_app_ids_for_agent(
                        agent_id, appids, table=self.CurrentAppsPerAgentCollection
                    )
                )

                pkg_data = []
                for app_id in valid_appids:
                    data_to_update = (
                        {
                            self.CurrentAppsPerAgentKey.Status: PENDING
                        }
                    )
                    if (oper_type == AgentOperations.INSTALL_OS_APPS or
                            oper_type == AgentOperations.UNINSTALL):
                        update_os_app_per_agent(agent_id, app_id, data_to_update)

                    elif oper_type == AgentOperations.INSTALL_CUSTOM_APPS:
                        update_custom_app_per_agent(agent_id, app_id, data_to_update)

                    elif oper_type == AgentOperations.INSTALL_SUPPORTED_APPS:
                        update_supported_app_per_agent(agent_id, app_id, data_to_update)

                    elif oper_type == AgentOperations.INSTALL_AGENT_APPS:
                        update_agent_app_per_agent(agent_id, app_id, data_to_update)

                    pkg_data.append(
                        self._get_apps_data(
                            app_id, agent_id, oper_type,
                            self.CurrentAppsCollection,
                            self.CurrentAppsKey.AppId
                        )
                    )

                operation_data = {
                    AgentOperationKey.Operation: oper_type,
                    AgentOperationKey.OperationId: operation_id,
                    AgentOperationKey.Plugin: oper_plugin,
                    AgentOperationKey.Restart: restart,
                    PKG_FILEDATA: pkg_data,
                    OperationPerAgentKey.AgentId: agent_id,
                    AgentOperationKey.CpuThrottle: cpu_throttle,
                    AgentOperationKey.NetThrottle: net_throttle,
                }
                self._store_in_agent_queue(operation_data)
                operation.add_agent_to_install_operation(agent_id, operation_id, pkg_data)

        else:
            msg = 'operation failed to create'
            status_code = GenericFailureCodes.FailedToCreateObject
            vfense_status_code = AgentOperationFailureCodes.FailedToCreateOperation
            results[ApiResultKeys.GENERATED_IDS] = [operation_id],
            results[ApiResultKeys.GENERIC_STATUS_CODE] = status_code
            results[ApiResultKeys.VFENSE_STATUS_CODE] = vfense_status_code
            results[ApiResultKeys.MESSAGE] = msg

        return(results)

    def _get_apps_data(self, app_id, agent_id, oper_type,
                       table=AppsCollection, app_key=AppsKey.AppId):

        if oper_type == AgentOperations.INSTALL_OS_APPS:
            pkg = (
                get_app_data(
                    app_id, table, app_key,
                    fields_to_pluck=[AppsKey.Name, AppsKey.Version]
                )
            )
            pkg[PKG_FILEDATA] = get_file_data(app_id, agent_id)

            if pkg:
                uris = (
                    get_download_urls(
                        self.customer_name, app_id, pkg[PKG_FILEDATA]
                    )
                )

                pkg_data = {
                    APP_NAME: pkg[AppsKey.Name],
                    APP_VERSION: pkg[AppsKey.Version],
                    APP_URIS: uris,
                    APP_ID: app_id
                }

        elif oper_type == AgentOperations.UNINSTALL:
            pkg = (
                get_app_data(
                    app_id, table, app_key,
                    fields_to_pluck=[AppsKey.Name, AppsKey.Version]
                )
            )
            pkg_data = (
                {
                    APP_NAME: pkg[AppsKey.Name],
                    APP_VERSION: pkg[AppsKey.Version],
                    APP_ID: app_id
                }
            )

        elif oper_type == AgentOperations.INSTALL_CUSTOM_APPS:
            table = CustomAppsCollection
            app_key = CustomAppsKey.AppId
            pkg = (
                get_app_data(
                    app_id, table, app_key,
                    fields_to_pluck=[CustomAppsKey.Name, CustomAppsKey.Version, PKG_CLI_OPTIONS]
                )
            )
            pkg[PKG_FILEDATA] = get_file_data(app_id, agent_id)

            if pkg:
                uris = (
                    get_download_urls(
                        self.customer_name, app_id,
                        pkg[PKG_FILEDATA], AgentOperations.INSTALL_CUSTOM_APPS
                    )
                )

                pkg_data = {
                    APP_NAME: pkg[CustomAppsKey.Name],
                    APP_VERSION: pkg[AppsKey.Version],
                    APP_URIS: uris,
                    APP_ID: app_id,
                    PKG_CLI_OPTIONS: pkg[PKG_CLI_OPTIONS]
                }

        elif oper_type == AgentOperations.INSTALL_SUPPORTED_APPS:
            table = SupportedAppsCollection
            app_key = SupportedAppsKey.AppId
            pkg = (
                get_app_data(
                    app_id, table, app_key,
                    fields_to_pluck=[SupportedAppsKey.Name, SupportedAppsKey.Version, PKG_CLI_OPTIONS]
                )
            )
            pkg[PKG_FILEDATA] = get_file_data(app_id, agent_id)

            if pkg:
                uris = (
                    get_download_urls(
                        self.customer_name, app_id, pkg[PKG_FILEDATA]
                    )
                )

                pkg_data = {
                    APP_NAME: pkg[SupportedAppsKey.Name],
                    APP_VERSION: pkg[AppsKey.Version],
                    APP_URIS: uris,
                    APP_ID: app_id,
                    PKG_CLI_OPTIONS: pkg[PKG_CLI_OPTIONS]
                }

        elif oper_type == AgentOperations.INSTALL_AGENT_APPS:
            table = AgentAppsCollection
            app_key = AgentAppsKey.AppId
            pkg = (
                get_app_data(
                    fields_to_pluck=[AgentAppsKey.Name, AgentAppsKey.Version, PKG_CLI_OPTIONS]
                )
            )
            pkg[PKG_FILEDATA] = get_file_data(app_id, agent_id)

            if pkg:
                uris = (
                    get_download_urls(
                        self.customer_name, app_id, pkg[PKG_FILEDATA]
                    )
                )

                pkg_data = {
                    APP_NAME: pkg[AgentAppsKey.Name],
                    APP_VERSION: pkg[AppsKey.Version],
                    APP_URIS: uris,
                    APP_ID: app_id,
                    PKG_CLI_OPTIONS: pkg[PKG_CLI_OPTIONS]
                }

        return(pkg_data)

    def _return_valid_app_ids_for_agent(self, agent_id, app_ids,
                                        table=AppsPerAgentCollection):
        conn = db_connect()
        if table == AppsPerAgentCollection:
            INDEX = AppsPerAgentIndexes.AgentIdAndAppId
            APPID = AppsKey.AppId
        elif table == CustomAppsPerAgentCollection:
            INDEX = CustomAppsPerAgentIndexes.AgentIdAndAppId
            APPID = CustomAppsKey.AppId
        elif table == SupportedAppsPerAgentCollection:
            INDEX = SupportedAppsPerAgentIndexes.AgentIdAndAppId
            APPID = SupportedAppsKey.AppId
        elif table == AgentAppsPerAgentCollection:
            INDEX = AgentAppsPerAgentIndexes.AgentIdAndAppId
            APPID = AgentAppsKey.AppId

        try:
            valid_appids = (
                r
                .expr(app_ids)
                .map(
                    lambda x: r.table(table)
                    .get_all(
                        [agent_id, x], index=INDEX
                    )
                    .coerce_to('array')
                )
                .concat_map(lambda x: x[APPID])
                .run(conn)
            )
        except Exception as e:
            logger.exception(e)
            valid_appids = []

        conn.close()
        return(valid_appids)