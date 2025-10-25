# AI & ML Research Blog

A full-stack web application for publishing and browsing AI and Machine Learning research articles, built with Reflex (Python) and FastAPI.

## 🏗️ Project Architecture

### Tech Stack
- **Frontend**: Reflex (Python-based reactive UI framework)
- **Backend**: FastAPI (RESTful API)
- **Database**: SQLite with SQLModel ORM
- **Authentication**: JWT tokens with role-based access control
- **Styling**: Tailwind CSS

### Project Structure

app/
├── api/                    # FastAPI REST API
│   ├── deps.py            # Dependency injection (DB session)
│   └── v1/                # API version 1
│       ├── api.py         # Router aggregation
│       └── endpoints/     # API endpoints by resource
│           ├── articles.py
│           ├── authors.py
│           ├── categories.py
│           ├── tags.py
│           ├── users.py
│           └── login.py
│
├── core/                   # Core configurations
│   ├── config.py          # App settings (JWT, API prefix)
│   └── security.py        # Password hashing, JWT tokens
│
├── db/                     # Database layer
│   ├── session.py         # SQLAlchemy engine & session
│   └── init_db.py         # DB initialization & seed data
│
├── models/                 # SQLModel database models
│   ├── article.py         # Article model & schemas
│   ├── author.py          # Author model & schemas
│   ├── category.py        # Category model & schemas
│   ├── tag.py             # Tag model & schemas
│   └── user.py            # User model & authentication
│
├── pages/                  # Reflex frontend pages
│   └── articles.py        # Articles listing page
│
├── states/                 # Reflex state management
│   └── articles_state.py  # Article fetching & filtering logic
│
├── components/             # Reusable UI components
│   └── article_card.py    # Article card component
│
└── app.py                  # Main application entry point


## 📊 Database Schema

### Core Entities

**Author**
- `id` (UUID, PK)
- `name` (str, indexed)
- `bio` (str, optional)
- Relationship: One-to-Many with Articles

**Category**
- `id` (UUID, PK)
- `name` (str, unique, indexed)
- `description` (str, optional)
- Relationship: One-to-Many with Articles

**Article**
- `id` (UUID, PK)
- `title` (str)
- `content` (str)
- `published_at` (datetime, optional)
- `author_id` (UUID, FK → Author)
- `category_id` (UUID, FK → Category)
- Relationship: Many-to-Many with Tags

**Tag**
- `id` (UUID, PK)
- `name` (str, unique, indexed)
- `description` (str, optional)
- Relationship: Many-to-Many with Articles via ArticleTagLink

**User** (Authentication)
- `id` (UUID, PK)
- `email` (str, unique, indexed)
- `full_name` (str, optional)
- `hashed_password` (str)
- `is_active` (bool)
- `role` (enum: admin, author, reader)

### Relationships
- **Author ↔ Article**: One author can write many articles
- **Category ↔ Article**: One category can contain many articles
- **Article ↔ Tag**: Many-to-many relationship through ArticleTagLink

## 🔌 API Endpoints

### Authentication
- `POST /api/v1/login/access-token` - Login with email/password, get JWT token

### Users
- `POST /api/v1/users/` - Register new user

### Articles
- `GET /api/v1/articles/` - List articles (with filtering by category, tags, search)
- `POST /api/v1/articles/` - Create article (requires auth)
- `GET /api/v1/articles/{id}` - Get specific article with details
- `PATCH /api/v1/articles/{id}` - Update article (requires auth)
- `DELETE /api/v1/articles/{id}` - Delete article (requires auth)

### Authors
- `GET /api/v1/authors/` - List all authors
- `POST /api/v1/authors/` - Create author
- `GET /api/v1/authors/{id}` - Get author with articles
- `PATCH /api/v1/authors/{id}` - Update author
- `DELETE /api/v1/authors/{id}` - Delete author

### Categories
- `GET /api/v1/categories/` - List all categories
- `POST /api/v1/categories/` - Create category
- `GET /api/v1/categories/{id}` - Get specific category
- `PATCH /api/v1/categories/{id}` - Update category
- `DELETE /api/v1/categories/{id}` - Delete category

### Tags
- `GET /api/v1/tags/` - List all tags
- `POST /api/v1/tags/` - Create tag
- `GET /api/v1/tags/{id}` - Get tag with articles
- `PATCH /api/v1/tags/{id}` - Update tag
- `DELETE /api/v1/tags/{id}` - Delete tag

## 🎨 Frontend Pages

### Current Pages
1. **Homepage** (`/`) - Welcome page with navigation to articles and API docs
2. **Articles Listing** (`/articles`) - Browse articles with search and category filtering

### Frontend State Management
- `ArticleState` - Manages article fetching, search, filtering, and loading states
- Uses Reflex's reactive state system with background events for async API calls

## 🔐 Authentication & Authorization

