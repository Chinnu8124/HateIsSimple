import { NextResponse } from 'next/server';

export async function GET(req: Request) {
    const isProcessing = (globalThis as any).hateProcessing;
    if (isProcessing) {
        return NextResponse.json({ part_2: "ST4T3_0F_C0LD_W4R}" }, { status: 200 });
    }
    return NextResponse.json({ error: "Nothing to see here." }, { status: 400 });
}

export async function POST(req: Request) {
    try {
        const bodyText = await req.text();
        const byteLength = new TextEncoder().encode(bodyText).length;

        if (byteLength < 13336) {
            return NextResponse.json({ error: "Too light" }, { status: 400 });
        }
        if (byteLength === 13336) {
            return NextResponse.json({ error: "Almost there" }, { status: 400 });
        }
        if (byteLength > 13337) {
            return NextResponse.json({ error: "Too heavy" }, { status: 400 });
        }

        // Must be valid JSON
        let parsedBody;
        try {
            parsedBody = JSON.parse(bodyText);
        } catch (e) {
            return NextResponse.json({ error: "Malformed thoughts. Must be valid JSON." }, { status: 400 });
        }

        const now = Date.now();
        let state = (globalThis as any).hateState || 0;
        const lastAccess = (globalThis as any).hateLastAccess || now;

        // Reset if more than 10 seconds (10000 ms) have passed since last access
        if (now - lastAccess > 10000) {
            state = 0;
        }

        state++;
        (globalThis as any).hateState = state;
        (globalThis as any).hateLastAccess = now;

        if (state === 1) {
            return NextResponse.json({ status: "Cold Hearted" }, { status: 200 });
        } else if (state === 2) {
            return NextResponse.json({ status: "Thawing..." }, { status: 200 });
        } else {
            // Simulate heavy processing for the race condition
            (globalThis as any).hateProcessing = true;
            await new Promise(resolve => setTimeout(resolve, 2000)); // 2 second window
            (globalThis as any).hateProcessing = false;

            return NextResponse.json({ part_1: "BPCTF{H4T3_1S_4_" }, { status: 200 });
        }
    } catch (error) {
        return NextResponse.json({ error: "Internal Server Error" }, { status: 500 });
    }
}
