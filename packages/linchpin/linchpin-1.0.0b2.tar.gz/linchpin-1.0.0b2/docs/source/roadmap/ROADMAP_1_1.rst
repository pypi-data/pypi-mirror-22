*******************************
LinchPin 1.1.x ROADMAP - July 31, 2017?
*******************************

More Unit Tests #257
---------------------
- coverage
- flake8
- cli fail testing
- api fail testing
- linchpin-lib pass/fail testing

Integration Testing #247
-------------------------
testing of each provider set in core (openstack, ec2, gce, libvirt)

Regression Testing
-------------------------
More research needed

Cloud-Init functionality #111 #148
-----------------------------
- Libvirt
- openstack userdata tooling
- aws userdata??
- gce userdata??

State Logging 
-------------------
- Report transitioning between states
  - (prehooks -> up -> posthooks -> resources -> postreshooks? -> inventory_generation -> postgenhooks)

Upgrade to Ansible 2.3
-------------------------------
- Handle new magic_vars
- Verify/Adapt any API changes work in LinchPin

Python 3 conversion
---------------------------
Separate core and contributed providers in packaging (we've already got some of this, but it's not clean)

******************************
LinchPin 1.2.x ROADMAP - October 1, 2017??
******************************

Authentication Driver for Libvirt and others
-----------------------------------------
- Libvirt -- PolicyKit/SSH/tcp integration/sudo (become) methods

Reworking Schema
-------------------------
- Use cerberus on a driver by driver basis to validate schemas

Zuul Integration
---------------------
Sean Myers is working on this

New providers
-------------------
- Azure
- RHEV RHEL

Rework on Roles
-----------------------
- Small playbooks that do provision/teardown per provider
- Create a plugin model for ephemeral services

Split out Linchpin API/REST API from cli
------------------------------------------------------
- API becomes linchpin pkg (libraries and playbooks)
- CLI becomes linchpin-cli pkg (just cli tooling)

Hooks
--------

- Built-in Hooks
  - inventory generator
  - resource outputter
  - schema validation
- Global hooks functionality

- State tracking:
  - on_success/on_failure flags for hooks and actions
  - Implement retry in hooks on failure

REST Service
-------------------
- simple rest service interface

*******************************
LinchPin 1.3.x ROADMAP - January 1, 2018???
*******************************

Network Provisioning
----------------------------
- Teardown options

Asynchronous Target Provisioning
---------------------------------------------
- Using a distributed queue to provision targets and get their states/outputs ??? ( more research needed)

Linchpin Status tracking
--------------------------------
- Use a database to track status  multiple targets.
- Give unique identifiers to target/topology/layout triples for naming

*******************************
Linchpin 2.0.x ROADMAP - June 1, 2018????????
*******************************

- Topology / parser rewrite
  - change groups and types and such to be more flexible

Optimization for performance, security

Inventory Generation for other tools
-----------------------------------------------

Puppet manifest
SaltStack groups
VagrantFile
Terraform
Cloudforms
etc
