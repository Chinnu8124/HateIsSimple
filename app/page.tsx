'use client';

import { useState, useEffect } from 'react';

function FloatingEmojis() {
  const [emojis, setEmojis] = useState<{ id: number; left: string; size: string; duration: string; delay: string }[]>([]);

  useEffect(() => {
    const emojis = Array.from({ length: 30 }).map((_, i) => ({
      id: i,
      left: `${Math.random() * 100}%`,
      size: `${Math.random() * 6 + 3}rem`,
      duration: `${Math.random() * 5 + 5}s`,
      delay: `${Math.random() * 5}s`,
    }));
    setEmojis(emojis);
  }, []);

  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden z-[-1]">
      {emojis.map((emoji) => (
        <div
          key={emoji.id}
          className="absolute bottom-[-10%] opacity-20 animate-float"
          style={{
            left: emoji.left,
            fontSize: emoji.size,
            animationDuration: emoji.duration,
            animationDelay: emoji.delay,
            animationName: 'float',
            animationTimingFunction: 'linear',
            animationIterationCount: 'infinite',
          }}
        >
          🔥
        </div>
      ))}
      <style jsx>{`
        @keyframes float {
          0% {
            transform: translateY(0);
            opacity: 0;
          }
          10% {
            opacity: 0.3;
          }
          90% {
            opacity: 0.3;
          }
          100% {
            transform: translateY(-120vh);
            opacity: 0;
          }
        }
      `}</style>
    </div>
  );
}

export default function Home() {
  const [reason, setReason] = useState('');
  const [response, setResponse] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setResponse("Sending...");

    try {
      // Intentionally missing headers to fail Phase 1 initially.
      // A clever player checks the response headers (like X-Hint and Server)
      // or looks at robots.txt for the SALT and then scripts their bypass.
      const res = await fetch('/api/hate', {
        method: 'POST',
        body: JSON.stringify({ reason }),
        headers: {
          'Content-Type': 'application/json'
        }
      });

      const data = await res.json();
      setResponse(JSON.stringify(data, null, 2));
    } catch (err) {
      setResponse(String(err));
    }
  };

  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-8 w-full max-w-3xl mx-auto text-center relative">
      <FloatingEmojis />

      <h1 className="text-4xl font-bold mb-4 uppercase tracking-widest text-[#ff4444] drop-shadow-[0_0_15px_rgba(255,0,0,0.8)]">
        🔥 Hate Is Simple 🔥
      </h1>
      <p className="text-red-300 font-mono text-lg mb-12 tracking-wide">
        If *LOVE IS Complicated* was a walk in the park, this is a minefield during a solar flare.
      </p>

      <form onSubmit={handleSubmit} className="w-full max-w-lg relative group flex flex-col items-center">
        <input
          type="text"
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          placeholder="Give me a reason to exist."
          className="w-full bg-black text-red-500 placeholder-red-900 border-2 border-red-900 rounded-md p-4 text-center outline-none focus:border-red-500 focus:ring-1 focus:ring-red-500 transition-all font-mono shadow-[0_0_10px_rgba(0,0,0,0.5)]"
          autoFocus
        />
        <div className="absolute inset-0 border border-red-500/0 group-hover:border-red-500/20 rounded-md pointer-events-none transition-all duration-500 animate-pulse"></div>
      </form>

      {
        response && (
          <div className="mt-8 bg-black/80 p-4 rounded-md border border-red-900/50 w-full overflow-x-auto shadow-inner">
            <pre className="text-red-400 font-mono text-sm whitespace-pre-wrap">
              {response}
            </pre>
          </div>
        )
      }
    </main >
  );
}
