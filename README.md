vFense
======

[![Join the chat at https://gitter.im/vFense/vFense](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/vFense/vFense?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

An Open-Source Cross-Platform Patch Management and Vulnerability Correlation tool.

### Basics on how vFense server works.

The vFense agents retrieves the metatdata of all of its updates through its assigned repositories. ( Just the metadata )
 * This metadata is than sent to the vFense server.

 * Once the server receives all of the application data from the agent, it than begins to correlate the data against vulnerability data and place the data into the appropriate collections.

 * During the processing of the application data, vFense will verify if the files already exist locally or if it needs to retrieve the updates from the urls that are within the metadata.

### What happens when you install an update to an agent.
 * The install operation is placed into the server queue.
 * Once the agent checks in, the agent will retrieve all operations from its queue.
 * The agent will see the operation to install an update.
 * The agent will then try to retrieve the update from the vFense server.
 * If the agent was able to download the file successfully from the server, the agent will then verify the given MD5 signature against one generated locally.
 * If the download or the MD5 check fails, the agent will then try again from the same repositories.
