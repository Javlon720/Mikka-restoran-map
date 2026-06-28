import { ReviewRepository } from '../../domain/repositories/ReviewRepository';
import { Review } from '../../domain/entities/Review';

export class GetReviewsByRestaurant {
  constructor(private reviewRepository: ReviewRepository) {}

  async execute(restaurantId: number): Promise<Review[]> {
    if (!restaurantId) {
      throw new Error('Restaurant ID is required');
    }
    return this.reviewRepository.findByRestaurantId(restaurantId);
  }
}
