#!/usr/bin/env node
const path = require('path');
const AlgoShield = require('../src/index');
const chalk = require('chalk');

const args = process.argv.slice(2);
const command = args[0];
const target = args[1] || '.';

const shield = new AlgoShield();

async function run() {
  if (command === 'scan') {
    if (target.endsWith('.teal')) {
      await shield.scanFile(target);
    } else {
      console.error(chalk.red('Please provide a .teal file to scan.'));
      process.exit(1);
    }
  } else if (command === 'watch') {
    shield.watch(target);
  } else {
    console.log(chalk.bold.cyan('\n🛡️  AlgoShield AI — Developer CLI\n'));
    console.log('Usage:');
    console.log('  algoshield scan <file.teal>    Analyze a smart contract');
    console.log('  algoshield watch <dir>         Monitor directory for changes');
    console.log('\nOptions:');
    console.log('  --api-key <key>                Set your API key');
    console.log('');
  }
}

run().catch(() => process.exit(1));
