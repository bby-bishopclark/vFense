vFense
======

[![Join the chat at https://gitter.im/vFense/vFense](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/vFense/vFense?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

An Open-Source Cross-Platform Patch Management and vulnerabiltiy correlation tool.

### Basics on how vFense server works.

The vFense agents retrieves the metatdata of all of its updates through its assigned repositories. ( Just the metadata )
 * This metadata is than sent to the vFense server.

 * Once the server receives all of the application data from the agent, it then begins to correlate the data against vulnerability data and place the data into the appropriate collections.

 * During the processing of the application data, vFense will verify any existing local files against known meta-data and decide whether to download fresh copies.

### What happens when you install an update to an agent.
 * The install operation is placed into the server queue.
 * Once the agent checks in, the agent will retrieve all operations from its queue.
 * The agent will see the operation to install an update.
 * The agent tries to retrieve the update, validating against MD5 checksums and retrying any rejects.
