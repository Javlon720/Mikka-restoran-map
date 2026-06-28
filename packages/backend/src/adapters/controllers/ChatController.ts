import { FastifyRequest, FastifyReply } from 'fastify';
import { GetGeminiResponse } from '../../use-cases/chat/GetGeminiResponse';

export class ChatController {
  constructor(private getGeminiResponse: GetGeminiResponse) {}

  async chat(req: FastifyRequest, reply: FastifyReply): Promise<void> {
    try {
      const { message, history } = req.body as any;
      if (!message) {
        reply.code(400).send({ success: false, error: 'Message is required' });
        return;
      }

      const response = await this.getGeminiResponse.execute(message, history || []);
      reply.code(200).send({ success: true, reply: response });
    } catch (error: any) {
      reply.code(500).send({ success: false, error: error.message });
    }
  }
}
