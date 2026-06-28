import { UserRepository } from '../../../domain/repositories/UserRepository';
import { User } from '../../../domain/entities/User';
import { pool } from './db';

export class PgUserRepository implements UserRepository {
  async findById(id: number): Promise<User | null> {
    const result = await pool.query('SELECT * FROM users WHERE id = $1', [id]);
    if (result.rows.length === 0) return null;
    const row = result.rows[0];
    return new User(row.id, row.username, row.email, row.password, row.role, row.created_at);
  }

  async findByEmail(email: string): Promise<User | null> {
    const result = await pool.query('SELECT * FROM users WHERE email = $1', [email]);
    if (result.rows.length === 0) return null;
    const row = result.rows[0];
    return new User(row.id, row.username, row.email, row.password, row.role, row.created_at);
  }

  async findByUsername(username: string): Promise<User | null> {
    const result = await pool.query('SELECT * FROM users WHERE username = $1', [username]);
    if (result.rows.length === 0) return null;
    const row = result.rows[0];
    return new User(row.id, row.username, row.email, row.password, row.role, row.created_at);
  }

  async create(user: Omit<User, 'id' | 'createdAt'>): Promise<User> {
    const result = await pool.query(
      'INSERT INTO users (username, email, password, role) VALUES ($1, $2, $3, $4) RETURNING *',
      [user.username, user.email, user.password, user.role]
    );
    const row = result.rows[0];
    return new User(row.id, row.username, row.email, row.password, row.role, row.created_at);
  }
}
