from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import sqlite3
import csv
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'database_explorer_secret_key_render')

# Use environment variable for database path or default to local
DATABASE = os.environ.get('DATABASE_PATH', 'database_explorer.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    conn = get_db_connection()
    
    # Domain Cost table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS domain_cost (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT,
            kw TEXT,
            type TEXT,
            team TEXT,
            owner TEXT,
            end_date TEXT,
            plan TEXT,
            cost REAL,
            month TEXT
        )
    ''')
    
    # Hosting Cost table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS hosting_cost (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month_registration TEXT,
            month_expire TEXT,
            domain TEXT,
            team TEXT,
            sum_hosting_cost_by_domain REAL
        )
    ''')
    
    # Performance table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT,
            team TEXT,
            owner TEXT,
            plan TEXT,
            end_date TEXT,
            cashgame TEXT,
            chalong TEXT,
            playgame TEXT,
            total_register INTEGER,
            total_topup INTEGER,
            regis_may INTEGER,
            topup_may INTEGER,
            regis_june INTEGER,
            topup_june INTEGER,
            regis_july INTEGER,
            topup_july INTEGER,
            cvr TEXT,
            first_seen_cg TEXT,
            first_seen_cl TEXT,
            first_seen_pg TEXT,
            date_gap TEXT,
            unique_visits INTEGER
        )
    ''')
    
    # Revenue table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS revenue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT,
            month TEXT,
            owner TEXT,
            team TEXT,
            web TEXT,
            win_loss REAL,
            rename TEXT,
            reteam TEXT
        )
    ''')
    
    # Salary table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS salary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT,
            salary REAL,
            team TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def import_initial_data():
    """Import CSV data only if tables are empty"""
    conn = get_db_connection()
    
    # Check if data already exists
    domain_count = conn.execute('SELECT COUNT(*) FROM domain_cost').fetchone()[0]
    if domain_count > 0:
        print("Database already has data, skipping initial import.")
        conn.close()
        return
    
    print("Importing initial CSV data...")
    
    # Sample data for initial deployment
    sample_domain_data = [
        ('example.com', 'sample', 'Sample Type', 'Sample Team', 'Sample Owner', '1 Jan 2025', 'A', 100.0, 'Jan 2025'),
        ('demo.com', 'demo', 'Demo Type', 'Demo Team', 'Demo Owner', '1 Feb 2025', 'B', 200.0, 'Feb 2025')
    ]
    
    sample_hosting_data = [
        ('Jan 2025', 'Jan 2026', 'example.com', 'Sample Team', 50.0),
        ('Feb 2025', 'Feb 2026', 'demo.com', 'Demo Team', 75.0)
    ]
    
    sample_performance_data = [
        ('example.com', 'Sample Team', 'Sample Owner', 'A', '1 Jan 2025', 'sample123', 'sample123', 'sample123', 10, 5, 2, 1, 3, 2, 5, 2, '10%', '', '', '', '', 25),
        ('demo.com', 'Demo Team', 'Demo Owner', 'B', '1 Feb 2025', 'demo456', 'demo456', 'demo456', 20, 10, 4, 3, 6, 4, 10, 3, '15%', '', '', '', '', 50)
    ]
    
    sample_revenue_data = [
        ('sample001', 'Jan 2025', 'Sample Owner', 'Sample Team', 'SampleWeb', 1500.0, 'Sample Owner', 'Sample Team'),
        ('demo002', 'Feb 2025', 'Demo Owner', 'Demo Team', 'DemoWeb', -500.0, 'Demo Owner', 'Demo Team')
    ]
    
    sample_salary_data = [
        ('Sample Employee', 15000.0, 'Sample Team'),
        ('Demo Employee', 17000.0, 'Demo Team')
    ]
    
    try:
        # Insert sample data
        conn.executemany('''
            INSERT INTO domain_cost (domain, kw, type, team, owner, end_date, plan, cost, month)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_domain_data)
        
        conn.executemany('''
            INSERT INTO hosting_cost (month_registration, month_expire, domain, team, sum_hosting_cost_by_domain)
            VALUES (?, ?, ?, ?, ?)
        ''', sample_hosting_data)
        
        conn.executemany('''
            INSERT INTO performance (domain, team, owner, plan, end_date, cashgame, chalong, playgame,
                                   total_register, total_topup, regis_may, topup_may, regis_june, topup_june,
                                   regis_july, topup_july, cvr, first_seen_cg, first_seen_cl, first_seen_pg,
                                   date_gap, unique_visits)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_performance_data)
        
        conn.executemany('''
            INSERT INTO revenue (code, month, owner, team, web, win_loss, rename, reteam)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_revenue_data)
        
        conn.executemany('''
            INSERT INTO salary (nickname, salary, team)
            VALUES (?, ?, ?)
        ''', sample_salary_data)
        
        conn.commit()
        print("Sample data imported successfully!")
        
    except Exception as e:
        print(f"Error importing sample data: {e}")
    finally:
        conn.close()

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        
        # Get counts for dashboard
        counts = {}
        tables = ['domain_cost', 'hosting_cost', 'performance', 'revenue', 'salary']
        
        for table in tables:
            try:
                count = conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
                counts[table] = count
            except:
                counts[table] = 0
        
        conn.close()
        return render_template('index.html', counts=counts)
    except Exception as e:
        return f"Database connection error: {e}", 500

@app.route('/domain_cost')
def domain_cost():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM domain_cost ORDER BY id DESC LIMIT 100').fetchall()
    conn.close()
    return render_template('domain_cost.html', data=data)

@app.route('/hosting_cost')
def hosting_cost():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM hosting_cost ORDER BY id DESC LIMIT 100').fetchall()
    conn.close()
    return render_template('hosting_cost.html', data=data)

@app.route('/performance')
def performance():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM performance ORDER BY id DESC LIMIT 100').fetchall()
    conn.close()
    return render_template('performance.html', data=data)

@app.route('/revenue')
def revenue():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM revenue ORDER BY id DESC LIMIT 100').fetchall()
    conn.close()
    return render_template('revenue.html', data=data)

@app.route('/salary')
def salary():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM salary ORDER BY id DESC LIMIT 100').fetchall()
    conn.close()
    return render_template('salary.html', data=data)

def safe_float(value):
    """Safely convert value to float"""
    if not value or value == '':
        return 0.0
    try:
        clean_value = str(value).replace(',', '').replace('"', '').strip()
        return float(clean_value)
    except (ValueError, TypeError):
        return 0.0

def safe_int(value):
    """Safely convert value to int"""
    if not value or value == '':
        return 0
    try:
        clean_value = str(value).replace(',', '').replace('"', '').strip()
        return int(float(clean_value))
    except (ValueError, TypeError):
        return 0

@app.route('/import_csv/<table_name>', methods=['POST'])
def import_csv(table_name):
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(url_for(table_name))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for(table_name))
    
    if not file.filename.endswith('.csv'):
        flash('Please select a valid CSV file')
        return redirect(url_for(table_name))

    try:
        conn = get_db_connection()
        csv_data = file.read().decode('utf-8').splitlines()
        csv_reader = csv.DictReader(csv_data)
        
        imported_count = 0
        
        for row in csv_reader:
            try:
                if table_name == 'domain_cost':
                    conn.execute('''
                        INSERT INTO domain_cost (domain, kw, type, team, owner, end_date, plan, cost, month)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        row.get('Domain', ''), 
                        row.get('kw', ''), 
                        row.get('type', ''), 
                        row.get('team', ''), 
                        row.get('owner', ''), 
                        row.get('end_date', ''),
                        row.get('plan', ''), 
                        safe_float(row.get('Cost', 0)), 
                        row.get('Month', '')
                    ))
                
                elif table_name == 'hosting_cost':
                    conn.execute('''
                        INSERT INTO hosting_cost (month_registration, month_expire, domain, team, sum_hosting_cost_by_domain)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        row.get('month_registration', ''), 
                        row.get('month_expire', ''), 
                        row.get('domain', ''), 
                        row.get('team', ''), 
                        safe_float(row.get('sum_hosting_cost_by_domain', 0))
                    ))
                
                elif table_name == 'performance':
                    conn.execute('''
                        INSERT INTO performance (domain, team, owner, plan, end_date, cashgame, chalong, playgame,
                                               total_register, total_topup, regis_may, topup_may, regis_june, topup_june,
                                               regis_july, topup_july, cvr, first_seen_cg, first_seen_cl, first_seen_pg,
                                               date_gap, unique_visits)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        row.get('Domain', ''),
                        row.get('team', ''),
                        row.get('owner', ''),
                        row.get('plan', ''),
                        row.get('end_date', ''),
                        row.get('CASHGAME', ''),
                        row.get('CHALONG', ''),
                        row.get('PLAYGAME', ''),
                        safe_int(row.get('Total Register', 0)),
                        safe_int(row.get('Total Topup', 0)),
                        safe_int(row.get('Regis - May', 0)),
                        safe_int(row.get('Topup - May', 0)),
                        safe_int(row.get('Regis - June', 0)),
                        safe_int(row.get('Topup - June', 0)),
                        safe_int(row.get('Regis - July', 0)),
                        safe_int(row.get('Topup - July', 0)),
                        row.get('CVR', ''),
                        row.get('First Seen - CG', ''),
                        row.get('First Seen - CL', ''),
                        row.get('First Seen - PG', ''),
                        row.get('Date Gap', ''),
                        safe_int(row.get('unique visits', 0))
                    ))
                
                elif table_name == 'revenue':
                    conn.execute('''
                        INSERT INTO revenue (code, month, owner, team, web, win_loss, rename, reteam)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        row.get('code', ''),
                        row.get('month', ''),
                        row.get('Owner', ''),
                        row.get('team', ''),
                        row.get('web', ''),
                        safe_float(row.get('win_loss', 0)),
                        row.get('Rename', ''),
                        row.get('Reteam', '')
                    ))
                
                elif table_name == 'salary':
                    conn.execute('''
                        INSERT INTO salary (nickname, salary, team)
                        VALUES (?, ?, ?)
                    ''', (
                        row.get('ชื่อเล่น', '') or row.get('nickname', ''),
                        safe_float(row.get('เงินเดือน', 0) or row.get('salary', 0)),
                        row.get('เบิกทีม', '') or row.get('team', '')
                    ))
                
                imported_count += 1
                
            except Exception as row_error:
                continue
        
        conn.commit()
        flash(f'Successfully imported {imported_count} records to {table_name}!')
        
    except Exception as e:
        flash(f'Error importing CSV: {str(e)}')
    finally:
        conn.close()
    
    return redirect(url_for(table_name))

@app.route('/add/<table_name>', methods=['POST'])
def add_record(table_name):
    conn = get_db_connection()
    
    try:
        if table_name == 'domain_cost':
            conn.execute('''
                INSERT INTO domain_cost (domain, kw, type, team, owner, end_date, plan, cost, month)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (request.form['domain'], request.form['kw'], request.form['type'], 
                 request.form['team'], request.form['owner'], request.form['end_date'],
                 request.form['plan'], float(request.form['cost']), request.form['month']))
        
        elif table_name == 'hosting_cost':
            conn.execute('''
                INSERT INTO hosting_cost (month_registration, month_expire, domain, team, sum_hosting_cost_by_domain)
                VALUES (?, ?, ?, ?, ?)
            ''', (request.form['month_registration'], request.form['month_expire'], 
                 request.form['domain'], request.form['team'], float(request.form['sum_hosting_cost_by_domain'])))
        
        elif table_name == 'performance':
            conn.execute('''
                INSERT INTO performance (domain, team, owner, plan, end_date, cashgame, chalong, playgame,
                                       total_register, total_topup, regis_may, topup_may, regis_june, topup_june,
                                       regis_july, topup_july, cvr, first_seen_cg, first_seen_cl, first_seen_pg,
                                       date_gap, unique_visits)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (request.form['domain'], request.form['team'], request.form['owner'], request.form['plan'],
                 request.form['end_date'], request.form['cashgame'], request.form['chalong'], request.form['playgame'],
                 int(request.form['total_register']), int(request.form['total_topup']),
                 int(request.form['regis_may']), int(request.form['topup_may']),
                 int(request.form['regis_june']), int(request.form['topup_june']),
                 int(request.form['regis_july']), int(request.form['topup_july']),
                 request.form['cvr'], request.form['first_seen_cg'], request.form['first_seen_cl'],
                 request.form['first_seen_pg'], request.form['date_gap'], int(request.form['unique_visits'])))
        
        elif table_name == 'revenue':
            conn.execute('''
                INSERT INTO revenue (code, month, owner, team, web, win_loss, rename, reteam)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (request.form['code'], request.form['month'], request.form['owner'],
                 request.form['team'], request.form['web'], float(request.form['win_loss']),
                 request.form['rename'], request.form['reteam']))
        
        elif table_name == 'salary':
            conn.execute('''
                INSERT INTO salary (nickname, salary, team)
                VALUES (?, ?, ?)
            ''', (request.form['nickname'], float(request.form['salary']), request.form['team']))
        
        conn.commit()
        flash('Record added successfully!')
    except Exception as e:
        flash(f'Error adding record: {str(e)}')
    finally:
        conn.close()
    
    return redirect(url_for(table_name))

