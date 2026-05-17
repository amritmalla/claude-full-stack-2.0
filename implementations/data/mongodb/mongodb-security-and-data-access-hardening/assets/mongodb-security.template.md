# MongoDB Security and Data Access Hardening — Layout Reference

Use this as the canonical auth / RBAC / TLS / CSFLE / audit pattern reference. Placeholder tokens use `<name>`. This skill enforces the upstream PII classification and wires CSFLE to the provisioned KMS; the KMS itself is an infrastructure handoff and data classification is `data-architecture.md` / `mongodb-data-model-and-migration`'s.

## Deliverable layout

```
security-hardening.md          # auth mechanism + role/grant matrix + TLS posture +
                               #   CSFLE field->key map + redaction/views + network +
                               #   audit config + negative-test results + backup key model
config/
├── roles.js                   # least-privilege custom roles (reproducible)
├── tls.conf                   # client + intra-cluster TLS
├── csfle-schema.json          # encrypted-field schema (field -> key, mode)
└── audit-filter.json          # security events; NO PII/secret values
```

## Auth always on; least-privilege role (not root)

```js
// mongod.conf:  security.authorization: enabled  + TLS (below). Never auth off
//               on a reachable host.
db.createRole({
  role: "<svc>-app",
  privileges: [{
    resource: { db: "<appdb>", collection: "<ownedCollection>" },
    actions: ["find", "insert", "update"]      // NOT remove/dropDatabase; NOT "*"
  }],
  roles: []
})
db.createUser({ user: "<svc>", pwd: "<from-secret-store>", roles: ["<svc>-app"] })
// Application connects as <svc> — never root / dbOwner / a shared superuser.
```

## TLS — client + intra-cluster, no plaintext

```yaml
# mongod.conf
net:
  tls:
    mode: requireTLS                 # no plaintext listener
    certificateKeyFile: <path>       # provenance + rotation stated in security-hardening.md
security:
  clusterAuthMode: x509              # internal member auth (replication skill's requirement)
```

## CSFLE — encrypt exactly the classified PII fields

```json
// csfle-schema.json  (field -> key; mode per access pattern)
{
  "<appdb>.<collection>": {
    "bsonType": "object",
    "encryptMetadata": { "keyId": "/<dataKeyId-from-provisioned-KMS>" },
    "properties": {
      "ssn":   { "encrypt": { "bsonType": "string",
                              "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic" } },
      "notes": { "encrypt": { "bsonType": "string",
                              "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Random" } }
    }
  }
}
// Deterministic only where equality query is required; Random otherwise.
// KMS is provisioned by infrastructure; this maps fields -> keys.
```

## Role-scoped redaction (PII visible to some roles only)

```js
db.createView("<collection>_redacted", "<collection>", [
  { $project: { ssn: 0, dob: 0 } }      // grant non-privileged role this view only
])
```

## Audit — security events, never the PII itself

```json
// audit-filter.json
{ "atype": { "$in": ["authenticate", "createRole", "grantRolesToUser",
                      "dropCollection", "authCheck"] } }
// Destination: tamper-resistant sink. Verify the stream carries NO field values.
```

## Negative-test record (in security-hardening.md)

```
[ ] unauthorized principal -> denied            : <result>
[ ] <svc> role cannot drop/readPII unintended   : <result>
[ ] raw read of `ssn` without key = ciphertext  : <result>
```

## Handoffs this skill names (does not implement)

| Concern | Owner |
|---|---|
| Document modeling, PII classification of fields, migrations | `mongodb-data-model-and-migration` / `data-architecture.md` |
| Query/index/pipeline tuning | `mongodb-indexing-and-query-optimization` |
| Replica topology (declares the internal-auth requirement) | `mongodb-replication-and-ha-readiness` |
| Backup procedure (consumes this skill's artifact key/access model) | `mongodb-backup-and-operational-readiness` |
| KMS / secret-store provisioning | infrastructure layer |
