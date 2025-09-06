# Roots Admin Dashboard

A modern React admin dashboard for managing the Roots vegetable store, built with Vite, React, and integrated with the FastAPI backend.

## Features

- **Authentication System**: Secure login/logout with JWT tokens
- **Dashboard Overview**: Key metrics, recent orders, and quick actions
- **Product Management**: Add, edit, delete, and manage vegetable inventory
- **Order Management**: View orders, update status, and track customer information
- **WhatsApp Integration**: Send individual messages and broadcasts to customers
- **Analytics**: Sales trends, product performance, and business insights
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Running FastAPI backend (see main README)

### Installation

1. Navigate to the admin dashboard directory:

```bash
cd admin-dashboard
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

The dashboard will be available at `http://localhost:3000`

### Login Credentials

Use these demo credentials to access the admin dashboard:

- **Username**: `admin`
- **Password**: `admin123`

### Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Project Structure

```
admin-dashboard/
├── src/
│   ├── components/
│   │   ├── Layout.jsx          # Main layout with sidebar navigation
│   │   └── ProtectedRoute.jsx  # Route protection component
│   ├── contexts/
│   │   └── AuthContext.jsx     # Authentication context
│   ├── pages/
│   │   ├── Login.jsx           # Login page
│   │   ├── Dashboard.jsx       # Overview dashboard
│   │   ├── Products.jsx        # Product management
│   │   ├── Orders.jsx          # Order management
│   │   ├── WhatsApp.jsx        # WhatsApp messaging
│   │   └── Analytics.jsx       # Business analytics
│   ├── services/
│   │   └── api.js              # API service layer
│   ├── App.jsx                 # Main app component
│   ├── main.jsx                # App entry point
│   └── index.css               # Global styles
├── package.json
├── vite.config.js              # Vite configuration
└── README.md
```

## API Integration

The dashboard connects to the FastAPI backend through a proxy configuration in `vite.config.js`. All API calls are routed through `/api/*` and forwarded to `http://localhost:8000`.

### Available API Endpoints

- **Authentication**: `/api/auth/*` (login, verify, logout)
- **Products**: `/api/catalog` (GET, POST, PUT, DELETE)
- **Orders**: `/api/orders` (GET, POST)
- **WhatsApp**: `/api/whatsapp/*` (webhook, send messages)
- **Health**: `/api/health` (GET)

## Key Features

### Authentication

- Secure JWT-based authentication
- Login/logout functionality
- Protected routes
- Automatic token refresh
- User session management

### Dashboard

- Real-time statistics (total products, orders, revenue)
- Recent orders overview
- Quick action buttons

### Product Management

- Add new products with name, description, price, unit
- Edit existing products
- Delete products
- Stock status management
- Responsive product grid

### Order Management

- View all orders with filtering by status
- Order details modal with item breakdown
- Status updates (new → confirmed → preparing → ready → delivered)
- Customer information display

### WhatsApp Integration

- Send individual messages to customers
- Broadcast messages to all customers
- Quick message templates
- Customer list with contact information
- Message history (when implemented)

### Analytics

- Revenue trends (last 7 days)
- Order status distribution
- Top-selling products
- Business insights and recommendations
- Interactive charts using Recharts

## Styling

The dashboard uses a custom CSS framework with:

- Modern, clean design
- Responsive grid system
- Status badges and indicators
- Hover effects and transitions
- Mobile-first approach

## Development

### Adding New Features

1. Create new components in `src/components/`
2. Add new pages in `src/pages/`
3. Update the navigation in `Layout.jsx`
4. Add API endpoints in `src/services/api.js`
5. Update routing in `App.jsx`

### Styling Guidelines

- Use the existing CSS classes for consistency
- Follow the color scheme (green primary, blue secondary)
- Ensure responsive design for all screen sizes
- Use Lucide React icons for consistency

## Deployment

### Vercel/Netlify

1. Build the project: `npm run build`
2. Deploy the `dist` folder
3. Update API proxy configuration for production

### Docker

```dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

## Troubleshooting

### Common Issues

1. **API Connection Failed**: Ensure the FastAPI backend is running on port 8000
2. **Build Errors**: Check Node.js version and dependencies
3. **Styling Issues**: Verify CSS classes are properly imported

### Development Tips

- Use browser dev tools to debug API calls
- Check the Network tab for failed requests
- Use React DevTools for component debugging
- Monitor console for JavaScript errors

## Contributing

1. Follow the existing code style
2. Add proper error handling
3. Include loading states for async operations
4. Test on multiple screen sizes
5. Update documentation for new features

## License

This project is part of the Roots vegetable store management system.
