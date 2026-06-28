import { Review } from '../entities/Review';

export interface ReviewRepository {
  findByRestaurantId(restaurantId: number): Promise<Review[]>;
  findById(id: number): Promise<Review | null>;
  create(review: Omit<Review, 'id' | 'createdAt'>): Promise<Review>;
  update(review: Review): Promise<Review>;
  delete(id: number): Promise<boolean>;
}
