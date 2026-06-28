import { ReviewRepository } from '../../domain/repositories/ReviewRepository';
import { Review } from '../../domain/entities/Review';

export class CreateReview {
  constructor(private reviewRepository: ReviewRepository) {}

  async execute(data: {
    restaurantId: number;
    userId: number;
    rating: number;
    comment: string;
    imageUrl: string | null;
  }): Promise<Review> {
    if (!data.restaurantId || !data.userId || !data.rating || !data.comment) {
      throw new Error('Restaurant ID, User ID, rating, and comment are required');
    }

    if (data.rating < 1 || data.rating > 5) {
      throw new Error('Rating must be between 1 and 5');
    }

    return this.reviewRepository.create({
      restaurantId: data.restaurantId,
      userId: data.userId,
      rating: data.rating,
      comment: data.comment,
      imageUrl: data.imageUrl
    });
  }
}
