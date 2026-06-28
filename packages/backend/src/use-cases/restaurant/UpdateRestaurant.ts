import { RestaurantRepository } from '../../domain/repositories/RestaurantRepository';
import { Restaurant } from '../../domain/entities/Restaurant';

export class UpdateRestaurant {
  constructor(private restaurantRepository: RestaurantRepository) {}

  async execute(
    id: number,
    data: {
      name: string;
      description: string;
      cuisine: string;
      address: string;
      imageUrl: string | null;
      lat: number | null;
      lng: number | null;
    }
  ): Promise<Restaurant> {
    const existing = await this.restaurantRepository.findById(id);
    if (!existing) {
      throw new Error('Restaurant not found');
    }

    const updatedRestaurant = new Restaurant(
      id,
      data.name,
      data.description,
      data.cuisine,
      data.address,
      data.imageUrl !== undefined ? data.imageUrl : existing.imageUrl,
      data.lat !== undefined ? data.lat : existing.lat,
      data.lng !== undefined ? data.lng : existing.lng,
      existing.createdBy,
      existing.createdAt
    );

    return this.restaurantRepository.update(updatedRestaurant);
  }
}
