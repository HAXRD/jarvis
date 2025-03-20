# Project overview
You are building a LLM chat platform, where the overall user experience is very much like ChatGPT.
The platform consists of a frontend webpage and a backend server.

# Architecture overview
## frontend
- Built with NextJS 15, shadcn, tailwind, Lucid icon
- Using WebSockets (Tornado) for realt-time LLM interactions.
- REST APIs (Flask) for user management, data fetching, and non-realtime tasks.

## backend services
- Tornado (Python): Handles WebSocket connections for streaming LLM responses and real-time updates.
- Flask (Python): Manages RESTful APIs for authentication, user profiles, and business logic.
- LLM Inference Service: Will be using a third-party API for model inference, such as Qwen by Alibaba.

## database
- PostgreSQL: Stores user management, preferences, and chat history.

# Integration Workflow
## Realtime Interaction
- Frontend <-> Tornado (WebSocket):
  - Users send prompts via WebSocket
  - Tornado streams responses from the LLM service back to the frontend
## User management && CRUD
- Frontend <-> Flask (RESTful API):
  - Handles login, registration, and profile updates via Flask endpoints.
  - Stores chat history, preferences, etcs, in a database.
## LLM Processing
- Tornado <-> LLM Service:
  - Tornado forwards user prompts to the LLM service via HTTP/RPC.
  - LLM returns generated text, which Tornado streams to the frontend.

# Cross-Service Communication
- Auth: JWT tokens issued by Flask, validated across all services.

# Deployment & DevOps
- Containerization: Dockerize each service (Tornado, Flask)
- Orchestration: Use Kubernetes for scaling and management (for now, only using a small number of pods for scaling demo purpose)
- API Gateway: Use nginx routes request, handle SSL and rate limiting.
- Monitoring: Centralized logging (ELK) and metrics (Prometheus/Grafna)

# Example Flow
1. User submits a prompt via WebSocket (Tornado)
2. Tornado sends the prompt to the LLM Inference Service
3. LLM processes the request and streams tokens back to Tornado
4. Tornado forwards tokens to the frontend in realtime
5. After completion, Tornado logs the interaction via Flask's API

# Doc

# Current file structure

/
├── frontend/                      # Next.js frontend application
│   ├── app/                      # Next.js app directory
│   │   ├── (auth)/              # Authentication routes
│   │   │   ├── login/
│   │   │   └── register/
│   │   ├── chat/                # Chat interface
│   │   └── settings/            # User settings
│   ├── components/              # Reusable React components
│   │   ├── chat/               
│   │   │   ├── ChatInput.tsx
│   │   │   ├── ChatMessage.tsx
│   │   │   └── ChatWindow.tsx
│   │   ├── ui/                  # UI components (shadcn)
│   │   └── shared/              # Shared components
│   ├── lib/                     # Utility functions and configs
│   │   ├── websocket.ts        # WebSocket client
│   │   └── api.ts              # REST API client
│   └── styles/                  # Global styles
│
├── backend/                      # Backend services
│   ├── tornado_server/          # WebSocket server
│   │   ├── handlers/           
│   │   ├── services/
│   │   └── main.py
│   │
│   ├── flask_server/           # REST API server
│   │   ├── routes/
│   │   ├── models/
│   │   ├── services/
│   │   └── app.py
│   │
│   └── shared/                 # Shared utilities between services
│       ├── config/
│       ├── database/
│       └── utils/
│
├── deployment/                  # Deployment configurations
│   ├── docker/
│   │   ├── frontend.Dockerfile
│   │   ├── tornado.Dockerfile
│   │   └── flask.Dockerfile
│   ├── kubernetes/
│   │   ├── frontend.yaml
│   │   ├── tornado.yaml
│   │   └── flask.yaml
│   └── nginx/
│       └── nginx.conf
│
├── docs/                       # Documentation
│   ├── api/
│   ├── deployment/
│   └── development/
│
└── scripts/                    # Development and deployment scripts
    ├── setup.sh
    └── deploy.sh