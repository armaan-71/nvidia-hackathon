# Scout 🛰️

**Scout** is an autonomous funding assistant designed to help nonprofits discover, evaluate, and apply for grant opportunities. This frontend MVP allows judges and stakeholders to visualize the AI-driven grant matching experience.

## ✨ Features

- **Mission Dashboard**: Holistic view of nonprofit profile, focus areas, and funding stats.
- **Autonomous Grant Finder**: Smart matching system with transparency into reasoning, strengths, and risks.
- **Match Reasoning**: Explainable AI panels that break down *why* a grant fits your mission.
- **Submission Timelines**: Dynamic checklists to guide nonprofits through the application process.
- **Agent Chat**: A split-screen AI workbench for querying documents and grant data.

## 🚀 Tech Stack

- **Framework**: [Next.js 14+](https://nextjs.org/) (App Router)
- **Language**: [TypeScript](https://www.typescriptlang.org/)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **Data Handling**: Simulated Async API layer (Promises)
- **Deployment**: Optimized for [Vercel](https://vercel.com/)

## 🛠️ Getting Started

### 1. Installation
Navigate to the `scout` directory and install dependencies:
```bash
cd scout
npm install
```

### 2. Development
Run the local development server:
```bash
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) (or the port indicated in your terminal) to see the result.

### 3. Build
Generate a production-ready build:
```bash
npm run build
```

## 📂 Project Structure

- `app/`: Next.js App Router pages and layouts.
- `components/`: Reusable UI components (Navbar, Cards, etc.).
- `lib/`:
    - `types.ts`: TypeScript interfaces for the data model.
    - `mockData.ts`: Semantic demo data for the hackathon.
    - `api.ts`: **The Integration Point.** Service layer that currently serves mock data.

## 🔗 Backend Integration

To connect the real **FastAPI** backend (RAG pipeline, analyzer agents):

1. Go to `lib/api.ts`.
2. Replace the simulated Promises with standard `fetch` or `axios` calls to your FastAPI endpoints:
    - `POST /chat`
    - `GET /grants`
    - `POST /ingest`

The UI components are already built to handle asynchronous states (loading skeletons, etc.), so the transition will be seamless.

---
*Built for the NVIDIA AI Hackathon.*
