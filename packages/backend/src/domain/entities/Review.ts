export class Review {
  constructor(
    public readonly id: number,
    public readonly restaurantId: number,
    public readonly userId: number,
    public readonly rating: number,
    public readonly comment: string,
    public readonly imageUrl: string | null,
    public readonly createdAt?: Date,
    public readonly username?: string 
  ) {}
}
