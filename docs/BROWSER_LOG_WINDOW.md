# Bounded browser log window

The live view keeps at most 20 execution records, 2,000 lines, 512 KiB of UTF-8 message text, and 8,192 UTF-16 code units per line. The JavaScript heap also contains record metadata and bounded pending/snapshot buffers; 512 KiB is the message payload limit, not a claim about total browser heap. Unicode suffix truncation never splits a scalar.

A virtual list renders only the visible rows plus overscan. Consecutive identical lines within the same execution are folded by default with a repeat count and last timestamp. The toggle unfolds only the already bounded window. Folding never modifies stored records or server evidence. Wheel/touch/pointer/keyboard interaction stops automatic tail scrolling; Jump to latest restores it. This is scroll-follow pause, not suspension of incoming ingestion.

Truncation remains visible. Server history/download remains the source for previously received raw logs, subject to server retention and transport guarantees; the UI does not claim that an offline legacy Agent delivered data it never sent. No logs are appended to localStorage. Existing connection recovery re-fetches authoritative bounded history and merges concurrent live deltas.

Tests cover 100,000-line input, 20,000 continuous deltas, multilingual/emoji byte limits, giant lines, snapshot/live overlap, replay deduplication, execution separation, and folding/unfolding without raw mutation. Unit tests, type checking and production build do not replace browser interaction QA, which is currently blocked by the cloud browser restriction.

The node execution-history modal uses the same bounded viewer and request-generation hook as the live suite page. Closing the modal invalidates pending history requests and releases its window; selecting another execution cannot render a late previous response.
