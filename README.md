# Flask API Docker Container

This is a Docker container for a Flask API application.

## Prerequisites

- Docker installed on your system
- MySQL database (local or remote)

## Environment Variables

Create a `.env` file in the same directory as the Dockerfile with the following variables:

```env
DB_NAME=your_database_name
DB_HOST=your_database_host
DB_PASSWORD=your_database_password
DB_PORT=your_database_port
DB_USER=your_database_user
```

## Building the Docker Image

```bash
docker build -t flask-api .
```

## Running the Container

```bash
docker run -d \
  --name flask-api \
  -p 10000:10000 \
  --env-file .env \
  flask-api
```

## Accessing the API

Once the container is running, you can access the API at:

- `http://localhost:10000/api/khachhang` (Customers)
- `http://localhost:10000/api/hoadon` (Invoices)
- `http://localhost:10000/api/nhanvien` (Employees)
- `http://localhost:10000/api/sanpham` (Products)
- And other endpoints as defined in the API

## API Endpoints

### Customers (KhachHang)
- GET /api/khachhang - Get all customers
- POST /api/khachhang - Create a new customer
- PUT /api/khachhang/{id} - Update a customer
- DELETE /api/khachhang/{id} - Delete a customer

### Invoices (HoaDon)
- GET /api/hoadon - Get all invoices
- POST /api/hoadon - Create a new invoice
- PUT /api/hoadon/{id} - Update an invoice
- DELETE /api/hoadon/{id} - Delete an invoice

### Employees (NhanVien)
- GET /api/nhanvien - Get all employees
- POST /api/nhanvien - Create a new employee
- PUT /api/nhanvien/{id} - Update an employee
- DELETE /api/nhanvien/{id} - Delete an employee

### Products (SanPham)
- GET /api/sanpham - Get all products
- POST /api/sanpham - Create a new product
- PUT /api/sanpham/{id} - Update a product
- DELETE /api/sanpham/{id} - Delete a product

## Stopping the Container

```bash
docker stop flask-api
```

## Removing the Container

```bash
docker rm flask-api
```
