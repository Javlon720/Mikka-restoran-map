import { RestaurantRepository } from '../../../domain/repositories/RestaurantRepository';
import { Restaurant } from '../../../domain/entities/Restaurant';
import { pool } from './db';

export class PgRestaurantRepository implements RestaurantRepository {
  async findAll(search?: string): Promise<Restaurant[]> {
    let query = 'SELECT * FROM restaurants';
    const params: any[] = [];

    if (search) {
      query += ' WHERE name ILIKE $1 OR cuisine ILIKE $1 OR description ILIKE $1 OR address ILIKE $1';
      params.push(`%${search}%`);
    }

    query += ' ORDER BY id DESC';
    const result = await pool.query(query, params);

    return result.rows.map(row => new Restaurant(
      row.id,
      row.name,
      row.description,
      row.cuisine,
      row.address,
      row.image_url,
      row.lat ? Number(row.lat) : null,
      row.lng ? Number(row.lng) : null,
      row.created_by,
      row.created_at
    ));
  }

  async findById(id: number): Promise<Restaurant | null> {
    const result = await pool.query('SELECT * FROM restaurants WHERE id = $1', [id]);
    if (result.rows.length === 0) return null;
    const row = result.rows[0];

    return new Restaurant(
      row.id,
      row.name,
      row.description,
      row.cuisine,
      row.address,
      row.image_url,
      row.lat ? Number(row.lat) : null,
      row.lng ? Number(row.lng) : null,
      row.created_by,
      row.created_at
    );
  }

  async create(restaurant: Omit<Restaurant, 'id' | 'createdAt'>): Promise<Restaurant> {
    const result = await pool.query(
      `INSERT INTO restaurants (name, description, cuisine, address, image_url, lat, lng, created_by)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING *`,
      [
        restaurant.name,
        restaurant.description,
        restaurant.cuisine,
        restaurant.address,
        restaurant.imageUrl,
        restaurant.lat,
        restaurant.lng,
        restaurant.createdBy
      ]
    );
    const row = result.rows[0];

    return new Restaurant(
      row.id,
      row.name,
      row.description,
      row.cuisine,
      row.address,
      row.image_url,
      row.lat ? Number(row.lat) : null,
      row.lng ? Number(row.lng) : null,
      row.created_by,
      row.created_at
    );
  }

  async update(restaurant: Restaurant): Promise<Restaurant> {
    const result = await pool.query(
      `UPDATE restaurants 
       SET name = $1, description = $2, cuisine = $3, address = $4, image_url = $5, lat = $6, lng = $7
       WHERE id = $8 RETURNING *`,
      [
        restaurant.name,
        restaurant.description,
        restaurant.cuisine,
        restaurant.address,
        restaurant.imageUrl,
        restaurant.lat,
        restaurant.lng,
        restaurant.id
      ]
    );
    const row = result.rows[0];

    return new Restaurant(
      row.id,
      row.name,
      row.description,
      row.cuisine,
      row.address,
      row.image_url,
      row.lat ? Number(row.lat) : null,
      row.lng ? Number(row.lng) : null,
      row.created_by,
      row.created_at
    );
  }

  async delete(id: number): Promise<boolean> {
    const result = await pool.query('DELETE FROM restaurants WHERE id = $1', [id]);
    return (result.rowCount ?? 0) > 0;
  }
}
