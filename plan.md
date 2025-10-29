# AI & ML Research Blog - PostgreSQL Migration with RBAC System

## Phase 1: Database Schema Setup ✅
- [x] Create comprehensive PostgreSQL schema with User, Role, Permission tables
- [x] Add RBAC (Role-Based Access Control) link tables
- [x] Create SQL migration script for all tables
- [x] Include User model with privacy settings and phone number

## Phase 2: Update Models and Database Connection
- [ ] Create new SQLModel models matching the PostgreSQL schema
- [ ] Update database session configuration to use PostgreSQL
- [ ] Add proper relationships between User, Role, and Permission models
- [ ] Update existing Article, Author, Category models to use serial IDs instead of UUIDs
- [ ] Create link models for many-to-many relationships

## Phase 3: Update API Endpoints and State
- [ ] Update authentication endpoints to work with new User model
- [ ] Add user contacts and privacy settings endpoints
- [ ] Update article endpoints to use PostgreSQL connection
- [ ] Test all CRUD operations with PostgreSQL
- [ ] Update frontend state to handle new data structure

---

**Current Task:** Setting up PostgreSQL schema with User RBAC system