### Security Features
- **Password Hashing**: SHA256 with random salt
- **JWT Tokens**: HS256 algorithm, 8-day expiration
- **Role-Based Access Control (RBAC)**: 
  - `admin` - Full access
  - `author` - Can create/edit articles
  - `reader` - Read-only access

### Test Credentials (from seed data)
- Admin: admin@aimlblog.com / AdminPass123!
- Author: author@aimlblog.com / AuthorPass123!
- Reader: reader@aimlblog.com / ReaderPass123!

## 🚀 Data Flow

### Article Listing Flow
1. User visits `/articles` page
2. `ArticleState.fetch_articles_and_categories()` is triggered on mount
3. State makes async HTTP requests to FastAPI endpoints:
   - `GET /api/v1/articles/` (with optional filters)
   - `GET /api/v1/categories/`
4. FastAPI routes to `articles.py` and `categories.py` endpoints
5. Endpoints use dependency injection to get DB session from `deps.py`
6. SQLModel ORM queries database with proper joins
7. Results serialized to JSON using Pydantic models
8. State updates with response data
9. Reflex re-renders UI components with new data

### Search & Filter Flow
1. User types in search box → `set_search_query()` with 300ms debounce
2. User selects category → `set_selected_category()`
3. Both trigger `fetch_articles_and_categories()` with updated params
4. API endpoint filters results using SQLModel WHERE clauses
5. UI updates reactively with filtered articles

## 📝 API Documentation

### Access Points
- **Swagger UI**: http://localhost:8000/docs (or /api/v1/docs on deployed version)
- **ReDoc**: http://localhost:8000/redoc (or /api/v1/redoc on deployed version)
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🛠️ Development Workflow

### Running Locally
bash
# Install dependencies
pip install -r requirements.txt

# Run development server
reflex run

# Access the app
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs


### Database Initialization
The database is automatically initialized on app startup:
1. `create_db_and_tables()` creates all SQLModel tables
2. `create_initial_data()` seeds test data if tables are empty

## 🗺️ Project Roadmap

### ✅ Completed (Phase 1-3)
- [x] Complete CRUD API for articles, authors, categories, tags
- [x] User authentication with JWT
- [x] Role-based access control
- [x] Article listing frontend with search & filtering
- [x] Responsive UI with Tailwind CSS
- [x] Database initialization with seed data

### 🎯 Next Steps (Phase 4-6)

#### Phase 4: Article Detail Page & Comments
- [ ] Create article detail page (`/articles/{id}`)
- [ ] Add markdown rendering for article content
- [ ] Implement comment system (CRUD endpoints + UI)
- [ ] Add related articles sidebar
- [ ] Social sharing buttons

#### Phase 5: Author & Category Pages
- [ ] Author profile pages with bio and article list
- [ ] Category pages with filtered articles
- [ ] Tag cloud visualization
- [ ] Author statistics (article count, views)

#### Phase 6: Admin Dashboard
- [ ] Protected admin dashboard (`/admin`)
- [ ] Article management interface (create, edit, delete)
- [ ] User management interface
- [ ] Analytics dashboard (views, popular articles)
- [ ] Content moderation tools

### 🔮 Future Enhancements
- [ ] Rich text editor for article creation
- [ ] Image upload for article thumbnails
- [ ] User profiles and preferences
- [ ] Bookmarking/favorites system
- [ ] Email notifications for new articles
- [ ] RSS feed generation
- [ ] Full-text search with ranking
- [ ] Article versioning/revision history
- [ ] Multi-language support
- [ ] Dark mode toggle

## 🏛️ Architecture Decisions

### Why Reflex?
- **Python-only stack**: No need for separate frontend framework
- **Reactive UI**: Automatic re-rendering on state changes
- **Type safety**: Full Python type hints throughout

### Why FastAPI for API layer?
- **Separation of concerns**: Clear API contracts independent of frontend
- **API-first design**: Can be consumed by mobile apps, other frontends
- **Auto-generated docs**: OpenAPI/Swagger out of the box
- **Performance**: Async/await support, fast JSON serialization

### Why SQLModel?
- **Type safety**: Pydantic models + SQLAlchemy ORM
- **Code reuse**: Same models for DB tables and API schemas
- **Migration friendly**: Can switch to Alembic for migrations later

## 📚 Key Patterns

### Dependency Injection

# All endpoints use DI for database session
def get_articles(session: Session = Depends(get_session)):
    ...


### Pydantic Schemas

# Separate schemas for different operations
ArticleBase → Article (DB) → ArticleCreate, ArticleRead, ArticleUpdate


### Background Events

# Async API calls don't block UI
@rx.event(background=True)
async def fetch_articles_and_categories(self):
    async with self:  # Lock state during updates
        ...


## 🐛 Known Issues
- Database initialization requires app restart on fresh deployment
- No pagination UI yet (API supports it via offset/limit)
- Search is case-sensitive (can be improved with full-text search)

## 📄 License
[Your License Here]

## 🤝 Contributing
[Contributing Guidelines Here]
