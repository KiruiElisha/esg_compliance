frappe.pages['esg-overview'].on_page_load = function(wrapper) {
	// Load Chart.js library
	frappe.require([
		'https://cdn.jsdelivr.net/npm/chart.js@3.7.0/dist/chart.min.js'
	], () => {
		var page = frappe.ui.make_app_page({
			parent: wrapper,
			title: 'ESG Overview Dashboard',
			single_column: true
		});

		// Initialize the ESG Overview
		frappe.esg_overview = new ESGOverview(page);
	});
};

class ESGOverview {
	constructor(page) {
		this.page = page;
		this.filters = {};
		this.make_filters();
		this.make_dashboard();
		this.refresh_data();
	}

	make_filters() {
		// Company Filter
		this.company_filter = this.page.add_field({
			fieldname: 'company',
			label: __('Company'),
			fieldtype: 'Link',
			options: 'Company',
			change: () => {
				this.filters.company = this.company_filter.get_value();
				this.refresh_data();
			}
		});

		// Date Range Filter
		this.date_range = this.page.add_field({
			fieldname: 'date_range',
			label: __('Date Range'),
			fieldtype: 'DateRange',
			change: () => {
				let range = this.date_range.get_value();
				if (range && range.length === 2) {
					this.filters.from_date = range[0];
					this.filters.to_date = range[1];
					this.refresh_data();
				}
			}
		});

		// Refresh Button
		this.page.add_inner_button(__('Refresh'), () => {
			this.refresh_data();
		});
	}

