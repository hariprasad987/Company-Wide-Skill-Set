# Angular Stimulated Task: Team Pulse Dashboard

An interactive Angular dashboard for monitoring a small team's availability and workload.

## Features

- Live team, availability, task, and capacity metrics
- Filter members by availability
- Toggle a member between Available and Focused
- Add new members using a validated form
- Responsive desktop and mobile layout

## Run the project

Angular 21 requires Node.js 20.19 or newer. From this folder, run:

```bash
source /root/.nvm/nvm.sh
nvm use 20.19.5
npm install
npm start
```

Open http://localhost:4200 in your browser.

## Verify

```bash
npm test -- --watch=false
npm run build
```
