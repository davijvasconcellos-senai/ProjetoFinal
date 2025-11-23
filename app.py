from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
from datetime import datetime, timedelta
import random
import os

app = Flask(__name__)
app.secret_key = 'duplotech_6040_secret_key_2023'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Dados simulados da máquina
class MachineData:
    def __init__(self):
        self.status = {
            'operacional': True,
            'temperatura': 42.3,
            'vibracao': 2.1,
            'consumo_energia': 245.8,
            'pressao_ar': 6.2,
            'horas_trabalho': 1247,
            'proxima_manutencao': (datetime.now() + timedelta(days=15)).strftime('%d/%m/%Y'),
            'ultima_manutencao': (datetime.now() - timedelta(days=45)).strftime('%d/%m/%Y')
        }
        
        self.alertas = [
            {'tipo': 'info', 'mensagem': 'Manutenção preventiva agendada para 15 dias', 'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M:%S')},
            {'tipo': 'warning', 'mensagem': 'Vibração acima do normal detectada', 'timestamp': (datetime.now() - timedelta(hours=2)).strftime('%d/%m/%Y %H:%M:%S')},
            {'tipo': 'success', 'mensagem': 'Calibração realizada com sucesso', 'timestamp': (datetime.now() - timedelta(days=1)).strftime('%d/%m/%Y %H:%M:%S')}
        ]
        
        self.metricas = {
            'uptime': 98.7,
            'eficiencia': 92.3,
            'qualidade_corte': 95.8,
            'velocidade_media': 85.2
        }
    
    def update_status(self):
        # Simula pequenas variações nos dados
        self.status['temperatura'] = round(42 + random.uniform(-1, 1), 1)
        self.status['vibracao'] = round(2 + random.uniform(-0.2, 0.2), 1)
        self.status['consumo_energia'] = round(245 + random.uniform(-5, 5), 1)
        self.status['pressao_ar'] = round(6 + random.uniform(-0.1, 0.1), 1)

machine_data = MachineData()

# Context processor para dados globais
@app.context_processor
def inject_global_data():
    user_data = {
        'is_authenticated': session.get('user_authenticated', False),
        'username': session.get('username', 'Visitante'),
        'role': session.get('user_role', 'visitante')
    }
    
    return {
        'current_user': type('User', (), user_data),
        'current_year': datetime.now().year,
        'current_time': datetime.now().strftime('%H:%M:%S')
    }

# ===== ROTAS PRINCIPAIS =====
@app.route('/')
def index():
    machine_data.update_status()
    
    dados_pagina = {
        'current_time': datetime.now().strftime('%H:%M:%S'),
        'proxima_manutencao': machine_data.status['proxima_manutencao'],
        'consumo_energetico': f"{machine_data.status['consumo_energia']} kWh",
        'temperatura': f"{machine_data.status['temperatura']}°C",
        'vibracao': f"{machine_data.status['vibracao']} mm/s",
        'uptime': f"{machine_data.metricas['uptime']}%"
    }
    
    return render_template('index.html', **dados_pagina)

@app.route('/dashboard')
def dashboard():
    if not session.get('user_authenticated'):
        flash('Por favor, faça login para acessar o dashboard.', 'warning')
        return redirect(url_for('login'))
    
    machine_data.update_status()
    
    # Formata os dados para exibição
    status_formatado = {
        'temperatura': f"{machine_data.status['temperatura']}°C",
        'vibracao': f"{machine_data.status['vibracao']} mm/s",
        'consumo_energia': f"{machine_data.status['consumo_energia']} kWh",
        'pressao_ar': f"{machine_data.status['pressao_ar']} bar",
        'horas_trabalho': f"{machine_data.status['horas_trabalho']}h",
        'proxima_manutencao': machine_data.status['proxima_manutencao'],
        'ultima_manutencao': machine_data.status['ultima_manutencao']
    }
    
    metricas_formatadas = {
        'uptime': f"{machine_data.metricas['uptime']}",
        'eficiencia': f"{machine_data.metricas['eficiencia']}",
        'qualidade_corte': f"{machine_data.metricas['qualidade_corte']}",
        'velocidade_media': f"{machine_data.metricas['velocidade_media']}"
    }
    
    return render_template('dashboard.html', 
                         status=status_formatado,
                         metricas=metricas_formatadas,
                         alertas=machine_data.alertas)

