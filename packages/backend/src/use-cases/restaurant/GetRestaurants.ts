import { RestaurantRepository } from '../../domain/repositories/RestaurantRepository';
import { Restaurant } from '../../domain/entities/Restaurant';

export class GetRestaurants {
  constructor(private restaurantRepository: RestaurantRepository) {}

  async execute(search?: string): Promise<Restaurant[]> {
    return this.restaurantRepository.findAll(search);
  }
}
