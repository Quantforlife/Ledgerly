
# 📊 Ledgerly - Business Management Suite

A modern, feature-rich business management application built with Streamlit, featuring dark/light themes, animated UI, CSV data import/export, and comprehensive business analytics.

## ✨ Features

### 🎨 Modern UI/UX
- **Dark/Light Mode Toggle**: Seamless theme switching with persistent preferences
- **Animated Gradient Backgrounds**: Dynamic, eye-catching gradients that change over time
- **Micro Animations**: Smooth transitions and hover effects throughout the interface
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Glass Morphism**: Modern frosted glass effect with backdrop blur

### 📊 Business Management
- **Sales Tracking**: Record and manage sales transactions with receipt generation
- **Expense Management**: Track business expenses by category with detailed notes
- **Inventory Control**: Manage stock levels with low-stock alerts and thresholds
- **Analytics Dashboard**: Real-time insights with interactive charts and graphs
- **Data Import/Export**: CSV upload/download functionality for bulk operations

### 🔧 Advanced Features
- **Voice Input Simulation**: Mock voice command processing for sales
- **Barcode Support**: Input field for barcode/item code scanning
- **Real-time Alerts**: Low stock warnings and pending receivables notifications
- **Forecasting**: 7-day sales prediction with trend analysis
- **Multi-format Export**: Export data as CSV, Excel formats

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd ledgerly
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

4. **Access the application:**
Open your browser and navigate to `http://localhost:8501`

## 📁 Project Structure

```
ledgerly/
├── app.py                  # Main application entry point
├── main.py                 # Application core logic
├── dashboard.py            # Dashboard and UI components
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── ledgerly/
│   ├── data/              # Database and sample data
│   │   ├── ledgerly.db    # SQLite database
│   │   ├── sample_sales.csv
│   │   ├── sample_inventory.csv
│   │   └── sample_expenses.csv
│   ├── models/            # Database models
│   │   ├── sales_model.py
│   │   ├── expenses_model.py
│   │   ├── stock_model.py
│   │   └── receivables_model.py
│   ├── services/          # Business logic services
│   │   ├── billing_service.py
│   │   ├── stock_service.py
│   │   ├── analytics_service.py
│   │   └── reminder_service.py
│   ├── static/           # CSS and static assets
│   │   └── style.css
│   └── utils/            # Utility functions
│       ├── config.py
│       ├── db.py
│       └── helpers.py
```

## 🎯 Usage Guide

### Dashboard
- View key metrics: Today's Sales, Expenses, Net Profit, Stock Items
- Monitor low stock alerts and pending receivables
- Access quick action buttons for common tasks

### Sales Management
- Add individual sales transactions
- Generate receipts automatically
- Track customer information
- Simulate voice input commands

### Expense Tracking
- Categorize expenses (Fuel, Rent, Salaries, Utilities, Misc)
- Add vendor information and notes
- Track spending patterns

### Inventory Management
- Add/update stock items
- Set low stock thresholds
- Monitor current stock levels with status indicators
- Receive automatic low stock alerts

### Reports & Analytics
- **Sales Analysis**: Top selling items with interactive charts
- **Revenue Trends**: Monthly sales trend visualization
- **Expense Breakdown**: Pie chart of expense categories
- **Forecasting**: 7-day sales prediction

### Data Import/Export
- **CSV Import**: Bulk upload sales, inventory, and expense data
- **Format Validation**: Automatic validation of CSV structure
- **Data Preview**: View uploaded data before processing
- **Export Options**: Download reports in CSV format

## 🎨 Theme Customization

The application supports both light and dark themes:

- **Light Mode**: Clean white background with pastel accents
- **Dark Mode**: Deep navy background with neon accents
- **Theme Toggle**: Located in the top-right corner (🌞/🌙)
- **Persistent Preferences**: Theme choice is saved in session state

## 📊 Database Schema

### Sales Table
- id (Primary Key)
- item (Product name)
- qty (Quantity sold)
- unit_price (Price per unit)
- total (Total amount)
- customer (Customer name)
- date (Transaction date)

### Stock Table
- id (Primary Key)
- item (Product name, Unique)
- qty (Current quantity)
- threshold (Low stock threshold)
- unit_cost (Cost per unit)
- last_updated (Last update date)

### Expenses Table
- id (Primary Key)
- category (Expense category)
- vendor (Vendor/supplier)
- amount (Expense amount)
- date (Expense date)
- notes (Additional notes)

### Receivables Table
- id (Primary Key)
- customer (Customer name)
- amount (Amount due)
- due_date (Due date)
- status (Payment status)

## 🔧 Configuration

### Environment Variables
- `DB_PATH`: Database file path (default: ledgerly/data/ledgerly.db)
- `CURRENCY_SYMBOL`: Currency symbol (default: ₹)
- `DATE_FORMAT`: Date format (default: %Y-%m-%d)

### CSV Import Formats

#### Sales CSV Format
```csv
item,qty,unit_price,customer
Sugar,10,45.50,John Doe
Rice,5,120.00,Jane Smith
```

#### Inventory CSV Format
```csv
item,qty,threshold,unit_cost
Sugar,100,10,40.00
Rice,50,5,110.00
```

#### Expenses CSV Format
```csv
category,vendor,amount,notes
Fuel,Gas Station ABC,2500.00,Monthly fuel expenses
Rent,Property Manager,15000.00,Store rent
```

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

### Production Deployment
```bash
streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🧪 Testing

### Load Sample Data
1. Navigate to Settings → Sample Data Management
2. Click "Load Sample Data" to populate the database with test data
3. Explore all features with realistic sample data

### CSV Import Testing
1. Use the sample CSV files in `ledgerly/data/`
2. Navigate to Settings → Data Import/Export
3. Upload and test the import functionality

## 🔒 Security Considerations

- **Input Validation**: All user inputs are validated and sanitized
- **SQL Injection Protection**: Using SQLAlchemy ORM for database operations
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Data Backup**: Regular database backups recommended for production

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure the data directory exists
   - Check file permissions
   - Verify SQLite installation

2. **CSV Import Failures**
   - Validate CSV format matches requirements
   - Check for special characters in data
   - Ensure proper encoding (UTF-8)

3. **Theme Not Persisting**
   - Clear browser cache
   - Check session state configuration
   - Restart the application

## 📈 Performance Optimization

- **Database Indexing**: Key fields are indexed for faster queries
- **Lazy Loading**: Charts and data load on demand
- **Caching**: Streamlit caching for expensive operations
- **Responsive Design**: Optimized for various screen sizes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Streamlit**: For the amazing framework
- **Plotly**: For interactive charts and visualizations
- **SQLAlchemy**: For robust database operations
- **Inter Font**: For beautiful typography

## 📞 Support

For support, email support@ledgerly.com or create an issue in the repository.

---

**Made with ❤️ using Streamlit**
