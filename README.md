# GitHub Analytics

A monorepo project built with Nx, containing a FastAPI backend and React frontend to create charts based on the user natural language input

Este proyecto consta de 4 agentes un supervisor, un arquetecto un analista y un desarrollador 

el supervisor es el encargado de supervisar u orqeustar el funcionamiento de los otros 3 agentes
el arquitecto

## Tech Stack

### Backend

- FastAPI
- LangChain + Azure OpenAI for AI agents
- Poetry for Python dependency management
- Pytest for testing
- Ruff for linting

### Frontend

- React 18
- TypeScript
- Tailwind CSS
- Recharts for data visualization
- Vite for building
- Vitest for testing

## Prerequisites

- Node.js (v18+)
- Python (v3.11+)
- Poetry for Python dependency management
- pnpm (recommended) or npm
- Azure OpenAI API access

## Project Structure

```
apps/
├── backend/ # FastAPI backend application
│ ├── src/ # Source code
└── frontend/ # React frontend application
│ ├── src/ # Source code
```

## Setup

1. Install Nx globally (optional but recommended):

```sh
npm install -g @nx/cli
```

2. Install project dependencies:

```sh
pnpm install
cd apps/backend && poetry install
```

3. Configure environment variables:

   - Copy `apps/backend/.env.dist` to `apps/backend/.env`
   - Set the following required variables:
     ```
     AZURE_OPENAI_API_KEY=your_api_key
     AZURE_OPENAI_ENDPOINT=your_endpoint
     AZURE_OPENAI_DEPLOYMENT=your_deployment
     CODEGEN_GH_AUTH=your_github_token
     ```

## Running the Project

To run both frontend and backend simultaneously:

```sh
pnpm nx run-many -t serve
```

## Contact

You can find me on:

- LinkedIn: [Luis Duvan Fernando Pinto Diaz](https://www.linkedin.com/in/duvanfernandopintodiaz/)
- Email: duvanpidi@hotmail.com
>>>>>>> c1c847d (feat(project): GitHub Analytics project setup)
