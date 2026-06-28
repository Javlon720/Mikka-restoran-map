import { FastifyRequest, FastifyReply } from 'fastify';
import fs from 'fs';
import path from 'path';
import { pipeline } from 'stream/promises';

const uploadDir = path.join(__dirname, '../../uploads');

// Ensure directory exists
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir, { recursive: true });
}

export const upload = async (req: FastifyRequest, reply: FastifyReply) => {
  if (!req.isMultipart()) {
    return;
  }

  const body: any = {};
  let fileInfo: any = null;

  try {
    const parts = req.parts();
    for await (const part of parts) {
      if (part.type === 'file') {
        const allowedTypes = /jpeg|jpg|png|gif|webp/;
        const ext = path.extname(part.filename).toLowerCase();
        
        if (!allowedTypes.test(part.mimetype) || !allowedTypes.test(ext)) {
          return reply.code(400).send({ success: false, error: 'Only image files are allowed!' });
        }

        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1e9);
        const filename = `${uniqueSuffix}${ext}`;
        const filepath = path.join(uploadDir, filename);

        // Save file stream to disk
        await pipeline(part.file, fs.createWriteStream(filepath));

        fileInfo = {
          fieldname: part.fieldname,
          originalname: part.filename,
          encoding: part.encoding,
          mimetype: part.mimetype,
          filename: filename,
          path: filepath,
          size: fs.statSync(filepath).size
        };
      } else {
        // It's a normal form field
        body[part.fieldname] = part.value;
      }
    }
  } catch (err: any) {
    return reply.code(400).send({ success: false, error: err.message });
  }

  // Populate req.body and req.file just like Multer did
  req.body = body;
  (req as any).file = fileInfo;
};