	make_dashboard() {
		this.page.main.html(`
			<div class="esg-dashboard">
				<!-- KPI Cards Row -->
				<div class="row mb-4">
					<div class="col-md-3">
						<div class="card esg-kpi-card environmental">
							<div class="card-body text-center">
								<div class="kpi-icon">🌱</div>
								<h3 class="kpi-value" id="environmental-score">-</h3>
								<p class="kpi-label">Environmental Score</p>
								<small class="kpi-change" id="env-change">-</small>
							</div>
						</div>
					</div>
					<div class="col-md-3">
						<div class="card esg-kpi-card social">
							<div class="card-body text-center">
								<div class="kpi-icon">👥</div>
								<h3 class="kpi-value" id="social-score">-</h3>
								<p class="kpi-label">Social Score</p>
								<small class="kpi-change" id="social-change">-</small>
							</div>
						</div>
					</div>
					<div class="col-md-3">
						<div class="card esg-kpi-card governance">
							<div class="card-body text-center">
								<div class="kpi-icon">⚖️</div>
								<h3 class="kpi-value" id="governance-score">-</h3>
								<p class="kpi-label">Governance Score</p>
								<small class="kpi-change" id="gov-change">-</small>
							</div>
						</div>
					</div>
					<div class="col-md-3">
						<div class="card esg-kpi-card overall">
							<div class="card-body text-center">
								<div class="kpi-icon">📊</div>
								<h3 class="kpi-value" id="overall-score">-</h3>
								<p class="kpi-label">Overall ESG Score</p>
								<small class="kpi-change" id="overall-change">-</small>
							</div>
						</div>
					</div>
				</div>

				<!-- Charts Row -->
				<div class="row mb-4">
					<div class="col-md-6">
						<div class="card">
							<div class="card-header">
								<h5>Initiative Progress by Category</h5>
							</div>
							<div class="card-body">
								<canvas id="initiative-chart" height="300"></canvas>
							</div>
						</div>
					</div>
					<div class="col-md-6">
						<div class="card">
							<div class="card-header">
								<h5>Metrics Performance Trend</h5>
							</div>
							<div class="card-body">
								<canvas id="metrics-trend-chart" height="300"></canvas>
							</div>
						</div>
					</div>
				</div>

				<!-- Statistics Cards -->
				<div class="row mb-4">
					<div class="col-md-4">
						<div class="card stat-card">
							<div class="card-body">
								<div class="row">
									<div class="col-8">
										<h6>Active Policies</h6>
										<h3 id="active-policies">-</h3>
										<small class="text-muted">Total: <span id="total-policies">-</span></small>
									</div>
									<div class="col-4 text-right">
										<div class="stat-icon">📋</div>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div class="col-md-4">
						<div class="card stat-card">
							<div class="card-body">
								<div class="row">
									<div class="col-8">
										<h6>Running Initiatives</h6>
										<h3 id="running-initiatives">-</h3>
										<small class="text-muted">Completion: <span id="avg-completion">-</span>%</small>
									</div>
									<div class="col-4 text-right">
										<div class="stat-icon">🎯</div>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div class="col-md-4">
						<div class="card stat-card">
							<div class="card-body">
								<div class="row">
									<div class="col-8">
										<h6>Overdue Actions</h6>
										<h3 id="overdue-actions" class="text-danger">-</h3>
										<small class="text-muted">Due this week: <span id="due-this-week">-</span></small>
									</div>
									<div class="col-4 text-right">
										<div class="stat-icon">⚠️</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>

				<!-- Recent Activities & Alerts -->
				<div class="row">
					<div class="col-md-8">
						<div class="card">
							<div class="card-header d-flex justify-content-between">
								<h5>Recent Activities</h5>
								<button class="btn btn-sm btn-outline-primary" onclick="frappe.esg_overview.view_all_activities()">View All</button>
							</div>
							<div class="card-body p-0">
								<div id="recent-activities" class="list-group list-group-flush">
									<!-- Activities will be loaded here -->
								</div>
							</div>
						</div>
					</div>
					<div class="col-md-4">
						<div class="card">
							<div class="card-header">
								<h5>Priority Alerts</h5>
							</div>
							<div class="card-body p-0">
								<div id="priority-alerts" class="list-group list-group-flush">
									<!-- Alerts will be loaded here -->
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>

			<style>
				.esg-dashboard {
					padding: 20px;
				}
				
				.esg-kpi-card {
					border-radius: 12px;
					border: none;
					box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
					transition: transform 0.2s ease;
				}
				
				.esg-kpi-card:hover {
					transform: translateY(-2px);
				}
				
				.esg-kpi-card.environmental {
					background: linear-gradient(135deg, #4ade80 0%, #16a34a 100%);
					color: white;
				}
				
				.esg-kpi-card.social {
					background: linear-gradient(135deg, #60a5fa 0%, #2563eb 100%);
					color: white;
				}
				
				.esg-kpi-card.governance {
					background: linear-gradient(135deg, #a78bfa 0%, #7c3aed 100%);
					color: white;
				}
				
				.esg-kpi-card.overall {
					background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
					color: white;
				}
				
				.kpi-icon {
					font-size: 2.5rem;
					margin-bottom: 10px;
				}
				
				.kpi-value {
					font-size: 2rem;
					font-weight: bold;
					margin: 10px 0 5px 0;
				}
				
				.kpi-label {
					margin-bottom: 5px;
					opacity: 0.9;
				}
				
				.kpi-change {
					font-size: 0.8rem;
					opacity: 0.8;
				}
				
				.stat-card {
					border-radius: 8px;
					border: 1px solid #e5e7eb;
					transition: box-shadow 0.2s ease;
				}
				
				.stat-card:hover {
					box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
				}
				
				.stat-icon {
					font-size: 2rem;
					opacity: 0.6;
				}
				
				.activity-item {
					padding: 12px 20px;
					border-bottom: 1px solid #f3f4f6;
				}
				
				.activity-item:last-child {
					border-bottom: none;
				}
				
				.activity-time {
					font-size: 0.8rem;
					color: #6b7280;
				}
				
				.alert-item {
					padding: 10px 15px;
				}
				
				.alert-high {
					border-left: 4px solid #ef4444;
				}
				
				.alert-medium {
					border-left: 4px solid #f59e0b;
				}
				
				.alert-low {
					border-left: 4px solid #10b981;
				}

				.card {
					border-radius: 8px;
					border: 1px solid #e5e7eb;
					margin-bottom: 20px;
				}
				
				.card-header {
					background-color: #f9fafb;
					border-bottom: 1px solid #e5e7eb;
					padding: 15px 20px;
				}
				
				.card-header h5 {
					margin: 0;
					font-weight: 600;
				}
			</style>
		`);
	}

