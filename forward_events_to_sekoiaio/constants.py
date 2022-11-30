SEKOIAIO_INTAKE_HOST = "https://intake.sekoia.io"
JSON_ENVELOP_BYTES = len('{"intake_key":"","jsons":[]}') + 36  # intake key size
INTAKE_PAYLOAD_BYTES_MAX_SIZE = 10485760  # 10Miobytes
CHUNK_BYTES_MAX_SIZE = INTAKE_PAYLOAD_BYTES_MAX_SIZE - JSON_ENVELOP_BYTES
