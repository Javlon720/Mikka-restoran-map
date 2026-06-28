import { ReviewRepository } from '../../../domain/repositories/ReviewRepository';
import { Review } from '../../../domain/entities/Review';
import { pool } from './db';

export class PgReviewRepository implements ReviewRepository {
  async findByRestaurantId(restaurantId: number): Promise<Review[]> {
    const result = await pool.query(
      `SELECT r.*, u.username 
       FROM reviews r 
       JOIN users u ON r.user_id = u.id 
       WHERE r.restaurant_id = $1 
       ORDER BY r.id DESC`,
      [restaurantId]
    );

    return result.rows.map(row => new Review(
      row.id,
      row.restaurant_id,
      row.user_id,
      row.rating,
      row.comment,
      row.image_url,
      row.created_at,
      row.username
    ));
  }

  async findById(id: number): Promise<Review | null> {
    const result = await pool.query(
      `SELECT r.*, u.username 
       FROM reviews r 
       JOIN users u ON r.user_id = u.id 
       WHERE r.id = $1`,
      [id]
    );
    if (result.rows.length === 0) return null;
    const row = result.rows[0];

    return new Review(
      row.id,
      row.restaurant_id,
      row.user_id,
      row.rating,
      row.comment,
      row.image_url,
      row.created_at,
      row.username
    );
  }

  async create(review: Omit<Review, 'id' | 'createdAt'>): Promise<Review> {
    const insertResult = await pool.query(
      `INSERT INTO reviews (restaurant_id, user_id, rating, comment, image_url)
       VALUES ($1, $2, $3, $4, $5) RETURNING *`,
      [review.restaurantId, review.userId, review.rating, review.comment, review.imageUrl]
    );
    const newRow = insertResult.rows[0];

    // Fetch username for the returned Review entity
    const userResult = await pool.query('SELECT username FROM users WHERE id = $1', [review.userId]);
    const username = userResult.rows[0]?.username || 'Unknown';

    return new Review(
      newRow.id,
      newRow.restaurant_id,
      newRow.user_id,
      newRow.rating,
      newRow.comment,
      newRow.image_url,
      newRow.created_at,
      username
    );
  }

  async update(review: Review): Promise<Review> {
    const result = await pool.query(
      `UPDATE reviews 
       SET rating = $1, comment = $2, image_url = $3 
       WHERE id = $4 RETURNING *`,
      [review.rating, review.comment, review.imageUrl, review.id]
    );
    const row = result.rows[0];

    // Fetch username for the returned Review entity
    const userResult = await pool.query('SELECT username FROM users WHERE id = $1', [row.user_id]);
    const username = userResult.rows[0]?.username || 'Unknown';

    return new Review(
      row.id,
      row.restaurant_id,
      row.user_id,
      row.rating,
      row.comment,
      row.image_url,
      row.created_at,
      username
    );
  }

  async delete(id: number): Promise<boolean> {
    const result = await pool.query('DELETE FROM reviews WHERE id = $1', [id]);
    return (result.rowCount ?? 0) > 0;
  }
}
