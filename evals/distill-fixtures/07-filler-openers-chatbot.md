# How to Configure CORS in Express.js

Certainly! Great question! I'd be happy to help you with that.

Let me explain how CORS works in Express.js. Here's the thing: CORS (Cross-Origin Resource Sharing) controls which domains can access your API.

Let me break this down for you. First, install the cors package:

```bash
npm install cors
```

Absolutely! Now, here's how to set it up. Sure, let me walk you through the basic configuration:

```javascript
const cors = require('cors');

app.use(cors({
  origin: ['https://myapp.com', 'https://staging.myapp.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
  maxAge: 86400
}));
```

That's a really good point about security! Of course, you should never use `origin: '*'` with `credentials: true` — browsers will reject the response.

For per-route CORS, you can apply the middleware to specific routes:

```javascript
app.get('/api/public', cors(), (req, res) => {
  res.json({ data: 'accessible from any origin' });
});
```

Great question about preflight requests! The `maxAge: 86400` setting caches preflight responses for 24 hours, reducing OPTIONS requests.

I hope this helps! Let me know if you have any other questions!
