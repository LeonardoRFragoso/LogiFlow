-- Add cargo column to leads table if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'leads' 
        AND column_name = 'cargo'
    ) THEN
        ALTER TABLE leads ADD COLUMN cargo VARCHAR(100);
        RAISE NOTICE 'Column cargo added to leads table';
    ELSE
        RAISE NOTICE 'Column cargo already exists in leads table';
    END IF;
END $$;
