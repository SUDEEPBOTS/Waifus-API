const WaifuClient = require('../clients/javascript/waifus.js');

async function main() {
  console.log('🌸 Initializing WaifuClient...');
  const client = new WaifuClient();

  // 1. Ping
  const ping = await client.ping();
  console.log('📡 Ping:', ping.message);

  // 2. Stats
  const stats = await client.stats();
  console.log(`📊 Total Waifus: ${stats.total_records} (${stats.database})`);

  // 3. Random Gacha
  console.log('\n🎲 Rolling Random Waifu...');
  const random = await client.random();
  console.log(`   Character: ${random.data.name}`);
  console.log(`   Rarity:    ${random.data.rarity}`);
  console.log(`   Image URL: ${random.data.img_url}`);

  // 4. Search
  console.log('\n🔍 Searching for "Komi"...');
  const search = await client.findByName('Komi');
  const items = Array.isArray(search.data) ? search.data : [search.data];
  if (items[0]) {
    console.log(`   Found: ${items[0].name} [${items[0].rarity}]`);
  }
}

main().catch(console.error);
