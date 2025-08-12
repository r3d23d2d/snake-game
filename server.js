import express from 'express';
import cors from 'cors';
import { OpenAI } from 'openai';

const app = express();
app.use(cors());
app.use(express.json());

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

app.post('/api/minus', async (req, res) => {
  try {
    const { phrases } = req.body;
    const userContent = `Сгенерируй список минус-слов для Яндекс Директа на основе следующих фраз: \n${phrases.join('\n')}`;

    const completion = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [
        { role: 'system', content: 'Ты помощник, который выделяет минус-слова для Яндекс Директа.' },
        { role: 'user', content: userContent }
      ]
    });

    const minusWords = completion.choices[0]?.message?.content ?? '';
    res.json({ minusWords });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Ошибка при запросе к OpenAI' });
  }
});

app.use(express.static('public'));

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
