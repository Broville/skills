# Provenance

Source: https://github.com/pbakaus/impeccable/tree/dad8dbb3aac21ad1fa236c110315ef4abece23e8

Version: 4.7.0; license: Apache-2.0. The entire .agents/skills/impeccable payload is vendored unchanged under upstream/, except SKILL.md is named PLAYBOOK.md to avoid a duplicate discoverable skill. SOURCE-SHA256.json records every original payload file hash. The upstream license and third-party NOTICE are preserved alongside this document. The Broville entrypoint supplies portable metadata, explicit authority boundaries and verification.

The upstream launcher can fetch and execute an engine, inspect files, and use network services; its installer can add hooks. Nothing in this import executes that launcher, installs hooks, or changes host settings. First runtime use requires inspection and any applicable action-time source confirmation. IMPECCABLE_HOME and all test/download/cache paths must honor the user's selected artifact location. This source snapshot does not pin or include engine binary bytes.
