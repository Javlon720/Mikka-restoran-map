import { GoogleGenerativeAI } from '@google/generative-ai';
import { RestaurantRepository } from '../../domain/repositories/RestaurantRepository';

export class GetGeminiResponse {
  constructor(private restaurantRepository: RestaurantRepository) {}

  async execute(message: string, history: Array<{ role: 'user' | 'model'; content: string }>): Promise<string> {
    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey || apiKey === 'your-gemini-api-key-here' || apiKey.trim() === '') {
      return "Gemini AI features are currently disabled. Please configure a valid GEMINI_API_KEY in the backend .env file.";
    }

    // Retrieve restaurant context
    const restaurants = await this.restaurantRepository.findAll();
    let restaurantContext = 'Available Restaurants in Mikka Restaurant Reviews application:\n';
    
    if (restaurants.length === 0) {
      restaurantContext += 'No restaurants are registered on the platform yet.';
    } else {
      restaurants.forEach((r, idx) => {
        restaurantContext += `${idx + 1}. Name: "${r.name}", Cuisine: "${r.cuisine}", Address: "${r.address}", Description: "${r.description}"\n`;
      });
    }

    const systemInstruction = `You are "Mikka AI Guide", a helpful, friendly, and smart AI assistant integrated into Mikka, a premium restaurant review application.
Your goal is to help users find restaurants, suggest dishes, answer general culinary questions, and guide them around the platform.

Here is the current real-time list of restaurants available on the Mikka platform:
--------------------------------------------------
${restaurantContext}
--------------------------------------------------

Guidelines:
1. Always base your restaurant suggestions on the Mikka platform list above. If a restaurant is not in this list, clearly explain that it is not yet registered on Mikka, but feel free to discuss other restaurants globally if the user asks.
2. Be polite, concise, and helpful. Keep responses under 3 paragraphs if possible.
3. You can format your output in clean Markdown.
4. Keep the tone friendly, enthusiastic, and professional.
5. If the user asks about the app itself, explain that Mikka is a premium restaurant review platform designed by JDU students.`;

    try {
      const genAI = new GoogleGenerativeAI(apiKey);
      const model = genAI.getGenerativeModel({
        model: 'gemini-2.5-flash',
        systemInstruction: systemInstruction,
      });

      // Format history to the structure required by Gemini SDK:
      // { role: 'user' | 'model', parts: [{ text: string }] }
      const formattedHistory = history.map(h => ({
        role: h.role === 'model' ? 'model' : 'user',
        parts: [{ text: h.content }]
      }));

      const chat = model.startChat({
        history: formattedHistory,
      });

      const result = await chat.sendMessage(message);
      const response = await result.response;
      return response.text();
    } catch (err: any) {
      console.error('Gemini API call failed:', err);
      return `Error calling Gemini AI: ${err.message}`;
    }
  }
}
