# CampusFind Frontend

## Setup Instructions

### Prerequisites
- Node.js 18+
- npm

### Installation

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env.local
   ```

3. **Run development server**
   ```bash
   npm run dev
   ```

The frontend will be available at: `http://localhost:5173`

### Building

```bash
npm run build
```

Output will be in the `dist/` directory.

### Running Tests

```bash
npm run test:unit
```

### Project Structure

```
frontend/
├── src/
│   ├── pages/           # Page components
│   ├── components/      # Reusable components
│   ├── services/        # API services
│   ├── stores/          # Zustand state management
│   ├── styles/          # Global styles
│   ├── App.tsx          # Main app component
│   └── main.tsx         # Entry point
├── index.html
├── vite.config.ts
├── tailwind.config.js
├── postcss.config.js
├── package.json
└── README.md
```

### Key Dependencies

- **React 18**: UI library
- **React Router v6**: Client-side routing
- **Axios**: HTTP client
- **Zustand**: State management
- **Tailwind CSS**: Utility-first CSS framework
- **Vite**: Build tool and dev server

### Environment Variables

Create a `.env.local` file:

```
VITE_API_URL=http://localhost:8000/api
```

### Pages

- `/login` - User login
- `/register` - User registration
- `/dashboard` - Main dashboard (found/lost items)
- `/search` - Search and filter items
- `/items/:id` - Item detail and claim
- `/admin` - Admin dashboard (pending claims, audit logs)

### Authentication

- Login credentials are stored in `localStorage`
- JWT tokens are used for API authentication
- Automatic token refresh on 401 responses
- Logout clears all stored tokens and user data

### Building for Production

```bash
npm run build
# Output will be in dist/
```

Then serve the `dist/` folder with a web server.

### Docker

```bash
docker build -t campusfind-frontend .
docker run -p 3000:3000 campusfind-frontend
```

### Common Issues

**API not responding**: Make sure backend is running on port 8000
**Module not found**: Run `npm install`
**Port 5173 in use**: Change in vite.config.ts or kill process on that port