@app.route('/analises')
def analises():
    if not session.get('user_authenticated'):
        flash('Por favor, faça login para acessar as análises.', 'warning')
        return redirect(url_for('login'))
    return render_template('analises.html')

@app.route('/configuracoes')
def configuracoes():
    if not session.get('user_authenticated'):
        flash('Por favor, faça login para acessar as configurações.', 'warning')
        return redirect(url_for('login'))
    return render_template('configuracoes.html')

@app.route('/ajuda')
def ajuda():
    return render_template('ajuda.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/documentacao')
def documentacao():
    return render_template('documentacao.html')

# ===== AUTENTICAÇÃO =====
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_authenticated'):
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        users = {
            'admin': {'password': 'admin123', 'role': 'administrador'},
            'operador': {'password': 'op123', 'role': 'operador'},
            'tecnico': {'password': 'tec123', 'role': 'tecnico'}
        }
        
        if username in users and users[username]['password'] == password:
            session['user_authenticated'] = True
            session['username'] = username
            session['user_role'] = users[username]['role']
            flash(f'Login realizado com sucesso! Bem-vindo, {username}.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciais inválidas. Tente novamente.', 'error')
    
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role', 'operador')
        
        if not username or not email or not password:
            flash('Todos os campos obrigatórios devem ser preenchidos.', 'error')
        elif len(username) < 3:
            flash('Nome de usuário deve ter pelo menos 3 caracteres.', 'error')
        elif len(password) < 6:
            flash('A senha deve ter pelo menos 6 caracteres.', 'error')
        elif password != confirm_password:
            flash('As senhas não coincidem.', 'error')
        else:
            flash('Conta criada com sucesso! Faça login para continuar.', 'success')
            return redirect(url_for('login'))
    
    return render_template('registro.html')

@app.route('/logout')
def logout():
    username = session.get('username', 'Usuário')
    session.clear()
    flash(f'Logout realizado com sucesso! Até logo, {username}.', 'info')
    return redirect(url_for('index'))

# ===== API ENDPOINTS =====
@app.route('/api/machine-status')
def api_machine_status():
    if not session.get('user_authenticated'):
        return jsonify({'error': 'Não autorizado'}), 401
    
    machine_data.update_status()
    
    return jsonify({
        'status': machine_data.status,
        'metricas': machine_data.metricas,
        'current_time': datetime.now().strftime('%H:%M:%S')
    })

@app.route('/api/alertas')
def api_alertas():
    if not session.get('user_authenticated'):
        return jsonify({'error': 'Não autorizado'}), 401
    
    return jsonify(machine_data.alertas)

# ===== ERROR HANDLERS =====
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# ===== INICIALIZAÇÃO =====
if __name__ == '__main__':
    print("=" * 60)
    print("🚀 DUPLOTECH 6040 - PLATAFORMA DE MANUTENÇÃO PREDITIVA")
    print("=" * 60)
    print("📁 Verificando arquivos...")
    
    # Verificar arquivos essenciais
    essential_files = [
        ('static/css/style.css', 'CSS Principal'),
        ('templates/base.html', 'Template Base'),
        ('templates/index.html', 'Página Inicial'),
        ('templates/login.html', 'Página de Login')
    ]
    
    all_files_ok = True
    for file_path, description in essential_files:
        if os.path.exists(file_path):
            print(f"✅ {description}")
        else:
            print(f"❌ {description} - AUSENTE")
            all_files_ok = False
    
    if all_files_ok:
        print("🎉 Todos os arquivos essenciais encontrados!")
    else:
        print("⚠️  Alguns arquivos estão ausentes. O sistema pode não funcionar corretamente.")
    
    print("=" * 60)
    print("🌐 Servidor iniciando em: http://localhost:5000")
    print("🔐 Credenciais de teste:")
    print("   👨‍💼 Admin:    admin / admin123")
    print("   👨‍🔧 Operador: operador / op123")
    print("   🔧 Técnico:  tecnico / tec123")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)