	async refresh_data() {
		this.show_loading();
		
		try {
			// Fetch all data in parallel for better performance
			const [kpiData, chartData, statsData, activitiesData, alertsData] = await Promise.all([
				this.get_kpi_data(),
				this.get_chart_data(),
				this.get_stats_data(),
				this.get_recent_activities(),
				this.get_priority_alerts()
			]);

			this.update_kpi_cards(kpiData);
			this.update_charts(chartData);
			this.update_stats(statsData);
			this.update_activities(activitiesData);
			this.update_alerts(alertsData);
			
		} catch (error) {
			frappe.msgprint(__('Error loading dashboard data: ') + error.message);
		}
		
		this.hide_loading();
	}

	async get_kpi_data() {
		// Get ESG Metric Entries
		const entries = await frappe.call({
			method: 'frappe.client.get_list',
			args: {
				doctype: 'ESG Metric Entry',
				fields: [
					'name', 'metric', 'measured_value', 'target_value',
					'performance', 'variance', 'source_doctype',
					'verification_status', 'entry_date'
				],
				filters: {
					...this.get_base_filters(),
					docstatus: 0
				},
				order_by: 'entry_date desc',
				limit_page_length: 1000
			}
		}).then(r => r.message || []);

		// Group by metric type
		const metricGroups = {
			Environmental: entries.filter(e => 
				e.metric.includes('Carbon') || 
				e.source_doctype === 'Stock Entry'
			),
			Social: entries.filter(e => 
				e.source_doctype === 'Work Order' || 
				e.source_doctype === 'Production Plan'
			),
			Governance: entries.filter(e => 
				e.source_doctype === 'Purchase Invoice' || 
				e.verification_status === 'Verified'
			)
		};

		// Calculate scores
		const scores = {
			environmental: this.calculateScore(metricGroups.Environmental),
			social: this.calculateScore(metricGroups.Social),
			governance: this.calculateScore(metricGroups.Governance)
		};

		// Calculate overall score
		scores.overall = Math.round((scores.environmental + scores.social + scores.governance) / 3);

		// Calculate trends (compare with last month)
		const trends = await this.calculateTrends(entries);

		return {
			...scores,
			trends
		};
	}

	calculateScore(entries) {
		if (!entries.length) return 0;
		
		const greenCount = entries.filter(e => e.performance === 'Green').length;
		return Math.round((greenCount / entries.length) * 100);
	}

	async calculateTrends(entries) {
		const lastMonth = frappe.datetime.add_months(frappe.datetime.get_today(), -1);
		
		const oldEntries = entries.filter(e => 
			frappe.datetime.str_to_obj(e.entry_date) < frappe.datetime.str_to_obj(lastMonth)
		);
		
		const currentEntries = entries.filter(e => 
			frappe.datetime.str_to_obj(e.entry_date) >= frappe.datetime.str_to_obj(lastMonth)
		);

		return {
			environmental: this.calculateTrendChange(
				this.calculateScore(oldEntries.filter(e => e.metric.includes('Carbon'))),
				this.calculateScore(currentEntries.filter(e => e.metric.includes('Carbon')))
			),
			social: this.calculateTrendChange(
				this.calculateScore(oldEntries.filter(e => ['Work Order', 'Production Plan'].includes(e.source_doctype))),
				this.calculateScore(currentEntries.filter(e => ['Work Order', 'Production Plan'].includes(e.source_doctype)))
			),
			governance: this.calculateTrendChange(
				this.calculateScore(oldEntries.filter(e => e.verification_status === 'Verified')),
				this.calculateScore(currentEntries.filter(e => e.verification_status === 'Verified'))
			)
		};
	}

	calculateTrendChange(oldScore, newScore) {
		return newScore - oldScore;
	}

	update_kpi_cards(data) {
		$('#environmental-score').text(data.environmental || 0);
		$('#social-score').text(data.social || 0);
		$('#governance-score').text(data.governance || 0);
		$('#overall-score').text(data.overall || 0);

		// Update trends
		$('#env-change')
			.text(this.formatTrend(data.trends.environmental))
			.removeClass('text-success text-danger text-muted')
			.addClass(this.getTrendClass(data.trends.environmental));
		
		$('#social-change')
			.text(this.formatTrend(data.trends.social))
			.removeClass('text-success text-danger text-muted')
			.addClass(this.getTrendClass(data.trends.social));
		
		$('#gov-change')
			.text(this.formatTrend(data.trends.governance))
			.removeClass('text-success text-danger text-muted')
			.addClass(this.getTrendClass(data.trends.governance));
		
		$('#overall-change')
			.text(this.formatTrend((data.trends.environmental + data.trends.social + data.trends.governance) / 3))
			.removeClass('text-success text-danger text-muted')
			.addClass(this.getTrendClass(data.trends.overall));
	}

