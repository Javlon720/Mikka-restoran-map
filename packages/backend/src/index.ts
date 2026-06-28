import { createServer } from './infrastructure/server';
import path from 'path';
import dotenv from 'dotenv';

dotenv.config({ path: path.resolve(__dirname, '../../../../.env') });

const app = createServer();
const PORT = process.env.PORT || 3000;

app.listen({ port: Number(PORT), host: '0.0.0.0' }, (err, address) => {
  if (err) {
    console.error('Error starting server:', err);
    process.exit(1);
  }
  console.log(`=============================================`);
  console.log(`🚀 JDU Restaurant Review Server is running!`);
  console.log(`👉 ${address}`);
  console.log(`=============================================`);
});
