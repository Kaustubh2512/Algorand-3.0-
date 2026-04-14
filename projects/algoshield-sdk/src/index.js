const { scanContract, scanFile } = require('./scanner');
const { formatResult, printError } = require('./formatter');

class AlgoShield {
  constructor(config = {}) {
    this.config = {
      apiKey:        config.apiKey        || process.env.ALGOSHIELD_API_KEY || 'demo-key-123',
      apiUrl:        config.apiUrl        || process.env.ALGOSHIELD_API_URL || 'http://localhost:8000',
      walletAddress: config.walletAddress || 'sdk-user',
      silent:        config.silent        || false,
    };
  }

  async scan(contractCode) {
    try {
      const r = await scanContract(contractCode, this.config);
      if (!this.config.silent) console.log(formatResult(r));
      return r;
    } catch (e) { if (!this.config.silent) printError(e); throw e; }
  }

  async scanFile(filePath) {
    try {
      const r = await scanFile(filePath, this.config);
      if (!this.config.silent) console.log(formatResult(r, filePath));
      return r;
    } catch (e) { if (!this.config.silent) printError(e); throw e; }
  }
}

module.exports = AlgoShield;
module.exports.scan     = (code, opts) => new AlgoShield(opts).scan(code);
module.exports.scanFile = (fp, opts)   => new AlgoShield(opts).scanFile(fp);
