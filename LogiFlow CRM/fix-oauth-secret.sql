-- Corrigir OAuth2 Client Secret
-- Execute: docker exec -i logiflow_db mysql -ulogiflow -plogiflow123 logiflow_crm < fix-oauth-secret.sql

UPDATE oauth2clients 
SET secret = '$2y$10$UqQJ1pm6vdl1RP5eG3gE5eseHcnJsG4tsHyAW7nB2rolS3jkMrje.',
    allowed_grant_type = 'client_credentials'
WHERE id = 'b8445d29-da7c-11f0-8e56-d6ca7fd38528';

SELECT 
    id,
    name,
    LENGTH(secret) as secret_length,
    allowed_grant_type,
    is_confidential
FROM oauth2clients 
WHERE deleted = 0;
