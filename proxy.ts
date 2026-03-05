import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const SALT = "Troy_Fallen_123";

export async function proxy(request: NextRequest) {
    if (request.nextUrl.pathname.startsWith('/api/hate')) {
        const checksum = request.headers.get('x-hate-checksum');
        const timeStr = request.headers.get('x-hate-time');

        if (!checksum || !timeStr) {
            return fallback();
        }

        const time = parseInt(timeStr, 10);
        if (isNaN(time)) {
            return fallback();
        }

        const now = Date.now();
        if (Math.abs(now - time) > 5000) {
            return fallback();
        }

        const encoder = new TextEncoder();
        const data = encoder.encode(SALT + timeStr);
        const hashBuffer = await crypto.subtle.digest('SHA-256', data);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');

        if (checksum !== hashHex) {
            return fallback();
        }

        return NextResponse.next();
    }
}

function fallback() {
    return new NextResponse(
        JSON.stringify({ error: "I'm a Teapot. Checksum required or time out of sync." }),
        {
            status: 418,
            headers: {
                'Content-Type': 'application/json',
                'X-Hint': Date.now().toString(),
                'Server': 'Hate-Edge-Gateway'
            }
        }
    );
}

export const config = {
    matcher: '/api/hate/:path*',
}