	formatTrend(value) {
		if (value > 0) return `↗ +${value.toFixed(1)}%`;
		if (value < 0) return `↘ ${value.toFixed(1)}%`;
		return `→ ${value.toFixed(1)}%`;
	}

	getTrendClass(value) {
		if (value > 0) return 'text-success';
		if (value < 0) return 'text-danger';
		return 'text-muted';
	}

	async get_chart_data() {
		const initiatives = await frappe.call({
			method: 'frappe.client.get_list',
			args: {
				doctype: 'ESG Initiative',
				fields: [
					'name', 
					'initiative_name',
					'status',
					'related_policy',
					'start_date',
					'end_date',
					'progress_',
					'priority',
					'budget',
					'actual_cost'
				],
				filters: {
					...this.get_base_filters(),
					docstatus: 0,
					status: ['!=', 'Completed']
				}
			}
		});

		// Also fetch policies for categorization
		const policies = await frappe.call({
			method: 'frappe.client.get_list',
			args: {
				doctype: 'ESG Policy',
				fields: ['name', 'policy_name', 'description'],
				filters: {
					docstatus: 0
				}
			}
		});

		return { 
			initiatives: initiatives.message || [], 
			policies: policies.message || [] 
		};
	}

	render_initiative_chart(data) {
		if (!window.Chart) {
			console.error('Chart.js not loaded');
			return;
		}

		const ctx = document.getElementById('initiative-chart').getContext('2d');
		
		if (this.initiativeChart) {
			this.initiativeChart.destroy();
		}

		// Group initiatives by policy category
		const categoryMap = {
			'Environmental': ['carbon', 'emission', 'environmental', 'energy', 'waste'],
			'Social': ['social', 'employee', 'community', 'health', 'safety'],
			'Governance': ['governance', 'compliance', 'risk', 'policy', 'regulatory']
		};

		const policyTypes = {
			'Environmental': 0,
			'Social': 0,
			'Governance': 0
		};

		data.initiatives.forEach(initiative => {
			let categorized = false;
			const policyDesc = data.policies.find(p => p.name === initiative.related_policy)?.description?.toLowerCase() || '';
			
			for (const [category, keywords] of Object.entries(categoryMap)) {
				if (keywords.some(keyword => 
					policyDesc.includes(keyword) || 
					initiative.initiative_name?.toLowerCase().includes(keyword)
				)) {
					policyTypes[category]++;
					categorized = true;
					break;
				}
			}
			
			if (!categorized) {
				// Default to Governance if no clear category
				policyTypes['Governance']++;
			}
		});

		this.initiativeChart = new Chart(ctx, {
			type: 'doughnut',
			data: {
				labels: Object.keys(policyTypes),
				datasets: [{
					data: Object.values(policyTypes),
					backgroundColor: ['#4ade80', '#60a5fa', '#a78bfa'],
					borderWidth: 0
				}]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				plugins: {
					legend: {
						position: 'bottom'
					},
					tooltip: {
						callbacks: {
							label: function(context) {
								const label = context.label || '';
								const value = context.raw || 0;
								return `${label}: ${value} initiatives`;
							}
						}
					}
				}
			}
		});
	}

	render_metrics_trend_chart() {
		if (!window.Chart) {
			console.error('Chart.js not loaded');
			return;
		}

		const ctx = document.getElementById('metrics-trend-chart').getContext('2d');
		
		// Destroy existing chart if it exists
		if (this.metricsChart) {
			this.metricsChart.destroy();
		}

		frappe.call({
			method: 'esg_compliance.esg_compliance.page.esg_overview.esg_overview.get_metrics_trend',
			args: {
				filters: this.get_base_filters()
			}
		}).then(r => {
			const { labels, datasets } = r.message;
			
			this.metricsChart = new Chart(ctx, {
				type: 'line',
				data: {
					labels,
					datasets: datasets.map(d => ({
						label: d.label,
						data: d.data,
						borderColor: d.color,
						backgroundColor: `${d.color}20`,
						fill: true,
						tension: 0.4
					}))
				},
				options: {
					responsive: true,
					maintainAspectRatio: false,
					scales: {
						y: {
							beginAtZero: true,
							max: 100
						}
					}
				}
			});
		});
	}

