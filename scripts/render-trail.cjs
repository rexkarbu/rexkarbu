// Adapt a real, saved public calendar to Platane/snk's GraphQL input shape.
// The upstream bundle is verified by update-activity.py before this process runs.
const fs = require('node:fs');
const path = require('node:path');

const [snapshotFile, bundleFile, outputFile] = process.argv.slice(2);
if (!snapshotFile || !bundleFile || !outputFile) {
  throw new Error('Usage: node render-trail.cjs snapshot.json verified-bundle.cjs output.svg');
}
const snapshot = JSON.parse(fs.readFileSync(snapshotFile, 'utf8'));
const levels = ['NONE', 'FIRST_QUARTILE', 'SECOND_QUARTILE', 'THIRD_QUARTILE', 'FOURTH_QUARTILE'];
const weeks = [];
for (const day of snapshot.calendar.days) {
  const weekday = new Date(`${day.date}T00:00:00Z`).getUTCDay();
  if (!weeks.length || weekday === 0) weeks.push({ contributionDays: [] });
  weeks.at(-1).contributionDays.push({
    date: day.date,
    weekday,
    contributionCount: day.count,
    contributionLevel: levels[day.level],
  });
}

// No token and no live network access are needed by the renderer. Dates, counts,
// and levels are copied unchanged; this is a data adapter, not synthetic activity.
globalThis.fetch = async (url, options) => {
  const body = JSON.parse(options.body);
  if (String(url) !== 'https://api.github.com/graphql' ||
      body.variables?.login !== 'rexkarbu' ||
      !body.query?.includes('contributionCalendar')) {
    throw new Error('Unexpected renderer network request');
  }
  return new Response(JSON.stringify({ data: { user: {
    contributionsCollection: { contributionCalendar: { weeks } },
  } } }), { status: 200, headers: { 'Content-Type': 'application/json' } });
};
delete process.env.GITHUB_TOKEN;
delete process.env.GH_TOKEN;
process.env.INPUT_GITHUB_TOKEN = '';
process.env.INPUT_GITHUB_USER_NAME = 'rexkarbu';
process.env.INPUT_GIF_OUT_PATH = '';
process.env.INPUT_SVG_OUT_PATH = '';
process.env.INPUT_OUTPUTS = path.resolve(outputFile).replaceAll('\\', '/') +
  '?color_snake=%23E5B567&color_dots=%2317243A,%23344943,%235A7968,%237F9F8B,%239DB7A5&color_dot_border=%230D1117';
require(path.resolve(bundleFile));
