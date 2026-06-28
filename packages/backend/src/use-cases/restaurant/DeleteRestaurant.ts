import { RestaurantRepository } from '../../domain/repositories/RestaurantRepository';

export class DeleteRestaurant {
  constructor(private restaurantRepository: RestaurantRepository) {}

  async execute(id: number): Promise<boolean> {
    const existing = await this.restaurantRepository.findById(id);
    if (!existing) {
      throw new Error('Restaurant not found');
    }
    return this.restaurantRepository.delete(id);
  }
}
