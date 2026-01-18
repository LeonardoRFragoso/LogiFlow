-- Corrigir OAuth2 Client com SHA256
INSERT INTO oauth2clients (id, name, secret, is_confidential, allowed_grant_type, date_entered, date_modified, deleted)
VALUES (
    'b8445d29-da7c-11f0-8e56-d6ca7fd38528',
    'LogiFlow Backend API',
    'SHA256_HASH_AQUI',
    1,
    'client_credentials',
    NOW(),
    NOW(),
    0
)
ON DUPLICATE KEY UPDATE
    secret = VALUES(secret),
    allowed_grant_type = VALUES(allowed_grant_type);

SELECT id, name, LENGTH(secret) as secret_len, allowed_grant_type FROM oauth2clients WHERE deleted=0;
