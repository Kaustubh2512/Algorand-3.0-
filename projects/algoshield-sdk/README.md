# AlgoShield AI SDK

Real-time Algorand smart contract security scanner for developers.

## Install

```bash
npm install algoshield-sdk
```

## Quick Start (Class Style)

```javascript
const AlgoShield = require('algoshield-sdk');

const shield = new AlgoShield({
  apiKey: 'your-api-key',
  walletAddress: 'your-algorand-address' // optional
});

// Scan a raw TEAL string
const result = await shield.scan(contractCode);
```

## Quick Start (Function Style)

```javascript
const { scan } = require('algoshield-sdk');

const result = await scan(contractCode, { apiKey: 'your-api-key' });
```

## Scan a File

```javascript
await shield.scanFile('./contracts/myapp.teal');
```

## Watch Mode

Auto-scan any .teal or .py file in a directory on every save.

```javascript
shield.watch('./contracts');
```

## Silent Mode

Suppress terminal output and just get the result object.

```javascript
const result = await shield.scan(code, { silent: true });
```

## Config Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `apiKey` | string | null | Your AlgoShield API key (required) |
| `apiUrl` | string | `http://localhost:8000` | AlgoShield Backend URL |
| `walletAddress` | string | `sdk-user` | Your wallet address for scan history |
| `verbose` | boolean | `false` | Show more detail for each vulnerability |
| `silent` | boolean | `false` | Suppress all console logging |

## Environment Variables

You can also set these in your `.env` file instead of passing them to the constructor:

- `ALGOSHIELD_API_KEY`
- `ALGOSHIELD_API_URL`

---

🛡️ **AlgoShield AI** — Securing the future of Algorand.
🏆 **Score ≥ 70?** You can mint an official Security Certificate NFT on our dashboard!
