-- Fix OAuth2 Client - Associar com usuário admin para contexto de usuário
-- Isso resolve o erro "Module id is empty when trying to get Users"

UPDATE oauth2clients 
SET 
    assigned_user_id = '1',
    created_by = '1',
    modified_user_id = '1'
WHERE id = 'b8445d29-da7c-11f0-8e56-d6ca7fd38528';

-- Verificar resultado
SELECT 
    id, 
    name, 
    allowed_grant_type, 
    assigned_user_id, 
    created_by,
    is_confidential
FROM oauth2clients 
WHERE deleted = 0;