	update_stats(stats) {
		$('#active-policies').text(stats.policies.active || 0);
		$('#total-policies').text(stats.policies.total || 0);
		$('#running-initiatives').text(stats.initiatives.running || 0);
		$('#avg-completion').text(stats.initiatives.avgCompletion || 0);
		$('#overdue-actions').text(stats.actions.overdue || 0);
		$('#due-this-week').text(stats.actions.dueThisWeek || 0);
	}

	update_activities(activities) {
		const html = activities.map(activity => `
			<div class="activity-item">
				<div class="d-flex justify-content-between">
					<strong>${activity.type}: ${activity.name}</strong>
					<small class="activity-time">${activity.time}</small>
				</div>
				<div class="text-muted small">${activity.action} by ${activity.user}</div>
			</div>
		`).join('');
		
		$('#recent-activities').html(html);
	}

	update_alerts(alerts) {
		const html = alerts.map(alert => `
			<div class="alert-item alert-${alert.priority}">
				<div class="small">${alert.message}</div>
				<div class="text-muted" style="font-size: 0.7rem;">${alert.days} day(s) ago</div>
			</div>
		`).join('');
		
		$('#priority-alerts').html(html);
	}

	update_kpi_cards(scores) {
		const formatTrend = (value) => {
			if (value > 0) return `↗ +${value}%`;
			if (value < 0) return `↘ ${value}%`;
			return `→ ${value}%`;
		};

		// Update scores
		$('#environmental-score').text(scores.environmental || 0);
		$('#social-score').text(scores.social || 0);
		$('#governance-score').text(scores.governance || 0);
		$('#overall-score').text(scores.overall || 0);

		// Mock trends (you can replace with actual trend calculation)
		$('#env-change')
			.text(formatTrend(2.3))
			.removeClass('text-success text-danger text-muted')
			.addClass('text-success');
		
		$('#social-change')
			.text(formatTrend(-1.1))
			.removeClass('text-success text-danger text-muted')
			.addClass('text-danger');
		
		$('#gov-change')
			.text(formatTrend(0))
			.removeClass('text-success text-danger text-muted')
			.addClass('text-muted');
		
		$('#overall-change')
			.text(formatTrend(0.8))
			.removeClass('text-success text-danger text-muted')
			.addClass('text-success');
	}

	update_charts(data) {
		this.render_initiative_chart(data);
		this.render_metrics_trend_chart();
	}

	async get_stats_data() {
		const [policies, initiatives, actions] = await Promise.all([
			this.get_policy_stats(),
			this.get_initiative_stats(),
			this.get_action_stats()
		]);

		return { policies, initiatives, actions };
	}

	async get_policy_stats() {
		const today = frappe.datetime.get_today();
		
		const [active, total] = await Promise.all([
			frappe.db.get_list('ESG Policy', {
				filters: {
					...this.get_base_filters(),
					docstatus: 0,
					effective_date: ['<=', today],
					expiry_date: ['>=', today]
				},
				limit: 0
			}),
			frappe.db.get_list('ESG Policy', {
				filters: {
					...this.get_base_filters(),
					docstatus: 0
				},
				limit: 0
			})
		]);

		return { 
			active: active.length, 
			total: total.length,
			expiring_soon: active.filter(p => 
				frappe.datetime.get_day_diff(p.expiry_date, today) <= 30
			).length
		};
	}

	async get_initiative_stats() {
		const data = await frappe.db.get_list('ESG Initiative', {
			fields: [
				'name', 'status', 'start_date', 'end_date', 
				'progress_', 'budget', 'actual_cost'
			],
			filters: {
				...this.get_base_filters(),
				docstatus: 0,
				status: ['in', ['Planned', 'Ongoing']]
			}
		});

		const running = data.length;
		const avgProgress = data.length ? 
			Math.round(data.reduce((sum, i) => sum + (i.progress_ || 0), 0) / data.length) : 0;
		const totalBudget = data.reduce((sum, i) => sum + (i.budget || 0), 0);
		const totalCost = data.reduce((sum, i) => sum + (i.actual_cost || 0), 0);

		return { 
			running, 
			avgProgress,
			budget_utilization: totalBudget ? Math.round((totalCost / totalBudget) * 100) : 0
		};
	}