@app.route('/edit/<table_name>/<int:record_id>', methods=['POST'])
def edit_record(table_name, record_id):
    conn = get_db_connection()
    
    try:
        if table_name == 'domain_cost':
            conn.execute('''
                UPDATE domain_cost SET domain=?, kw=?, type=?, team=?, owner=?, end_date=?, plan=?, cost=?, month=?
                WHERE id=?
            ''', (request.form['domain'], request.form['kw'], request.form['type'], 
                 request.form['team'], request.form['owner'], request.form['end_date'],
                 request.form['plan'], float(request.form['cost']), request.form['month'], record_id))
        
        elif table_name == 'hosting_cost':
            conn.execute('''
                UPDATE hosting_cost SET month_registration=?, month_expire=?, domain=?, team=?, sum_hosting_cost_by_domain=?
                WHERE id=?
            ''', (request.form['month_registration'], request.form['month_expire'], 
                 request.form['domain'], request.form['team'], float(request.form['sum_hosting_cost_by_domain']), record_id))
        
        elif table_name == 'performance':
            conn.execute('''
                UPDATE performance SET domain=?, team=?, owner=?, plan=?, end_date=?, cashgame=?, chalong=?, playgame=?,
                                     total_register=?, total_topup=?, regis_may=?, topup_may=?, regis_june=?, topup_june=?,
                                     regis_july=?, topup_july=?, cvr=?, first_seen_cg=?, first_seen_cl=?, first_seen_pg=?,
                                     date_gap=?, unique_visits=?
                WHERE id=?
            ''', (request.form['domain'], request.form['team'], request.form['owner'], request.form['plan'],
                 request.form['end_date'], request.form['cashgame'], request.form['chalong'], request.form['playgame'],
                 int(request.form['total_register']), int(request.form['total_topup']),
                 int(request.form['regis_may']), int(request.form['topup_may']),
                 int(request.form['regis_june']), int(request.form['topup_june']),
                 int(request.form['regis_july']), int(request.form['topup_july']),
                 request.form['cvr'], request.form['first_seen_cg'], request.form['first_seen_cl'],
                 request.form['first_seen_pg'], request.form['date_gap'], int(request.form['unique_visits']), record_id))
        
        elif table_name == 'revenue':
            conn.execute('''
                UPDATE revenue SET code=?, month=?, owner=?, team=?, web=?, win_loss=?, rename=?, reteam=?
                WHERE id=?
            ''', (request.form['code'], request.form['month'], request.form['owner'],
                 request.form['team'], request.form['web'], float(request.form['win_loss']),
                 request.form['rename'], request.form['reteam'], record_id))
        
        elif table_name == 'salary':
            conn.execute('''
                UPDATE salary SET nickname=?, salary=?, team=?
                WHERE id=?
            ''', (request.form['nickname'], float(request.form['salary']), request.form['team'], record_id))
        
        conn.commit()
        flash('Record updated successfully!')
    except Exception as e:
        flash(f'Error updating record: {str(e)}')
    finally:
        conn.close()
    
    return redirect(url_for(table_name))

@app.route('/delete/<table_name>/<int:record_id>')
def delete_record(table_name, record_id):
    conn = get_db_connection()
    try:
        conn.execute(f'DELETE FROM {table_name} WHERE id = ?', (record_id,))
        conn.commit()
        flash('Record deleted successfully!')
    except Exception as e:
        flash(f'Error deleting record: {str(e)}')
    finally:
        conn.close()
    
    return redirect(url_for(table_name))

@app.route('/health')
def health_check():
    """Health check endpoint for Render"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.route('/api/stats')
def api_stats():
    """API endpoint for database statistics"""
    try:
        conn = get_db_connection()
        stats = {}
        tables = ['domain_cost', 'hosting_cost', 'performance', 'revenue', 'salary']
        
        for table in tables:
            count = conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
            stats[table] = count
        
        conn.close()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Initialize database on startup
with app.app_context():
    init_database()
    import_initial_data()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)