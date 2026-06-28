import { Pool } from 'pg';
import path from 'path';
import dotenv from 'dotenv';

dotenv.config({ path: path.resolve(__dirname, '../../../../../../.env') });

export const pool = new Pool({
  connectionString: process.env.DATABASE_URL
});