	async get_action_stats() {
		const today = frappe.datetime.get_today();
		const weekLater = frappe.datetime.add_days(today, 7);
		
		const [overdue, dueThisWeek] = await Promise.all([
			frappe.db.count('ESG Action Item', {
				filters: {
					...this.get_base_filters(),
					status: ['!=', 'Completed'],
					due_date: ['<', today]
				}
			}),
			frappe.db.count('ESG Action Item', {
				filters: {
					...this.get_base_filters(),
					status: ['!=', 'Completed'],
					due_date: ['between', [today, weekLater]]
				}
			})
		]);

		return { overdue, dueThisWeek };
	}

	get_base_filters() {
		const filters = {};
		if (this.filters.company) filters.company = this.filters.company;
		return filters;
	}

	show_loading() {
		$('.esg-dashboard').append('<div class="loading-overlay"><div class="spinner-border text-primary"></div></div>');
	}

	hide_loading() {
		$('.loading-overlay').remove();
	}

	view_all_activities() {
		frappe.route_options = this.filters;
		frappe.set_route('query-report', 'ESG Activity Log');
	}

	async get_recent_activities() {
		const activities = await frappe.db.get_list('ESG Initiative', {
			fields: ['name', 'initiative_name', 'status', 'modified', 'modified_by', 'responsible_person'],
			filters: {
				...this.get_base_filters(),
				docstatus: 0,
				modified: ['>', frappe.datetime.add_days(frappe.datetime.now_date(), -7)]
			},
			order_by: 'modified desc',
			limit: 5
		});

		// Get employee names
		const employeeMap = new Map();
		const employeeNames = await frappe.db.get_list('Employee', {
			fields: ['name', 'employee_name'],
			filters: {
				name: ['in', activities.map(a => a.responsible_person).filter(Boolean)]
			}
		});
		employeeNames.forEach(e => employeeMap.set(e.name, e.employee_name));

		return activities.map(activity => ({
			type: 'Initiative',
			name: activity.initiative_name || activity.name,
			action: `Status changed to ${activity.status}`,
			time: frappe.datetime.comment_when(activity.modified),
			user: employeeMap.get(activity.responsible_person) || activity.modified_by
		}));
	}

	async get_priority_alerts() {
		const alerts = [];
		const today = frappe.datetime.get_today();

		// Check ESG Metrics that need updating
		const overdueMetrics = await frappe.db.get_list('ESG Metric Entry', {
			fields: ['name', 'metric', 'reporting_period', 'modified'],
			filters: {
				...this.get_base_filters(),
				docstatus: 0,
				modified: ['<', frappe.datetime.add_days(today, -30)]
			},
			limit: 5
		});

		overdueMetrics.forEach(entry => {
			alerts.push({
				message: `Metric Entry ${entry.metric} needs updating`,
				priority: 'high',
				days: frappe.datetime.get_day_diff(today, entry.modified)
			});
		});

		// Check initiatives near deadline
		const nearingDeadlines = await frappe.db.get_list('ESG Initiative', {
			fields: ['name', 'initiative_name', 'end_date'],
			filters: {
				...this.get_base_filters(),
				docstatus: 0,
				status: ['in', ['Planned', 'Ongoing']],
				end_date: ['between', [today, frappe.datetime.add_days(today, 14)]]
			},
			limit: 5
		});

		nearingDeadlines.forEach(initiative => {
			alerts.push({
				message: `Initiative ${initiative.initiative_name || initiative.name} due soon`,
				priority: 'medium',
				days: frappe.datetime.get_day_diff(initiative.end_date, today)
			});
		});

		// Check policies expiring soon
		const expiringPolicies = await frappe.db.get_list('ESG Policy', {
			fields: ['name', 'policy_name', 'expiry_date'],
			filters: {
				...this.get_base_filters(),
				docstatus: 0,
				expiry_date: ['between', [today, frappe.datetime.add_days(today, 30)]]
			},
			limit: 5
		});

		expiringPolicies.forEach(policy => {
			alerts.push({
				message: `Policy ${policy.policy_name || policy.name} expires soon`,
				priority: 'low',
				days: frappe.datetime.get_day_diff(policy.expiry_date, today)
			});
		});

		return alerts;
	}
}