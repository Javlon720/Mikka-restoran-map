import { FastifyRequest, FastifyReply } from 'fastify';
import { GetReviewsByRestaurant } from '../../use-cases/review/GetReviewsByRestaurant';
import { CreateReview } from '../../use-cases/review/CreateReview';
import { ReviewRepository } from '../../domain/repositories/ReviewRepository';
import { Review } from '../../domain/entities/Review';

export class ReviewController {
  constructor(
    private getReviewsByRestaurant: GetReviewsByRestaurant,
    private createReview: CreateReview,
    private reviewRepository: ReviewRepository
  ) {}

  async getByRestaurantId(req: FastifyRequest, reply: FastifyReply): Promise<void> {
    try {
      const restaurantId = parseInt((req.params as any).restaurantId, 10);
      const reviews = await this.getReviewsByRestaurant.execute(restaurantId);
      reply.code(200).send({ success: true, data: reviews });
    } catch (error: any) {
      reply.code(500).send({ success: false, error: error.message });
    }
  }

  async create(req: FastifyRequest, reply: FastifyReply): Promise<void> {
    try {
      const user = (req as any).user;
      if (!user) {
        reply.code(401).send({ success: false, error: 'Unauthorized' });
        return;
      }

      const { restaurantId, rating, comment } = req.body as any;
      const file = (req as any).file;
      const imageUrl = file ? `/uploads/${file.filename}` : null;

      const review = await this.createReview.execute({
        restaurantId: parseInt(restaurantId, 10),
        userId: user.id,
        rating: parseInt(rating, 10),
        comment,
        imageUrl
      });

      reply.code(201).send({ success: true, data: review });
    } catch (error: any) {
      reply.code(400).send({ success: false, error: error.message });
    }
  }

  async update(req: FastifyRequest, reply: FastifyReply): Promise<void> {
    try {
      const user = (req as any).user;
      if (!user) {
        reply.code(401).send({ success: false, error: 'Unauthorized' });
        return;
      }

      const reviewId = parseInt((req.params as any).id, 10);
      const existing = await this.reviewRepository.findById(reviewId);
      if (!existing) {
        reply.code(404).send({ success: false, error: 'Review not found' });
        return;
      }

      // Authorization check: only owner or admin can update
      if (existing.userId !== user.id && user.role !== 'admin') {
        reply.code(403).send({ success: false, error: 'Access denied. You can only edit your own reviews.' });
        return;
      }

      const { rating, comment } = req.body as any;
      const file = (req as any).file;
      const imageUrl = file ? `/uploads/${file.filename}` : undefined;

      const updatedReview = new Review(
        reviewId,
        existing.restaurantId,
        existing.userId,
        rating ? parseInt(rating, 10) : existing.rating,
        comment || existing.comment,
        imageUrl !== undefined ? imageUrl : existing.imageUrl,
        existing.createdAt,
        existing.username
      );

      const saved = await this.reviewRepository.update(updatedReview);
      reply.code(200).send({ success: true, data: saved });
    } catch (error: any) {
      reply.code(400).send({ success: false, error: error.message });
    }
  }

  async delete(req: FastifyRequest, reply: FastifyReply): Promise<void> {
    try {
      const user = (req as any).user;
      if (!user) {
        reply.code(401).send({ success: false, error: 'Unauthorized' });
        return;
      }

      const reviewId = parseInt((req.params as any).id, 10);
      const existing = await this.reviewRepository.findById(reviewId);
      if (!existing) {
        reply.code(404).send({ success: false, error: 'Review not found' });
        return;
      }

      // Authorization check: only owner or admin can delete
      if (existing.userId !== user.id && user.role !== 'admin') {
        reply.code(403).send({ success: false, error: 'Access denied. You can only delete your own reviews.' });
        return;
      }

      await this.reviewRepository.delete(reviewId);
      reply.code(200).send({ success: true, message: 'Review deleted successfully' });
    } catch (error: any) {
      reply.code(400).send({ success: false, error: error.message });
    }
  }
}
