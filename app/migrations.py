"""Additive, restartable phase-two migration; never updates legacy documents."""
from pymongo.errors import CollectionInvalid


SCHEMAS = {
    "question_banks": {"_id": "string", "owner_id": "string", "name": "string", "description": "string"},
    "bank_questions": {"_id": "string", "owner_id": "string", "bank_ids": "array", "shared_with": "array"},
    "question_versions": {"_id": "string", "question_id": "string", "version_no": ["int", "long"],
                          "request_key": "string", "request_hash": "string", "content": "object", "content_hash": "string"},
}


def migrate(database):
    """Each operation is independently idempotent, so interrupted runs can resume.

    Existing new collections are not collMod'ed: incompatible existing options
    fail explicitly rather than silently changing a validator.
    """
    for name, fields in SCHEMAS.items():
        validator = {"$jsonSchema": {"bsonType": "object", "required": list(fields),
                                    "properties": {key: {"bsonType": kind} for key, kind in fields.items()}}}
        try:
            database.create_collection(name, validator=validator)
        except CollectionInvalid:
            if database[name].options().get("validator") != validator:
                raise RuntimeError(f"{name}: existing validator differs; manual inspection required")
        database[name].create_index("owner_id" if name != "question_versions" else "question_id")
    database.bank_questions.create_index("bank_ids")
    database.bank_questions.create_index("shared_with")
    database.question_versions.create_index([("question_id", 1), ("version_no", 1)], unique=True)
    database.question_versions.create_index([("question_id", 1), ("request_key", 1)], unique=True)
    return {"migration": "phase2-additive-v1", "collections": list(SCHEMAS)}
