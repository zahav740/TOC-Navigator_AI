# Phase 1 Backlog

## Orders CRUD
- Create order model and database migration
- Implement REST endpoints for listing, retrieving, creating, updating and deleting orders
- Validate payloads with Pydantic schemas
- Add pagination and filtering to order list endpoint
- Write tests for orders API

## Operators CRUD
- Define operator model and migration
- Endpoints for CRUD operations on operators
- Associate orders with operators
- Add authentication placeholder for operator actions
- Tests for operators API

## Excel Import
- Endpoint to upload Excel files
- Parse spreadsheet into order records using pandas
- Provide validation errors back to the user
- Store uploaded files temporarily
- Tests covering successful and failed imports

