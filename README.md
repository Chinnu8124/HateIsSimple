# Hate Is Simple (Web Exploitation)

*If LOVE IS Complicated was a walk in the park, HATE IS SIMPLE is a walk through a minefield during a solar flare.*

## Description
You thought the last challenge was hard? It turns out love is complicated, but hate... hate is terrifyingly simple. It's the execution that kills you. We found this strange portal on the edge of the network. It just sits there, asking for a reason to exist. Can you bypass its defenses and extract the secrets hidden within its memory?

**Flag Format:** `HATE{...}`

## Setup Instructions

This challenge is built using Next.js to simulate an Edge/Serverless environment. The environment heavily relies on HTTP middleware proxies, precise byte sizes, and simulating memory leaks.

### Running Locally

Requirements: 
- Node.js (v18+)
- npm

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. The challenge will be accessible at `http://localhost:3000` (or whichever port Next.js assigns).

### Deployment

Because this challenge relies on Edge Middleware and "Warm Start" container lifecycle exploitation, it is best deployed on a platform like **Vercel** or **Dockerized** behind a standard proxy.

If building a Docker image, simply run:
```bash
npm run build
npm run start
```

## Hints for Players

1.  **Hint 1:** Look closely at the response headers when you hit a wall. What time is the server running on? Can you prove you belong in that timeline?
2.  **Hint 2:** Sometimes, the size of your thoughts matters more than the thoughts themselves. 13,337 is a very specific number.
3.  **Hint 3:** The server has a short memory. You have to keep it "warm" if you want to get anywhere. Keep knocking.
4.  **Hint 4:** To get the final piece, you need to be in two places at once. Literally.
